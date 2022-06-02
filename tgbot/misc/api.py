import aiohttp


class API:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = 'http://127.0.0.1:8000/api/%s'

    async def get(self, request_url: str):
        url = self.base_url % request_url
        async with self.session.get(url) as response:
            return await response.json()

    async def post(self, request_url, data=None):
        url = self.base_url % request_url
        async with self.session.post(url, data=data) as response:
            return await response.json()

    async def put(self, url, data=None):
        async with self.session.put(url, data=data) as response:
            return await response.json()

    async def close(self):
        await self.session.close()
