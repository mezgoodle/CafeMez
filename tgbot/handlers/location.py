from aiogram.types import Message, ContentType
from aiogram.utils.markdown import hlink

from tgbot.misc.calc_distance import choose_shortest
from loader import dp


@dp.message_handler(content_types=ContentType.LOCATION)
async def nearest_restaurants(message: Message) -> Message:
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    closest_restaurants = choose_shortest(location)
    text_format = "Назва: {name}. {url}\nВідстань до нього: {distance:.1f} км."
    text = '\n\n'.join(
        [
            text_format.format(name=name, url=hlink('Google', url), distance=distance)
            for name, distance, url, location in closest_restaurants
        ]
    )
    await message.answer(f'Дякую!\n'
                         f'Ваші координати: {latitude}, {longitude}\n\n'
                         f'{text}',
                         disable_web_page_preview=True)
    for name, distance, url, location in closest_restaurants:
        await message.answer_location(location['lat'], location['lot'])
    return await message.answer('Скористатйтеся посилання на Google карти')
