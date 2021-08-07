from flask.wrappers import Response
from spots.test_data_generator import generate
from flask import Flask, request, render_template, jsonify
from flask.helpers import make_response
from werkzeug.utils import redirect

from config import DEBUG, AK
from utils import login_required
from spots import spot_manager

server = Flask(__name__)

if DEBUG:
    print('Enabling CORS.')
    from flask_cors import CORS
    CORS(server)


@server.route('/')
def index():
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
        resp = make_response(redirect('/'))
        resp.set_cookie('reserved', '')
        return resp
    return redirect('/')


@server.route('/editor', methods=['GET', 'POST'])
@login_required
def editor(token):
    if request.method == 'GET':
        return render_template('editor.html', access_key=AK)
    else:
        for k, v in request.form.items():
            print('%s -> %s' % (k, v))
        return render_template('editor.html', access_key=AK)


@server.route('/spots/<uid>', methods=['GET', 'POST'])
def detail(uid):
    r = request.cookies.get('reserved')
    if request.method == 'GET':
        return render_template('detail.html', spot=spot_manager.get_spot(uid), access_key=AK, reserved=(r != ''))
    else:
        name = request.form.get('name', '群众')
        phone = request.form.get('contact', '无信息')
        # TODO: do something
        spot = spot_manager.get_spot(uid)
        spot.set_registered(spot.registered + 1)
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
        return '''<form method="POST" action="/login"><button>LOGIN</button><input value=%s name="next"/></form>''' % request.args.get('next', '/')
    else:
        r = make_response(redirect(request.form.get('next')))
        r.set_cookie('sessionToken', '233666', max_age=3600*24*32)
        return r


if __name__ == '__main__':
    # generate(300)
    server.run(host='0.0.0.0', debug=DEBUG, port=80)
