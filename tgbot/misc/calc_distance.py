import math
from typing import Dict

from aiogram import Bot
from aiogram.types import Location

from tgbot.misc.map import show


def calc_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate dinstance between two points by their coordinates

    Args:
        lat1 (float): latitude of the first point
        lon1 (float): longitude of the first point
        lat2 (float): latitude of the second point
        lon2 (float): longitude of the second point

    Returns:
        float: dinstance in kilometres
    """
    radius = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = radius * c

    return distance


async def choose_shortest(location: Location, bot: Bot) -> list:
    """Choose the nearest two points

    Args:
        location (Location): location from Telegram message
        bot (Bot): bot instance

    Returns:
        list: coordinates of the two nearest restaurants
    """
    distances = list()
    api = bot.get("restaurants_api")
    restaurants = await api.get_all_restaurants()
    for restaurant in restaurants:
        coord_dict: Dict[str, float] = {
            "lat": restaurant["latitude"],
            "lot": restaurant["longitude"],
        }
        distances.append(
            (
                restaurant["name"],
                calc_distance(
                    location.latitude,
                    location.longitude,
                    restaurant["latitude"],
                    restaurant["longitude"],
                ),
                show(**coord_dict),
                coord_dict,
            )
        )
    return sorted(distances, key=lambda x: x[1])[:2]
