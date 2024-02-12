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

class VkBotEventType(Enum):
    """
    Типы событий в группах ВК
    Все типы можно посмотреть в документации VK API: (https://dev.vk.com/ru/api/community-events/json-schema#message_new)
    """
    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGE_ALLOW = 'message_allow'
    MESSAGE_DENY = 'message_deny'
    MESSAGE_EVENT = 'message_event'
    MESSAGE_TYPING_STATE = 'message_typing_state'

    PHOTO_NEW = 'photo_new'
    PHOTO_COMMENT_NEW = 'photo_comment_new'
    PHOTO_COMMENT_EDIT = 'photo_comment_edit'
    PHOTO_COMMENT_RESTORE = 'photo_comment_restore'
    PHOTO_COMMENT_DELETE = 'photo_comment_delete'

    AUDIO_NEW = 'audio_new'

    VIDEO_NEW = 'video_new'
    VIDEO_COMMENT_NEW = 'video_comment_new'
    VIDEO_COMMENT_EDIT = 'video_comment_edit'
    VIDEO_COMMENT_RESTORE = 'video_comment_restore'
    VIDEO_COMMENT_DELETE = 'video_comment_delete'

    WALL_POST_NEW = 'wall_post_new'
    WALL_REPOST = 'wall_repost'

    WALL_REPLY_NEW = 'wall_reply_new'
    WALL_REPLY_EDIT = 'wall_reply_edit'
    WALL_REPLY_RESTORE = 'wall_reply_restore'
    WALL_REPLY_DELETE = 'wall_reply_delete'

    LIKE_ADD = 'like_add'
    LIKE_REMOVE = 'like_remove'

    BOARD_POST_NEW = 'board_post_new'
    BOARD_POST_EDIT = 'board_post_edit'
    BOARD_POST_RESTORE = 'board_post_restore'
    BOARD_POST_DELETE = 'board_post_delete'

    MARKET_COMMENT_NEW = 'market_comment_new'
    MARKET_COMMENT_EDIT = 'market_comment_edit'
    MARKET_COMMENT_RESTORE = 'market_comment_restore'
    MARKET_COMMENT_DELETE = 'market_comment_delete'
    MARKET_ORDER_NEW = 'market_order_new'
    MARKET_ORDER_EDIT = 'market_order_edit'

    GROUP_JOIN = 'group_join'
    GROUP_LEAVE = 'group_leave'

    USER_BLOCK = 'user_block'
    USER_UNBLOCK = 'user_unblock'

    POLL_VOTE_NEW = 'poll_vote_new'

    GROUP_OFFICERS_EDIT = 'group_officers_edit'
    GROUP_CHANGE_SETTINGS = 'group_change_settings'
    GROUP_CHANGE_PHOTO = 'group_change_photo'

    VKPAY_TRANSACTION = 'vkpay_transaction'

    APP_PAYLOAD = 'app_payload'

    DONUT_SUBSCRIPTION_CREATE = 'donut_subscription_create'
    DONUT_SUBSCRIPTION_PROLONGED = 'donut_subscription_prolonged'
    DONUT_SUBSCRIPTION_EXPIRED = 'donut_subscription_expired'
    DONUT_SUBSCRIPTION_CANCELLED = 'donut_subscription_cancelled'
    DONUT_SUBSCRIPTION_PRICE_CHANGED = 'donut_subscription_price_changed'
    DONUT_MONEY_WITHDRAW = 'donut_money_withdraw'
    DONUT_MONEY_WITHDRAW_ERROR = 'donut_money_withdraw_error'