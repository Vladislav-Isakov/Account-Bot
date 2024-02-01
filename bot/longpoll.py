from typing import Optional
from bot.VKApi import VKApi
from bot.custom_enums import VkLongpollMode


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