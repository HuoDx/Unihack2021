from spots.spot import Spot
from utils import distance_between, connect_to_database

spots:list[Spot] = []

with connect_to_database() as connection:
    cursor = connection.cursor()
    cursor.execute('SELECT _uid FROM spots;')
    uids = cursor.fetchall()
    print('Loadded %d spots.'%len(uids))
    for uid in uids:
        spots.append(Spot.load(uid))
    cursor.close()
    
def get_spot(uid):
    global spots
    if spots is None:
        return None
    for spot in spots:
        if spot._uid == uid:
            return spot

def add_spot(spot):
    global spots
    spots.append(spot)     

def get_nearby_spots(point: tuple[float, float]) -> list:
    global spots
    filtered: list[Spot] = []
    for spot in spots:
        if distance_between((spot.lng, spot.lat), point) < 1500 and spot.capacity - spot.registered > 0:
            filtered.append(spot)
    return filtered



