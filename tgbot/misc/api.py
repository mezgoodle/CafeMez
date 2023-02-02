from typing import Tuple, Union

import aiohttp

from tgbot.misc.decorators import api_decorator


class API:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = "http://127.0.0.1:8000/api/%s"

    @api_decorator
    async def get(self, request_url: str) -> Union[dict, list]:
        """Method for HTTP-get method

        Args:
            request_url (str): part of the url

        Returns:
            Union[dict, list]: dict of the object or list of the objects
        """
        url = self.base_url % request_url
        async with self.session.get(url) as response:
            return await response.json()

    @api_decorator
    async def post(
        self, request_url, data: dict = None, headers: dict = None
    ) -> Tuple[dict, int]:
        """Method for HTTP-post method

        Args:
            request_url (_type_): part of the url
            data (dict, optional): data of the new object. Defaults to None.
            headers (dict, optional): some additional headers. Defaults to None.

        Returns:
            Tuple[dict, int]: created object and status
        """
        url = self.base_url % request_url
        async with self.session.post(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    @api_decorator
    async def put(
        self, request_url, data=None, headers: dict = None
    ) -> Tuple[dict, int]:
        """Method for HTTP-put method

        Args:
            request_url (_type_): part of the url
            data (_type_, optional): new data. Defaults to None.
            headers (dict, optional): some additional headers. Defaults to None.

        Returns:
            Tuple[dict, int]: updated object and status
        """
        url = self.base_url % request_url
        async with self.session.patch(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    @api_decorator
    async def delete(self, request_url: str, headers: dict = None) -> int:
        """Method for HTTP-delete method

        Args:
            request_url (str): part of the url
            headers (dict, optional): some additional headers. Defaults to None.

        Returns:
            int: status
        """
        url = self.base_url % request_url
        async with self.session.delete(url, headers=headers) as response:
            return response.status

    async def close(self):
        await self.session.close()
