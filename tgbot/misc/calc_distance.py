import math

from aiogram.types import Location

from tgbot.misc.coords import restaurants
from tgbot.misc.map import show


def calc_distance(lat1, lon1, lat2, lon2):
    radius = 6373.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = radius * c

    return distance


def choose_shortest(location: Location):
    distances = list()
    for shop_name, shop_coords in restaurants.items():
        distances.append((shop_name,
                          calc_distance(location.latitude, location.longitude,
                                        shop_coords['lat'], shop_coords['lot']),
                          show(**shop_coords),
                          shop_coords
                          ))
    return sorted(distances, key=lambda x: x[1])[:2]
