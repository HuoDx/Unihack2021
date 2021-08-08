from hashlib import sha256
import os
from uuid import uuid4
import time

from flask.wrappers import Response
from spots.test_data_generator import generate
from flask import Flask, request, render_template, jsonify
from flask.helpers import make_response
from werkzeug.utils import redirect

from config import DEBUG, AK
from utils import distance_between, login_required, connect_to_database
from spots import spot_manager
from spots.spot import Spot
import session_manager

server = Flask(__name__)

if DEBUG:
    print('Enabling CORS.')
    from flask_cors import CORS
    CORS(server)


@server.route('/')
def index():
    return render_template('welcome.html')


@server.route('/map')
def map_index():
    r = request.cookies.get('reserved')
    if r is not None and spot_manager.get_spot(r) is not None:
        return redirect('/spots/%s' % r)
    resp = make_response(render_template('index.html', access_key=AK))
    resp.set_cookie('reserved', '')
    return resp


@server.route('/cancel-reservation')
def cancel_reservation():
    r = request.cookies.get('reserved')
    if r is not None:
        spot = spot_manager.get_spot(r)
        spot.set_registered(spot.registered - 1)
        resp = make_response(redirect('/map'))
        resp.set_cookie('reserved', '')
        return resp
    return redirect('/map')


@server.route('/arrive')
def arrive():
    r = request.cookies.get('reserved')
    if r is not None:
        spot = spot_manager.get_spot(r)
        resp = make_response(render_template('arrived.html'))
        resp.set_cookie('reserved', '')
        return resp
    return redirect('/map')


@server.route('/panel/<spot_uid>')
@login_required
def panel(token, spot_uid):
    if spot_manager.get_spot(spot_uid).owner != session_manager.get_uid(token):
        return redirect('/map')
    data = []
    with connect_to_database() as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM reservations WHERE spot_uid=%s', (spot_uid,))
        results = cursor.fetchall()
        for result in results:
            data.append({'name': result[0], 'contact': result[1]})
    return render_template('panel.html', data=data)


@server.route('/editor', methods=['GET', 'POST'])
@login_required
def editor(token):
    if request.method == 'GET':
        return render_template('editor.html', access_key=AK)
    else:
        logo_option = request.form.get('logo-option')
        title = request.form.get('title')
        lng = request.form.get('lng')
        lat = request.form.get('lat')
        location_description = request.form.get('location-description')
        capacity = request.form.get('capacity')
        description = request.form.get('description')
        contact = request.form.get('contact')

        s = Spot(
            str(uuid4()),
            session_manager.get_uid(token),
            lng,
            lat,
            location_description,
            capacity,
            0,
            title,
            '/static/%s.svg' % logo_option,
            description,
            contact,
            int(time.time()*1e3)
        )
        spot_manager.add_spot(s)
        s._insert()
        return render_template('editor.html', access_key=AK)


def reserve(uid, name, phone):
    with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO reservations VALUES(%s,%s,%s);', (
                name,
                phone,
                uid
            ))
    spot = spot_manager.get_spot(uid)
    spot.set_registered(spot.registered + 1)

@server.route('/automatch', methods=['GET', 'POST'])
def automatch():
    r = request.cookies.get('reserved')
    if r is not None and spot_manager.get_spot(r) is not None:
        return redirect('/spots/%s' % r)

    if request.method == 'GET':
        return render_template('automatch.html', access_key=AK)
    else:
        name = request.form.get('name', '群众')
        phone = request.form.get('contact', '无信息')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        logo_option = request.form.get('logo-option')
        target = []
        for spot in spot_manager.spots:
            if logo_option in spot.logo:
                target.append((distance_between((lng, lat), (spot.lng, spot.lat)), spot._uid))
        s = sorted(target, key=lambda d: d[0])
        print(s[0])
        uid = s[0][1]
        reserve(uid, name, phone)
        response = make_response(render_template(
            'detail.html', spot=spot_manager.get_spot(uid), access_key=AK, reserved=True))
        response.set_cookie('reserved', uid, max_age=3600*24*3)
        return response

@server.route('/spots/<uid>', methods=['GET', 'POST'])
def detail(uid):
    r = request.cookies.get('reserved')
    if request.method == 'GET':
        return render_template('detail.html', spot=spot_manager.get_spot(uid), access_key=AK, reserved=(r != ''))
    else:
        name = request.form.get('name', '群众')
        phone = request.form.get('contact', '无信息')
        # TODO: do something
        reserve(uid, name, phone)
        response = make_response(render_template(
            'detail.html', spot=spot_manager.get_spot(uid), access_key=AK, reserved=True))
        response.set_cookie('reserved', uid, max_age=3600*24*3)
        return response


@server.route('/api/nearby-spots', methods=['GET'])
def nearby_spots():
    lng: float = request.args.get('lng', type=float)
    lat: float = request.args.get('lat', type=float)
    result = []
    for spot in spot_manager.get_nearby_spots((lng, lat)):
        result.append(spot.brief())
    return jsonify(result)


@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next = request.args.get('next', '/map'))
    else:
        password = request.form.get('password')
        email = request.form.get('email')
        uid = None
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
            result = cursor.fetchone()

            if sha256(bytes(password + result[-1], encoding='UTF-8')).hexdigest() == result[2]:
                uid = result[0]
            else:
                return redirect('/login')
        token = session_manager.add_session(uid)
        r = make_response(redirect(request.form.get('next')))
        r.set_cookie('sessionToken', token, max_age=3600*24)
        return r

@server.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', next = request.args.get('next', '/map'))
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')

        uid = str(uuid4())
        salt = os.urandom(4).hex()
        salted_hashed_password = sha256(bytes(password + salt, encoding='UTF-8')).hexdigest()
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO users VALUES(%s,%s,%s,%s,%s)',(
                    uid,
                    email,
                    salted_hashed_password,
                    name,
                    salt
                ))
            else:
                if sha256(bytes(password + result[-1], encoding='UTF-8')).hexdigest() == result[2]:
                    uid = result[0]
                else:
                    return redirect('/register')
        
        token = session_manager.add_session(uid)

        r = make_response(redirect(request.form.get('next')))

        r.set_cookie('sessionToken', token, max_age=3600*24)
        return r

if __name__ == '__main__':
    # generate(300)
    server.run(host='0.0.0.0', debug=DEBUG, port=80)
