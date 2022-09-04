from collections import Counter

from aiogram import Bot
from aiogram.types import Location, LabeledPrice

from tgbot.misc.api import API
from tgbot.config import load_config, Config
from tgbot.misc.calc_distance import choose_shortest

from typing import Tuple, List, Union, Dict


class Backend(API):
    token: str = None
    auth_str = 'Token %s'

    def __init__(self):
        super().__init__()

    async def get_all_objects(self, collection: str) -> Union[list, int]:
        items = await self.get(collection)
        return items

    async def get_object(self, collection: str, item_id: str, additional_path: str = None) -> Union[dict, int]:
        item = await self.get(f'{collection}/{item_id}' + (additional_path if additional_path else ''))
        return item

    async def update_object(self, collection: str, item_id, data: dict) -> Tuple[dict, int]:
        await self.__get_token()
        headers = {'Authorization': self.auth_str % self.token}
        data, status = await self.put(f'{collection}/{item_id}', data, headers=headers)
        return data, status

    async def delete_object(self, collection: str, item_id) -> int:
        await self.__get_token()
        headers = {'Authorization': self.auth_str % self.token}
        status = await self.delete(f'{collection}/{item_id}', headers=headers)
        return status

    async def create_object(self, collection: str, data: dict) -> Tuple[dict, int]:
        await self.__get_token()
        headers = {'Authorization': self.auth_str % self.token}
        data, status = await self.post(collection, data, headers=headers)
        return data, status

    async def __get_token(self):
        if not self.token:
            config: Config = load_config()
            token, status = await self.post('token',
                                            data={
                                                'username': config.admin.email,
                                                'password': config.admin.password
                                            })
            if status == 200:
                self.token = token['token']
            else:
                raise Exception('Could not get token')


class Restaurant(Backend):
    def __init__(self):
        super().__init__()

    async def get_all_restaurants(self) -> list:
        restaurants = await self.get_all_objects('restaurants')
        return restaurants

    async def get_restaurant(self, restaurant_name) -> dict:
        restaurant = await self.get_object('restaurants', restaurant_name)
        return restaurant

    async def create_restaurant(self, name, latitude, longitude) -> Tuple[dict, int]:
        data = {
            'name': name,
            'latitude': latitude,
            'longitude': longitude
        }
        data, status = await self.create_object('restaurants', data)
        return data, status

    async def delete_restaurant(self, restaurant_id) -> int:
        status = await self.delete_object('restaurants', restaurant_id)
        return status


class Place(Backend):
    def __init__(self):
        super().__init__()

    async def get_all_places(self) -> list:
        places = await self.get_all_objects('places')
        return places

    async def get_places_by_restaurant(self, restaurant_name: str) -> list:
        places = await self.get_all_objects(f'places/restaurant/{restaurant_name}')
        return places

    async def get_place(self, place_id) -> dict:
        place = await self.get_object('places', place_id)
        return place

    async def delete_place(self, place_id) -> int:
        status = await self.delete_object('places', place_id)
        return status

    async def update_place(self, place_id, data: dict) -> Tuple[dict, int]:
        data, status = await self.update_object('places', place_id, data)
        return data, status

    async def remove_place(self, place_id) -> int:
        status = await self.delete_object('places', place_id)
        return status


class User(Backend):
    def __init__(self):
        super().__init__()

    async def get_all_users(self) -> list:
        users = await self.get_all_objects('users')
        return users

    async def get_user(self, username: str) -> dict:
        user = await self.get_object('users', username)
        return user

    async def get_staff(self, restaurant_name=None) -> Union[Dict[str, list], list]:
        if restaurant_name:
            return await self.get_all_objects(f'users/get_staff/{restaurant_name}')
        return await self.get_all_objects('users/get_admins')

    async def delete_user(self, username: str) -> int:
        status = await self.delete_object('users', username)
        return status

    async def create_user(self,
                          username: str,
                          email: str,
                          telegram_id: int,
                          restaurant: str = None,
                          is_staff: bool = False,
                          is_chef: bool = False,
                          is_courier: bool = False,
                          password: str = 'test') -> Tuple[dict, int]:
        data = {
            'username': username,
            'password': password,
            'telegram_id': telegram_id,
            'is_staff': is_staff,
            'email': email,
            'is_chef': is_chef,
            'is_courier': is_courier,
            'connected_restaurant': restaurant
        }
        data, status = await self.create_object('users', data)
        return data, status

    async def is_job(self, username: str, job: str) -> bool:
        user = await self.get_user(username)
        try:
            return user[job]
        except KeyError:
            return False


