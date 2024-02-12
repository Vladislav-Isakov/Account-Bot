import ast
import os
from pprint import pprint as print
from bot.VKBot import Bot
from bot.VKApi import VKApi
from config import config

vk_api_session = VKApi(token=config['VK_API_TOKEN'])

test = Bot(base_vk_api=vk_api_session)

@test.command('<test:command>  <int(len=10):name>', prefixes=['-'])
def test_func(hello):
    ...

test.run()

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