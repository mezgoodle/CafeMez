from tgbot.misc.api import API
from tgbot.config import load_config, Config


class Backend:
    token: str = None
    auth_str = 'Token %s'

    def __init__(self, api):
        self.api: API = api

    async def get_all_items(self, collection: str):
        items = await self.api.get(collection)
        return items

    async def get_item(self, collection: str, item_id):
        item = await self.api.get(f'{collection}/{item_id}')
        return item

    async def update_item(self, collection: str, item_id, name, price, category_id, subcategory_id):
        await self.get_token()
        pass

    async def delete_item(self, collection: str, item_id):
        await self.get_token()
        headers = {'Authorization': self.auth_str % self.token}
        status = await self.api.delete(f'{collection}/{item_id}', headers=headers)
        return status

    async def create_item(self, collection: str, data: dict):
        await self.get_token()
        headers = {'Authorization': self.auth_str % self.token}
        status = await self.api.post(collection, data, headers=headers)
        return status

    async def get_token(self):
        if not self.token:
            config: Config = load_config()
            token = await self.api.post('token',
                                        data={
                                            'username': config.admin.email,
                                            'password': config.admin.password
                                        })
            self.token = token['token']


class Restaurant(Backend):
    def __init__(self, api):
        super().__init__(api)

    async def get_all_restaurants(self):
        restaurants = await self.get_all_items('restaurants')
        return restaurants

    async def get_restaurant(self, restaurant_id):
        restaurant = await self.get_item('restaurants', restaurant_id)
        return restaurant

    async def create_restaurant(self, name, latitude, longitude):
        data = {
            'name': name,
            'latitude': latitude,
            'longitude': longitude
        }
        status = await self.create_item('restaurants', data)
        return status

    async def delete_restaurant(self, restaurant_id):
        status = await self.delete_item('restaurants', restaurant_id)
        return status


class Place(Backend):
    def __init__(self, api):
        super().__init__(api)

    async def get_all_places(self):
        places = await self.get_all_items('places')
        return places

    async def get_places_by_restaurant(self, restaurant_name: str):
        places = await self.get_all_items(f'places/restaurant/{restaurant_name}')
        return places

    async def get_place(self, place_id):
        place = await self.get_item('places', place_id)
        return place

    async def delete_place(self, place_id):
        status = self.delete_item('places', place_id)
        return status


class User(Backend):
    def __init__(self, api):
        super().__init__(api)

    async def get_all_users(self):
        users = await self.get_all_items('users')
        return users

    async def get_user(self, username: str):
        user = await self.get_item('users', username)
        return user

    async def delete_user(self, username: str):
        status = self.delete_item('users', username)
        return status

    async def create_user(self, username: str, email: str, is_staff: bool = False, password: str = None):
        data = {
            'username': username,
            'password': password,
            'is_staff': is_staff,
            'email': email,
        }
        status = await self.create_item('users', data)
        return status

    async def is_staff(self, username: str):
        user = await self.get_user(username)
        return user['is_staff']

    async def is_superuser(self, username: str):
        user = await self.get_user(username)
        return user['is_superuser']


class Product(Backend):
    def __init__(self, api):
        super().__init__(api)
