import json
import os


class Storage:
    def __init__(self, filename: str = 'tgbot/misc/storage/storage.json'):
        self.filename = filename
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def delete_file(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def read_file(self, mode: str = 'r') -> dict:
        with open(self.filename, mode) as f:
            return json.load(f)

    def get_cart(self, identifier: str) -> list:
        data = self.read_file()
        return self.getting_data(data, str(identifier))

    def add_to_cart(self, identifier: str, item: str, quantity: int = 1) -> None:
        data = self.read_file()
        cart = self.getting_data(data, str(identifier))
        cart.extend([item] * quantity)
        data[str(identifier)] = cart
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def remove_from_cart(self, identifier: str, item: str) -> None:
        data = self.read_file()
        cart = self.getting_data(data, str(identifier))
        cart = list(filter((item).__ne__, cart))
        data[str(identifier)] = cart
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def change_amount(self, identifier: str, item: str, amount: int) -> None:
        self.remove_from_cart(identifier, item)
        self.add_to_cart(identifier, item, amount)

    def clean_cart(self, identifier: str) -> None:
        data = self.read_file()
        del data[str(identifier)]
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def getting_data(data: dict, key: str) -> list:
        try:
            return data[key]
        except KeyError:
            return []


