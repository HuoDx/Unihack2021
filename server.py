from flask import Flask, request, render_template
from flask.helpers import make_response
from werkzeug.utils import redirect

from config import DEBUG, AK
from utils import login_required
server = Flask(__name__)

if DEBUG:
    print('Enabling CORS.')
    from flask_cors import CORS
    CORS(server)

@server.route('/')
@login_required
def index(token):
    return render_template('index.html', access_key = AK)

@server.route('/api/nearby-spots', methods=['GET'])
def get_nearby_spots():
    lng: float = request.args.get('lng', type=float)
    lat: float = request.args.get('lat', type=float)

@server.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''<form method="POST" action="/login"><button>LOGIN</button><input value=%s name="next"/></form>'''%request.args.get('next','/')
    else:
        r = make_response(redirect(request.form.get('next')))
        r.set_cookie('sessionToken', '233666', max_age=3600*24*32)
        return r


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug = DEBUG, port=80)