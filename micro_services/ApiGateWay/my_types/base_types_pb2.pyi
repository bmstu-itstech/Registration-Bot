from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BaseResponse(_message.Message):
    __slots__ = ["state", "code"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    state: str
    code: int
    def __init__(self, state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...

class BotResponse(_message.Message):
    __slots__ = ["id", "tg_token", "google_token", "owner", "bot_survey_id", "start_message", "state", "code"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TG_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    BOT_SURVEY_ID_FIELD_NUMBER: _ClassVar[int]
    START_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    id: int
    tg_token: str
    google_token: str
    owner: int
    bot_survey_id: int
    start_message: str
    state: str
    code: int
    def __init__(self, id: _Optional[int] = ..., tg_token: _Optional[str] = ..., google_token: _Optional[str] = ..., owner: _Optional[int] = ..., bot_survey_id: _Optional[int] = ..., start_message: _Optional[str] = ..., state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...

class BotsResponse(_message.Message):
    __slots__ = ["bots"]
    BOTS_FIELD_NUMBER: _ClassVar[int]
    bots: _containers.RepeatedCompositeFieldContainer[BotResponse]
    def __init__(self, bots: _Optional[_Iterable[_Union[BotResponse, _Mapping]]] = ...) -> None: ...

class Module(_message.Message):
    __slots__ = ["question", "answer_type", "title", "buttons", "next_id"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_ID_FIELD_NUMBER: _ClassVar[int]
    question: str
    answer_type: str
    title: str
    buttons: _containers.RepeatedCompositeFieldContainer[Button]
    next_id: int
    def __init__(self, question: _Optional[str] = ..., answer_type: _Optional[str] = ..., title: _Optional[str] = ..., buttons: _Optional[_Iterable[_Union[Button, _Mapping]]] = ..., next_id: _Optional[int] = ...) -> None: ...

class Answer(_message.Message):
    __slots__ = ["module_id", "answer"]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    module_id: int
    answer: str
    def __init__(self, module_id: _Optional[int] = ..., answer: _Optional[str] = ...) -> None: ...

class Journal(_message.Message):
    __slots__ = ["modules"]
    class ModulesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Module
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Module, _Mapping]] = ...) -> None: ...
    MODULES_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.MessageMap[int, Module]
    def __init__(self, modules: _Optional[_Mapping[int, Module]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["title", "description", "contact"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    contact: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class Button(_message.Message):
    __slots__ = ["answer", "next_id"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    NEXT_ID_FIELD_NUMBER: _ClassVar[int]
    answer: str
    next_id: int
    def __init__(self, answer: _Optional[str] = ..., next_id: _Optional[int] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ["title", "description", "contact", "state", "code"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    contact: str
    state: str
    code: int
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., contact: _Optional[str] = ..., state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...
