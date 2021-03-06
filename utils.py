import math
from functools import wraps

from flask import request, redirect
from flask.helpers import make_response
import psycopg2
from geopy.distance import geodesic

from config import DatabaseConfig
from session_manager import get_uid

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('sessionToken', None)
        if token is None:
            return redirect('/login?next=%s' % request.url)
        if get_uid(token) is None:
            r = make_response(redirect('/login?next=%s' % request.url))
            r.set_cookie('sesstionToken', '')
            return r
        return func(token, *args, **kwargs)
    return wrapper

def distance_between(point1, point2) -> float:
    global RADIUS
    '''
    point1, tuple: (lng, lat);
    point2, tuple: (lng, lat);
    gets the distance between in meters.
    '''
    
    return geodesic(reversed(point1), reversed(point2)).meters

class _DatabaseConnection:

    def __enter__(self):
        try:
            self._connection = psycopg2.connect(
                dbname = DatabaseConfig.database,
                user = DatabaseConfig.user, 
                host = DatabaseConfig.host, 
                password = DatabaseConfig.password, 
                port = DatabaseConfig.port
            )
            return self._connection
        except Exception as e:
            print('Cannot connect to database: %s'%e)
        
    def __exit__(self, type, value, traceback):
        if value != None:
            # an error occured; rollback
            print('An SQL error occured:  ')
            self._connection.rollback()
        self._connection.commit()
        self._connection.close()

def connect_to_database():
    return _DatabaseConnection()