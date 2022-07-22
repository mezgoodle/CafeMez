import json
import os


class Storage:
    def __init__(self, filename: str = 'tgbot/misc/storage/storage.json'):
        self.filename = filename
        self.create_file()

    def create_file(self):
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
        try:
            return data[identifier]
        except KeyError:
            return []

    def add_to_cart(self, identifier: str, item: str, quantity: int = 1) -> None:
        data = self.read_file()
        try:
            cart = data[identifier]
        except KeyError:
            cart = []
        cart.extend([item] * quantity)
        data[identifier] = cart
        with open(self.filename, 'w') as f:
            json.dump(data, f)
