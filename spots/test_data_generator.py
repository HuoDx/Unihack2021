import random
from uuid import uuid4

def generate(rounds):
    from spots.spot import Spot
    import time
    for _ in range(rounds):
        x = random.randint(0,2)
        cap = random.randint(4,40)
        Spot(
            str(uuid4()),
            'fab92cb1-91af-4fc6-8ac7-074ec0876e5e',
            116.402759 + 0.0001 * random.randint(-300,300),
            40.016628 + 0.0001 * random.randint(-300,300),
            '',
            cap,
            random.randint(0,cap),
            places[x][1],
            places[x][0],
            '希望能给需要的人一些帮助.',
            '%s'%(15901436059 + random.randint(-90000,99999)),
            int(time.time()*1e3)
        )._insert()

places = [
    ('/static/water.svg', '提供饮用水'),
    ('/static/food.svg', '提供简餐'),
    ('/static/shelter.svg', '可以室内留宿'),
]