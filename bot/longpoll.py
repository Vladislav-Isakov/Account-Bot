from typing import Optional
from bot.VKApi import VKApi
from enum import IntEnum

class VkLongpollMode(IntEnum):
    """
    Дополнительные параметры, для получения расширенных данных в событиях.
    Документация: (https://dev.vk.com/ru/api/user-long-poll/getting-started)
    """
    # получать вложения
    ATTACHMENTS = 2
    # возвращать расширенный набор событий
    EXTENDED_SET_OF_EVENTS = 16
    # возвращать pts (это требуется для работы метода messages.getLongPollHistory без ограничения в 256 последних событий)
    GET_PTS = 32
    # в событии с кодом 8 (друг стал онлайн) возвращать дополнительные данные в поле $extra 
    # (смотрите https://dev.vk.com/ru/api/user-long-poll/getting-started#Структура%20событий)
    ADDITIONAL_DATA_EXTRA = 64
    # возвращать поле random_id 
    # (random_id может быть передан при отправке сообщения методом https://dev.vk.com/ru/method/messages.send).
    RETURN_THE_RANDOM_ID_FIELD = 128

class VKUserLongpoll:

    def __init__(self, base_vk_api: Optional[VKApi] = None, longpoll_wait: int = 25, longpoll_mode: VkLongpollMode = VkLongpollMode.GET_PTS, longpoll_version: int = 3) -> None:
        self.api = base_vk_api
        self.wait = longpoll_wait
        self.mode = longpoll_mode
        self.version = longpoll_version

        self.url = None
        self.key = None
        self.server = None
        self.ts = None
        self.pts = None
    
    def update_longpoll(self, update_ts: bool = True):
        pass



class VkBotLongPoll:

    def __init__(self) -> None:
        pass