import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from aiogram.types import Message, InputFile

import os

matplotlib.use('TkAgg')
# TODO: make unique path_name
path_name = 'plot.png'


async def make_analysis(data: list, message: Message):
    df: pd.DataFrame = prepare_df(data)
    df = casting_types(df)
    await plot_restaurant_count(df, message)
    await plot_items_price(df, message)
    await histplot_items(df, message)
    await scatter_time(df, message)
    return
    
    d = df.groupby('name')['price'].agg(['median', 'mean'])
    indexes = d.index
    columns = d.columns
    for index in indexes:
        for column in columns:
            print(index, column)
            print(d.loc[index, column])
        print()
    df.to_csv('./data.csv')


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


def casting_types(df: pd.DataFrame):
    df['time'] = pd.to_datetime(df['time']).dt.normalize()
    return df


async def plot_restaurant_count(df: pd.DataFrame, message: Message):
    sns.countplot(x=df['restaurant'], palette='Greens')
    plt.savefig(path_name)
    photo_bytes = InputFile(path_or_bytesio=path_name)
    await message.answer_photo(photo_bytes, 'Кількість замовлень у кожному ресторані')
    os.remove(path_name)


async def plot_items_price(df: pd.DataFrame, message: Message):
    sns.barplot(x='price', y='restaurant', hue='name', data=df, palette="Greens")
    plt.savefig(path_name)
    photo_bytes = InputFile(path_or_bytesio=path_name)
    await message.answer_photo(photo_bytes, 'Бла бла')
    os.remove(path_name)


async def histplot_items(df: pd.DataFrame, message: Message):
    sns.histplot(df['name'])
    plt.savefig(path_name)
    photo_bytes = InputFile(path_or_bytesio=path_name)
    await message.answer_photo(photo_bytes, 'хістплот айтемс')
    os.remove(path_name)


async def scatter_time(df: pd.DataFrame, message: Message):
    df.plot.scatter(x='time', y='restaurant')
    plt.savefig(path_name)
    photo_bytes = InputFile(path_or_bytesio=path_name)
    await message.answer_photo(photo_bytes, 'scatter time')
    os.remove(path_name)
