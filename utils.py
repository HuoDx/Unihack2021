import math
from functools import wraps

from flask import request, redirect
import psycopg2

from config import DatabaseConfig

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('sessionToken', None)
        if token is None:
            return redirect('/login?next=%s' % request.url)
        return func(token, *args, **kwargs)
    return wrapper


def distance_between(point1, point2) -> int:
    '''
    point1, tuple: (lng, lat);
    point2, tuple: (lng, lat);
    gets the distance between in meters.
    '''
    lng1 = math.radians(point1[0])
    lng2 = math.radians(point1[0])
    lat1 = math.radians(point1[0])
    lat2 = math.radians(point1[0])
    lat_dist = lat1 - lat2
    lng_dist = lng1 - lng2
    s = 2 * math.asin(
        math.sqrt(
            math.sin(lat_dist/2)**2 + math.cos(lat1) *
            math.cos(lat2) * math.sin(lng_dist/2)**2
        )
    )

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