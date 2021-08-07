import random
from uuid import uuid4

def generate(rounds):
    from spots.spot import Spot
    import time
    for _ in range(rounds):
        Spot(
            str(uuid4()),
            '60d4f3ef-b172-4e34-b679-54ca71d2dfa4',
            116.33326925061 + 0.0001 * random.randint(-200,200),
            39.986995080731 + 0.0001 * random.randint(-200,200),
            '附近%s侧街道旁'%('左' if random.randint(1,10) < 5 else '右'),
            random.randint(4,400),
            0,
            0,
            '提供饮用水.',
            '%s'%(15001136059 + random.randint(-90000,99999)),
            int(time.time() + random.randint(-1000,1000))
        )._insert()
