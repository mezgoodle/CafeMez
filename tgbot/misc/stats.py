import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


def make_analysis(data: list):
    df: pd.DataFrame = prepare_df(data)
    df = casting_types(df)
    print(df.groupby('name')['price'].agg(['count', 'mean']))
    sns.countplot(x=df['restaurant'], palette='Greens')
    plt.savefig('plot.png')
    sns.barplot(x='price', y='restaurant', hue='name', data=df, palette="Greens")
    plt.show()
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
    df['time'] = pd.to_datetime(df['time'])
    return df
