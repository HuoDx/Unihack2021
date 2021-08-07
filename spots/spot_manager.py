from spots.spot import Spot
from utils import distance_between, connect_to_database

spots:list[Spot] = []
with connect_to_database() as connection:
    cursor = connection.cursor()
    cursor.execute('SELECT _uid FROM spots;')
    uids = cursor.fetchall()
    cursor.close()
    print('Loadded %d spots.'%len(uids))
    for uid in uids:
        spots.append(Spot.load(uid))
    

def get_nearby_spots(point: tuple[float, float]) -> list:
    global spots
    filtered: list[Spot] = []
    for spot in spots:
        if distance_between((spot.lng, spot.lat), point) < 1000:
            filtered.append(spot)
    return filtered



