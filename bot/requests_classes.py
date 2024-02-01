import asyncio
from traceback import TracebackException
from types import TracebackType
from aiohttp import ClientResponse, ClientSession, JsonPayload, ClientTimeout, client_exceptions
from typing import (
    Any,
    Dict,
    Optional,
    Type,
    TypeVar,
)

T = TypeVar("T", bound="AioSession")

class AioSession:
    
    def __init__(self) -> None:
        self._session: ClientSession = ClientSession()

    async def __aenter__(self: T) -> ClientSession:
        return self._session

    async def __aexit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[TracebackException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

class AioLoop:
    
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None, debug: Optional[bool] = None) -> None:
        self._loop = loop
        self.debug = debug
    
    @property
    def loop(self):
        if self._loop is None:
            self.loop = asyncio.new_event_loop()
        return self._loop
    
    @loop.setter
    def loop(self, loop: asyncio.AbstractEventLoop):
        if isinstance(loop, asyncio.AbstractEventLoop):
            if self.debug is not None:
                loop.set_debug(self.debug)
            asyncio.set_event_loop(loop)
            self._loop = loop
        else:
            raise TypeError(f'Ошибка установки цикла событий для ассинхронных задач. Был передан объект {loop!r}, который не является экземпляром AsyncIO: {asyncio.AbstractEventLoop!r}')

class AioRequests:
     
    def __init__(self, session_timeout: Optional[int] = 5) -> None:
        self._session_timeout: ClientTimeout = ClientTimeout(total=session_timeout)
        self._session: AioSession = AioSession()

    async def get(self, url: str):
        async with self._session as session:
            async with session.get(url, timeout=self._session_timeout) as response:
                return await response.json()
    
    async def post(
        self, 
        url: str, 
        data: Optional[str] = None, 
        json: Optional[JsonPayload] = None, 
        headers: Optional[Dict[str, Any]] = None,
    ) -> ClientResponse.json:
        async with self._session as session:
            async with session.post(url, data=data, json=json, headers=headers, timeout=self._session_timeout) as response:
                return await response.json()