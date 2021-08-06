from flask import Flask, request, render_template

from consts import DEBUG, AK

server = Flask(__name__)

if DEBUG:
    print('Enabling CORS.')
    from flask_cors import CORS
    CORS(server)

@server.route('/')
def index():
    return render_template('index.html', access_key = AK)

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug = DEBUG, port=80)