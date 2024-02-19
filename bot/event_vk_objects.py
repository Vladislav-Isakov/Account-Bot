from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union


class VkEventActionObject(Enum):
    CHAT_PHOTO_UPDATE = 'chat_photo_update'
    CHAT_PHOTO_REMOVE = 'chat_photo_remove'
    CHAT_CREATE = 'chat_create'
    CHAT_TITLE_UPDATE = 'chat_title_update'
    CHAT_INVITE_USER = 'chat_invite_user'
    CHAT_KICK_USER = 'chat_kick_user'
    CHAT_PIN_MESSAGE = 'chat_pin_message'
    CHAT_UNPIN_MESSAGE = 'chat_unpin_message'
    CHAT_INVITE_USER_BY_LINK = 'chat_invite_user_by_link'

class VkEventActionObjectPhoto(Enum):
    PHOTO_50 = 'photo_50'
    PHOTO_100 = 'photo_100'
    PHOTO_200 = 'photo_200'

class VkTypeButton(Enum):
    TEXT = 'text'
    OPEN_LINK = 'open_link'
    LOCATION = 'location'
    VKPAY = 'vkpay'
    OPEN_APP = 'open_app'
    CALLBACK = 'callback'
    INTENT_SUBSCRIBE = 'intent_subscribe'
    INTENT_UNSUBSCRIBE = 'intent_unsubscribe'

class VkKeyboardButtonColor(Enum):
    DEFAULT = 'default'
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'

@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal["longitude"], Literal["latitude"]], float]) -> 'Coordinates':
        return Coordinates(
            longitude=json_dict.get('longitude', 0),
            latitude=json_dict.get('latitude', 0)
        )

@dataclass(slots=True, frozen=True)
class GeoPlace:
    id: Union[int, None]
    title: Union[str, None]
    latitude: float
    longitude: float
    created: Union[int, None]
    icon: Union[str, None]
    country: Union[str, None]
    city: Union[str, None]

    @staticmethod
    def from_json(json_dict: Dict[str, Any]) -> 'GeoPlace':
        return GeoPlace(
            id=json_dict.get('id', None),
            title=json_dict.get('title', None),
            latitude=json_dict.get('latitude', 0),
            longitude=json_dict.get('longitude', 0),
            created=json_dict.get('created', None),
            icon=json_dict.get('icon', None),
            country=json_dict.get('country', None),
            city=json_dict.get('city', None)
        )
    
@dataclass(slots=True, frozen=True)
class GeoObject:
    type: Union[str, None]
    coordinates: Coordinates
    place: Union[GeoPlace, None]
    showmap: Union[int, None]

    @staticmethod
    def from_json(json_dict: Dict[str, Any]) -> 'GeoObject':
        return GeoObject(
            type=json_dict.get('type', None),
            coordinates=Coordinates.from_json(json_dict.get('coordinates', {})),
            place=GeoPlace.from_json(json_dict.get('place', {})),
            showmap=json_dict.get('showmap', None)
        )

@dataclass(slots=True, frozen=True)
class MessageActionObject:
    type: VkEventActionObject
    member_id: Union[int, str]
    text: Union[str, None]
    email: Union[str, None]
    photo: Union[VkEventActionObjectPhoto, None]

    @staticmethod
    def from_json(json_dict: Dict[str, Any]) -> 'MessageActionObject':
        return MessageActionObject(
            type=VkEventActionObject(json_dict.get('type')),
            member_id=json_dict.get('member_id', 0),
            text=json_dict.get('text', None),
            email=json_dict.get('email', None),
            photo=VkEventActionObjectPhoto(json_dict.get('photo')) if json_dict.get('photo', None) else None
        )
    
@dataclass(slots=True, frozen=True)
class TextButtonObject:
    label: str
    payload: str
    type: str = field(default='text')

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['label'], Literal['payload']], Any]) -> 'TextButtonObject':
        return TextButtonObject(
            label=json_dict.get('label', ''),
            payload=json_dict.get('payload', '')
        )
    
@dataclass(slots=True, frozen=True)
class LinkButtonObject:
    link: str
    label: str
    payload: str
    type: str = field(default='open_link')

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['link'], Literal['label'], Literal['payload']], Any]) -> 'LinkButtonObject':
        return LinkButtonObject(
            link=json_dict.get('link', ''),
            label=json_dict.get('label', ''),
            payload=json_dict.get('payload', '')
        )
