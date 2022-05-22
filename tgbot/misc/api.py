import aiohttp


class API:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = 'http://127.0.0.1:8000/api/%s'

    async def get(self, request: str):
        url = self.base_url % request
        async with self.session.get(url) as response:
            return await response.json()

    async def post(self, url, data=None):
        async with self.session.post(url, data=data) as response:
            return await response.json()

    async def close(self):
        await self.session.close()