class Item(Backend):
    def __init__(self):
        super().__init__()

    async def create_item(self, data: dict) -> Tuple[dict, int]:
        data, status = await self.create_object('items', data)
        return data, status

    async def get_categories(self, **kwargs) -> List[dict]:
        categories = await self.get_all_objects('categories')
        return categories

    async def get_subcategories(self, category: str) -> List[dict]:
        subcategories = await self.get_all_objects(f'subcategories/by/{category}')
        return subcategories

    async def get_items(self, subcategory: str) -> List[dict]:
        items = await self.get_all_objects(f'items/by/{subcategory}')
        return items

    async def get_item(self, item_id: str) -> dict:
        item = await self.get_object('items', item_id)
        return item


class Referral(Backend):
    def __init__(self):
        super().__init__()

    async def apply_referral(self, from_user_id: int, to_user_id: int) -> Tuple[dict, int]:
        data = {
            'referrer_id': from_user_id,
            'user_id': to_user_id
        }
        data, status = await self.create_object('referrals', data)
        return data, status

    async def get_discount(self, username: str) -> Union[int, bool]:
        discount = await self.get_object('users', username, '/get_discount')
        return discount


class Order(Backend):
    def __init__(self):
        super().__init__()

    async def get_orders(self, username: str) -> list:
        orders = await self.get_all_objects(f'orders/by/{username}')
        return orders

    async def create_order(self,
                           user: str,
                           payment_method: str,
                           shipping_address_name: str,
                           shipping_address_longitude: float = None,
                           shipping_address_latitude: float = None,
                           shipping_price: float = 0.,
                           ) -> Tuple[int, int]:
        data = {
            'user': user,
            'payment_method': payment_method,
            'shipping_address_name': shipping_address_name,
            'shipping_price': float(shipping_price)
        }
        if shipping_address_latitude:
            data['shipping_address_latitude'] = shipping_address_latitude
            data['shipping_address_longitude'] = shipping_address_longitude
        order, status = await self.create_object('orders', data)
        return order['id'], status

    async def add_order_items(self, order_id: int, items: Counter) -> Union[Tuple[int, list], int]:
        item_backend = Item()
        prices = []
        for item_id, quantity in items.items():
            order_item = await item_backend.get_item(item_id)
            prices.append(LabeledPrice(
                label=f'{order_item["name"]}, {quantity} шт.',
                amount=int(order_item['price']) * 100 * quantity
            ))
            _, status = await self.create_object('order_items', {'order': order_id,
                                                                 'item': order_item['name'],
                                                                 'quantity': quantity
                                                                 }
                                                 )
            if status != 201:
                return status
        return 201, prices

    async def get_order(self, order_id: str) -> dict:
        order = await self.get_object('orders', order_id)
        return order

    async def get_order_by_courier(self, username: str) -> dict:
        order = await self.get_object('users', username, '/get_order')
        return order

    async def get_orders_by_username(self, username: str) -> List[dict]:
        orders = await self.get_all_objects(f'users/{username}/get_orders')
        return orders

    async def get_order_item(self, item_id: str) -> dict:
        item = await self.get_object('order_items', item_id)
        return item

    async def update_order(self, order_id: str, data: dict) -> Tuple[dict, int]:
        data, status = await self.update_object('orders', order_id, data)
        return data, status

    async def delete_order(self, order_id: str) -> int:
        status = await self.delete_object('orders', order_id)
        return status

    @staticmethod
    async def get_shipping_price(location: Location, bot: Bot) -> tuple:
        distances = await choose_shortest(location, bot)
        return distances[0][0], distances[0][1] * 15