@dataclass(slots=True, frozen=True)
class LocationButtonObject:
    payload: str
    type: str = field(default='location')

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['payload']], Any]) -> 'LocationButtonObject':
        return LocationButtonObject(
            payload=json_dict.get('payload', '')
        )
    
@dataclass(slots=True, frozen=True)
class VkpayButtonObject:
    payload: str
    hash: str
    type: str = field(default='vkpay')

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['payload'], Literal['hash']], Any]) -> 'VkpayButtonObject':
        return VkpayButtonObject(
            payload=json_dict.get('payload', ''),
            hash=json_dict.get('hash', '')
        )
    
@dataclass(slots=True, frozen=True)
class AppButtonObject:
    app_id: int
    owner_id: int
    payload: str
    label: str
    hash: str
    type: str = field(default='open_app')
    
    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['app_id'], Literal['owner_id'], Literal['payload'], Literal['label'], Literal['hash']], Any]) -> 'AppButtonObject':
        return AppButtonObject(
            app_id=json_dict.get('app_id', 0),
            owner_id=json_dict.get('owner_id', 0),
            payload=json_dict.get('payload', ''),
            label=json_dict.get('label', ''),
            hash=json_dict.get('hash', '')
        )
@dataclass(slots=True, frozen=True)
class CallbackButtonObject:
    label: str
    payload: str
    type: str = field(default='callback')

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['label'], Literal['payload']], Any]) -> 'CallbackButtonObject':
        return CallbackButtonObject(
            label=json_dict.get('label', ''),
            payload=json_dict.get('payload', '')
        )

@dataclass(slots=True, frozen=True)
class KeyboardButtonObject:
    action: Union[TextButtonObject, LinkButtonObject, LocationButtonObject, VkpayButtonObject, AppButtonObject, CallbackButtonObject]
    color: VkKeyboardButtonColor

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal['action'], Literal['color'], str], Any]) -> 'KeyboardButtonObject':

        DICT_ACTION_OBJECT = {
            'text': TextButtonObject,
            'open_link': LinkButtonObject,
            'location': LocationButtonObject,
            'vkpay': VkpayButtonObject,
            'open_app': AppButtonObject,
            'callback': CallbackButtonObject
        }
        if DICT_ACTION_OBJECT.get(json_dict['action']['type'], None) is None:
            raise TypeError(f"Не найден объект кнопки VK, с типом {json_dict['action']['type']}, возможно вы установили слишком высокую версию LongPoll API.")
        
        return KeyboardButtonObject(
            action=DICT_ACTION_OBJECT[json_dict['action']['type']].from_json(json_dict['action']),
            color=VkKeyboardButtonColor(json_dict.get('color'))
        )
@dataclass(slots=True, frozen=True)
class KeyboardObject:
    one_time: bool
    buttons: List[List[KeyboardButtonObject]]
    author_id: Union[int, None]
    inline: bool

    @staticmethod
    def from_json(json_dict: Dict[Union[Literal["one_time"], Literal["inline"], Literal["buttons"], str], Any]) -> 'KeyboardObject':
        return KeyboardObject(
            one_time=json_dict['one_time'],
            buttons=[[KeyboardButtonObject.from_json(button) for button in row_of_buttons] for row_of_buttons in json_dict['buttons']],
            author_id=json_dict.get('author_id', None),
            inline=json_dict['inline']
        )
