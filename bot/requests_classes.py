import asyncio
from traceback import TracebackException
from types import TracebackType
from aiohttp import ClientSession, JsonPayload, ClientTimeout
from typing import (
    Optional,
    NoReturn,
)
from config import config

class AioSession:

    def __init__(self) -> None:
        self._session: ClientSession = self.get_session()

    @staticmethod
    def get_session() -> ClientSession:
        if 'aio_session' not in config:
            config['aio_session'] = ClientSession()
        return config['aio_session']

    async def __aenter__(self) -> "AioSession":
        return self._session

    async def __aexit__(
        self,
        exc_type: Optional[Exception],
        exc_val: Optional[TracebackException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    
    async def close(self) -> None:
        await self._session.close()

class AioRequests:
     
    def __init__(self, timeout: Optional[int] = 5) -> None:
        # if 'aio_loop' not in config:
        #     loop = asyncio.new_event_loop()
        #     asyncio.set_event_loop(loop)
        #     config['aio_loop'] = loop
        # else:
        #     loop = config['aio_loop']
        self._timeout: ClientTimeout = ClientTimeout(total=timeout)
        self._session: AioSession = AioSession()

    async def get(self, url: str):
        async with self._session as session:
            async with session.get(url, timeout=self._timeout) as response:
                return await response.text()
    
    async def post(self, url: str, json: Optional[JsonPayload]):
        return

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    html = await AioRequests().get('https://dev.vk.com')
    # print(html)

asyncio.run(main())