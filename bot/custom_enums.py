from enum import IntEnum, Enum

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

class VKTypeLongpoll(Enum):
    """
    Тип longpoll событий, который будет получать система.
    User Long Poll API: (https://dev.vk.com/ru/api/user-long-poll/getting-started)
    Bots Long Poll API: (https://dev.vk.com/ru/api/bots-long-poll/getting-started)
    """
    USER = 'user'
    GROUP = 'group'
