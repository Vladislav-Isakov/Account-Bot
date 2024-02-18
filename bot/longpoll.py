import asyncio
from typing import Any, Dict, List, Optional, Union
from bot.VKApi import VKApi
from bot.custom_enums import VkLongpollMode, VkBotEventType, VkBotEventContext
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bot.event_vk_objects import NewMessageEvent
from bot.requests_classes import AioRequests
# from pympler.asizeof import asized

@dataclass(slots=True, frozen=True)
class VkBotEvent:
    group_id: int
    raw_event: List[Dict[str, Any]]
    event_type: Union[VkBotEventType, str]
    event_context: VkBotEventContext
    event_object: Dict[str, Any]
    event_id: str
    v: str

class VkLongPoll(ABC):

    @abstractmethod
    def update_longpoll(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def _parse_event(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def listen_longpoll(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def get_event(self):
        """"""
        raise NotImplementedError

class VKUserLongpoll(VkLongPoll):

    def __init__(self, base_vk_api: Optional[VKApi] = None, longpoll_wait: int = 25, longpoll_mode: VkLongpollMode = VkLongpollMode.GET_PTS, longpoll_version: int = 3) -> None:
        self._api = base_vk_api
        self._wait = longpoll_wait
        self._mode = longpoll_mode
        self._version = longpoll_version

        self._key = None
        self._server = None
        self._ts = None
        self._pts = None
    
    def update_longpoll(self, update_ts: bool = True):
        pass

    def _parse_event(self):
        pass

    def get_event(self):
        pass

    def listen_longpoll(self):
        while True:
            for event in self.get_event():
                yield event


CONVERSATION_START_ID = int(2E9)

class VkBotParseEvent:

    def __init__(self, raw_event) -> None:
        self.raw = raw_event

    def _parse_event_type(self) -> Union[VkBotEventType, str]:
        try:
            event_type = VkBotEventType(self.raw['type'])
        except ValueError:
            event_type = self.raw['type']
        return event_type
    
    def _parse_event_context(self) -> VkBotEventContext:

        try:
            if self.raw['object'].get('message', None) is not None:
                peer_id = self.raw['object']['message']['peer_id']
            else:
                peer_id = self.raw['object']['peer_id']
        except KeyError:
            peer_id = -1

        if peer_id < 0:
            context_type = 'group_event'
        elif peer_id < CONVERSATION_START_ID:
            context_type = 'private_messages_event'
        else:
            context_type = 'conversation_event'

        return VkBotEventContext(context_type)

    def get_vk_event(self) -> VkBotEvent:
        
        DICT_OF_EVENT_OBJECTS = {
            VkBotEventType.MESSAGE_NEW.value: NewMessageEvent
        }

        _event_type = self._parse_event_type()
        _event_context = self._parse_event_context()

        if DICT_OF_EVENT_OBJECTS.get(self.raw['type'], None) is not None:
            _event_object = DICT_OF_EVENT_OBJECTS.get(self.raw['type'])
        else:
            raise KeyError(f"Возникла ошибка поиска объекта события с типом {self.raw['type']}, по всей видимости объект события не был описан.")

        return VkBotEvent(
            raw_event=self.raw,
            event_type=_event_type,
            event_context=_event_context,
            event_object=_event_object.get_object_event(self.raw['object']),
            group_id=self.raw['group_id'],
            event_id=self.raw['event_id'],
            v=self.raw['v']
            )

class VkBotLongPoll(VkLongPoll):

    def __init__(self, *, base_vk_api: VKApi, vk_group_id: Optional[int] = None, longpoll_wait: int = 25) -> None:
        self._api = base_vk_api
        self._group_id = vk_group_id
        self._wait = longpoll_wait
        self._aio_http = AioRequests

        self._key = None
        self._server = None
        self._ts = None

        self.update_longpoll()
        self.get_event()

    def update_longpoll(self, update_ts: bool = True):
        if not all((self._api, self._group_id)):
            raise ValueError('Ошибка обновления VKBotLongpoll, были переданы невалидные аргументы base_vk_api или group_id.')
        
        values = {
            'group_id': self._group_id
        }
        
        request = self._api._method('groups.getLongPollServer', values)

        loop = asyncio.get_event_loop()
        task_response = loop.create_task(request)

        response = loop.run_until_complete(task_response)['response']

        self._key = response['key']
        self._server = response['server']

        if update_ts:
            self._ts = response['ts']

    def _parse_event(self, raw_event):

        bot_event = VkBotParseEvent(raw_event=raw_event)

        return bot_event.get_vk_event()

    async def get_update_longpoll(self, server, values):

        response = await self._aio_http(session_timeout=self._wait + 10).get(
            server,
            params=values
        )

        return response

    def get_event(self):
        values = {
            'act': 'a_check',
            'key': self._key,
            'ts': self._ts,
            'wait': self._wait,
        }

        loop = asyncio.get_event_loop()

        task_response = loop.create_task(self.get_update_longpoll(self._server, values))
        try:
            response = loop.run_until_complete(task_response)
        except:
            pass

        if 'failed' not in response:

            self.ts = response['ts']

            return [
                self._parse_event(vk_event)
                for vk_event in response['updates']
            ]

        elif response['failed'] == 1:
            self._ts = response['ts']

        elif response['failed'] == 2:
            self.update_longpoll(update_ts=False)

        elif response['failed'] == 3:
            self.update_longpoll()

        return []

    def listen_longpoll(self):
        while True:
            for event in self.get_event():
                yield event