from utils import connect_to_database


class Spot:
    def __init__(
        self,
        uid: str,
        owner: str,
        lng: float,
        lat: float,
        location_description: str,
        capacity: int,
        registered: int,
        title: int,
        logo: str,
        description: str,
        contact_number: str,
        created_at: int,
    ):  # ugly code, sad face
        self._uid = uid
        self.lng = lng
        self.lat = lat
        self.location_description = location_description
        self.owner = owner
        self.capacity = capacity
        self.registered = registered
        self.title = title
        self.logo = logo
        self.description = description
        self.contact_number = contact_number
        self.created_at = created_at

    def set_registered(self, new_value):
        self.registered = new_value
        with connect_to_database() as connection:
            connection.cursor().execute(
                'UPDATE spots SET registered = %s WHERE _uid = %s;', (new_value, self._uid))

    def set_arriving(self, new_value):
        self.arriving = new_value
        with connect_to_database() as connection:
            connection.cursor().execute(
                'UPDATE spots SET arriving = %s WHERE _uid = %s;', (new_value, self._uid))

    def brief(self) -> dict:
        return {
            'location': {
                'lng': self.lng,
                'lat': self.lat
            },
            'capacity': self.capacity,
            'availiability': self.capacity - self.registered,
            'description': self.description,
            'uid': self._uid,
            'logo': self.logo,
            'title': self.title
        }

    def _insert(self):
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO spots VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            ''', (
                self._uid,
                self.owner,
                self.lng,
                self.lat,
                self.location_description,
                self.capacity,
                self.registered,
                self.title,
                self.logo,
                self.description,
                self.contact_number,
                self.created_at,
            ))

    @staticmethod
    def delete(cls, uid):
        with connect_to_database() as connection:
            connection.cursor().execute('DELETE * FROM spots WHERE _uid = %s', (uid,))

    @classmethod
    def load(cls, uid):
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM spots WHERE _uid = %s', (uid,))
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
                result[10],
                result[11]
            )
