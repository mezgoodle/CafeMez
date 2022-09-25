import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import io
from datetime import datetime, timedelta

matplotlib.use('TkAgg')


async def make_analysis(data: list, message: Message) -> Message:
    df: pd.DataFrame = prepare_df(data)
    df = casting_types(df)
    await plot_restaurant_count(df, message)
    await plot_items_price(df, message)
    await histplot_items(df, message)
    await scatter_time(df, message)
    return await send_text(df, message)


def prepare_df(data: list):
    df = pd.DataFrame([
        {
            'name': order_item['item']['name'],
            'price': order_item['item']['price'],
            'quantity': order_item['quantity'],
            'time': order_item['created'],
            'restaurant': order_item['order']['shipping_address_name'],
            'time_period': make_period(order_item['created'])
        } for order_item in data
    ])
    return df


def make_period(time) -> str:
    time = parsing_iso_string(time)
    hour = time.hour
    periods = {
        (8, 12): 'Early day',
        (12, 18): 'Late day',
        (18, 22): 'Evening'
    }
    for key, value in periods.items():
        if key[0] <= hour < key[1]:
            return value
    return periods[(8, 12)]


def parsing_iso_string(time: str):
    dt, _, us = time.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)


def casting_types(df: pd.DataFrame):
    df['time'] = pd.to_datetime(df['time']).dt.normalize()
    return df


async def plot_restaurant_count(df: pd.DataFrame, message: Message):
    fig, _ = plt.subplots(figsize=(6,6))
    sns.countplot(x=df['restaurant'], palette='Greens')
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    await message.answer_photo(img, 'Кількість замовлень у кожному ресторані')


async def plot_items_price(df: pd.DataFrame, message: Message):
    fig, _ = plt.subplots(figsize=(6,6))
    sns.barplot(x='quantity', y='restaurant', hue='name', data=df, palette="Greens")
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    await message.answer_photo(img, 'Бла бла')


async def histplot_items(df: pd.DataFrame, message: Message):
    fig, _ = plt.subplots(figsize=(6,6))
    sns.histplot(df['name'])
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    await message.answer_photo(img, 'хістплот айтемс')


async def scatter_time(df: pd.DataFrame, message: Message):
    fig, _ = plt.subplots(figsize=(6,6))
    sns.scatterplot(data=df, x="time_period", y='name', hue='restaurant')
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    await message.answer_photo(img, 'scatter time')


async def send_text(df: pd.DataFrame, message: Message):
    text = ''
    grouped_df = df.groupby('name')['price'].agg(['median', 'mean'])
    indexes = grouped_df.index
    columns = grouped_df.columns
    for index in indexes:
        text += f'Товар {hbold(index)}: '
        for column in columns:
            text += f'{column} - {hbold(grouped_df.loc[index, column])}, '
        text += '\n'
    return await message.answer(text)
