from utils import connect_to_database


class Spot:
    def __init__(
        self,
        owner: str,
        lng: float,
        lat: float,
        location_description: str,
        capacity: int,
        arrived: int,
        arriving: int,
        description: str,
        contact_number: str,
        created_at: int,
    ):  # ugly code, sad face
        self.lng = lng
        self.lat = lat
        self.location_description = location_description
        self.owner = owner
        self.capacity = capacity
        self.arrived = arrived
        self.arriving = arriving
        self.description = description
        self.contact_number = contact_number
        self.created_at = created_at

    def set_arrived(self, new_value):
        self.arrived = new_value
        with connect_to_database() as connection:
            connection.cursor().execute(
                'UPDATE spots SET arrived = %s WHERE _owner = %s;', (new_value, self.owner))

    def set_arriving(self, new_value):
        self.arriving = new_value
        with connect_to_database() as connection:
            connection.cursor().execute(
                'UPDATE spots SET arriving = %s WHERE _owner = %s;', (new_value, self.owner))

    def calculate_availiability(self):
        if self.arrived >= self.capacity:
            return 2
        if self.arrived + self.arrving >= self.capacity and self.arrived < self.capacity:
            return 1
        return 0

    def brief(self) -> dict:
        return {
            'location': {
                'lng': self.lng,
                'lat': self.lat
            },
            'capacity': self.capacity,
            'availiability': self.calculate_availiability()
        }

    def _insert(self):
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO spots VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            ''', (
                self.owner,
                self.lng,
                self.lat,
                self.location_description,
                self.capacity,
                self.arrived,
                self.arriving,
                self.description,
                self.contact_number,
                self.created_at,
            ))

    @staticmethod
    def delete(cls, uid):
        with connect_to_database() as connection:
            connection.cursor().execute('DELETE * FROM spots WHERE _owner = %s', (uid,))

    @classmethod
    def load(cls, uid):
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM spots WHERE _owner = %s', (uid,))
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                return 'No such UID', True

            return Spot(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5],
                result[6],
                result[7],
                result[8],
                result[9],
            )