@dataclass(slots=True, frozen=True)
class MessageObject:
    """
    Датакласс описывает объект личных сообщений, описание доступно в документации (https://dev.vk.com/ru/reference/objects/message). \n
    Если у переменной-атрибута в полученном вами объекте установлено значение None, это означает что данного объекта не обнаружено в полученном событии от LongPoll VK. \n
    None означает что данная переменная-атрибут НЕ всегда будет содержать данные или какое-либо значение, это значит что переменная "плавающая". \n
    :meth:`None` - это не значение от LongPoll VK, это значение :meth:`исключительно для различных проверок if...else/match...case`.
    """
    id: int
    out: int
    version: int
    date: int
    peer_id: int
    from_id: int
    text: Union[str, None]
    random_id: int
    ref: Union[str, None]
    ref_source: Union[str, None]
    attachments: List[Dict[str, Any]]
    important: bool
    is_hidden: bool
    is_unavailable: bool
    geo: Union[GeoObject, None]
    payload: Union[str, None]
    keyboard: Union[KeyboardObject, None]
    fwd_messages: List[Dict[str, Any]]
    reply_message: Union[List[Dict[str, Any]], None] # не описан объект сообщения
    action: Union[MessageActionObject, None]
    admin_author_id: Union[int, None]
    conversation_message_id: str
    is_cropped: Union[bool, None]
    members_count: Union[int, None]
    update_time: Union[int, None]
    was_listened: Union[bool, None]
    pinned_at: Union[int, None]
    message_tag: Union[str, None]
    is_mentioned_user: Union[bool, None]
    
    @staticmethod
    def from_json(json_dict: Dict[str, Any]) -> 'MessageObject':

        id = json_dict.get('id', None)
        out = json_dict.get('out', None)
        version = json_dict.get('version', None)
        date = json_dict.get('date', None)
        peer_id = json_dict.get('peer_id', None)
        from_id = json_dict.get('from_id', None)
        text = json_dict.get('text', None)
        random_id = json_dict.get('random_id', None)
        ref = json_dict.get('ref', None)
        ref_source = json_dict.get('ref_source', None)
        attachments = json_dict.get('attachments', [])
        important = json_dict.get('important', None)
        geo = GeoObject.from_json(json_dict.get('geo', {})) if json_dict.get('geo', None) else None
        payload = json_dict.get('payload', None)
        keyboard = KeyboardObject.from_json(json_dict.get('keyboard', {})) if json_dict.get('keyboard', None) else None
        fwd_messages = json_dict.get('fwd_messages', [])
        is_hidden = json_dict.get('is_hidden', None)
        is_unavailable = json_dict.get('is_unavailable', None)
        reply_message = json_dict.get('reply_message', None)
        action = MessageActionObject.from_json(json_dict.get('action', {})) if json_dict.get('action', None) else None
        admin_author_id = json_dict.get('admin_author_id', None)
        conversation_message_id = json_dict.get('conversation_message_id', None)
        is_cropped = json_dict.get('is_cropped', None)
        members_count = json_dict.get('members_count', None)
        update_time = json_dict.get('update_time', None)
        was_listened = json_dict.get('was_listened', None)
        pinned_at = json_dict.get('pinned_at', None)
        message_tag = json_dict.get('message_tag', None)
        is_mentioned_user = json_dict.get('is_mentioned_user', None)

        return MessageObject(
            id=id,
            out=out,
            version=version,
            date=date,
            peer_id=peer_id,
            from_id=from_id,
            text=text,
            random_id=random_id,
            ref=ref,
            ref_source=ref_source,
            attachments=attachments,
            important=important,
            is_hidden=is_hidden,
            is_unavailable=is_unavailable,
            geo=geo,
            payload=payload,
            keyboard=keyboard,
            fwd_messages=fwd_messages,
            reply_message=reply_message,
            action=action,
            admin_author_id=admin_author_id,
            conversation_message_id=conversation_message_id,
            is_cropped=is_cropped,
            members_count=members_count,
            update_time=update_time,
            was_listened=was_listened,
            pinned_at=pinned_at,
            message_tag=message_tag,
            is_mentioned_user=is_mentioned_user
        )
        
@dataclass(slots=True, frozen=True)
class ClientInfo:
    """
    :var keyboard: Доступна ли клавиатура пользователю
    """
    button_actions: Union[List[VkTypeButton], List]
    keyboard: bool # Доступна ли клавиатура пользователю
    inline_keyboard: bool
    carousel: bool
    lang_id: int
    """
    :var keyboard: Доступна ли клавиатура пользователю
    """

    @staticmethod
    def from_json(json_dict: Dict[str, Any]) -> 'ClientInfo':
        return ClientInfo(
            button_actions=json_dict.get('button_actions', []),
            keyboard=json_dict.get('keyboard', False),
            inline_keyboard=json_dict.get('inline_keyboard', False),
            carousel=json_dict.get('carousel', False),
            lang_id=json_dict.get('lang_id', 0)
        )

@dataclass(slots=True, frozen=True)
class NewMessageEvent:
    message: MessageObject
    client_info: ClientInfo

    @staticmethod
    def get_object_event(json_object: Dict[str, Any]) -> 'NewMessageEvent':
        return NewMessageEvent(
            message=MessageObject.from_json(json_object['message']),
            client_info=ClientInfo.from_json(json_object['client_info'])
        )