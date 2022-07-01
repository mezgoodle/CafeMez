import aiohttp

from typing import Tuple


class API:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = 'http://127.0.0.1:8000/api/%s'

    async def get(self, request_url: str) -> dict:
        url = self.base_url % request_url
        async with self.session.get(url) as response:
            return await response.json()

    async def post(self, request_url, data: dict = None, headers: dict = None) -> Tuple[dict, int]:
        url = self.base_url % request_url
        async with self.session.post(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    async def put(self, request_url, data=None) -> dict:
        url = self.base_url % request_url
        async with self.session.put(url, data=data) as response:
            return await response.json()

    async def delete(self, request_url: str, headers: dict = None) -> int:
        url = self.base_url % request_url
        async with self.session.delete(url, headers=headers) as response:
            return response.status

    async def close(self):
        await self.session.close()
