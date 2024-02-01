import requests
import json
import ast
import time
import os
import secrets
from requests.exceptions import Timeout
from datetime import datetime
from sqlalchemy import desc
from pprint import pprint as print
from bot.models import Users
# from app.functions import
# from app.сlasses import
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
from vk_api.utils import get_random_id
import threading
from threading import Thread
from bot.VKBot import Bot

test = Bot()

@test.command('<test:command>  <int(len=10):name>', prefixes=['-'])
def test_func(hello):
    ...

# print('Запуск скрипта...')
# vk_session = vk_api.VkApi(token=config['VK_TOKEN'])
# bot_longpoll = VkBotLongPoll(vk_session, group_id='206209370', wait=25)
# vk_method = vk_session.get_api()

# def api():
#     while True:
#         try:
#             for event in bot_longpoll.listen():
#                 print(event.raw)
#                 print(event.type)
#                 print(event.object)
#                 if event.type == VkBotEventType.MESSAGE_NEW:
#                     vk_method.messages.send(
#                         message='Я живой x2!',
#                         peer_id=event.object['message']['peer_id'],
#                         random_id=get_random_id(),
#                     )
#         except KeyboardInterrupt:
#             pass

# class ThreadWithReturnValue(Thread):
    
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#         self._stop_event = threading.Event()
#         self.daemon = True
#         self.start()

#     def stop(self):
#         self._stop_event.set()

#     def stopped(self):
#         return self._stop_event.is_set()
    
#     def run(self):
#         if self._target is not None:
#             self._return = self._target(*self._args,
#                                                 **self._kwargs)
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return

# Thread_1 = ThreadWithReturnValue(target=api, name='bot_longpoll')
# print(Thread_1.isDaemon)
# print(Thread_1.is_alive())
# print(Thread_1.ident)
# print('Скрипт запущен.')