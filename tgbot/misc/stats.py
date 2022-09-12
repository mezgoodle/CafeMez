import pandas as pd
from pprint import pprint


def make_analysis(data: list):
    df: pd.DataFrame = prepare_df(data)
    print(df.to_string())


def prepare_df(data: list):
    df = pd.DataFrame([
        {
            'name': order_item['item']['name'],
            'price': order_item['item']['price'],
            'quantity': order_item['quantity'],
            'time': order_item['created'],
            'restaurant': order_item['order']['shipping_address_name']
        } for order_item in data
    ])
    return df



