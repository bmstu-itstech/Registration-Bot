from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Answer(_message.Message):
    __slots__ = ["answer_text", "module_id"]
    ANSWER_TEXT_FIELD_NUMBER: _ClassVar[int]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    answer_text: str
    module_id: int
    def __init__(self, module_id: _Optional[int] = ..., answer_text: _Optional[str] = ...) -> None: ...

class BaseResponse(_message.Message):
    __slots__ = ["code", "state"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    code: int
    state: str
    def __init__(self, state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...

class BotResponse(_message.Message):
    __slots__ = ["bot_survey_id", "code", "google_token", "id", "owner", "state", "tg_token"]
    BOT_SURVEY_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TG_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_survey_id: int
    code: int
    google_token: str
    id: int
    owner: int
    state: str
    tg_token: str
    def __init__(self, id: _Optional[int] = ..., tg_token: _Optional[str] = ..., google_token: _Optional[str] = ..., owner: _Optional[int] = ..., bot_survey_id: _Optional[int] = ..., state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...

class Button(_message.Message):
    __slots__ = ["answer_text", "next_question_id", "question_id"]
    ANSWER_TEXT_FIELD_NUMBER: _ClassVar[int]
    NEXT_QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    answer_text: str
    next_question_id: int
    question_id: int
    def __init__(self, question_id: _Optional[int] = ..., answer_text: _Optional[str] = ..., next_question_id: _Optional[int] = ...) -> None: ...

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

class Module(_message.Message):
    __slots__ = ["answer_type", "buttons", "id", "next_question_id", "question", "question_type", "title"]
    ANSWER_TYPE_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    QUESTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    answer_type: str
    buttons: _containers.RepeatedCompositeFieldContainer[Button]
    id: int
    next_question_id: int
    question: str
    question_type: str
    title: str
    def __init__(self, question: _Optional[str] = ..., question_type: _Optional[str] = ..., answer_type: _Optional[str] = ..., title: _Optional[str] = ..., buttons: _Optional[_Iterable[_Union[Button, _Mapping]]] = ..., next_question_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["contact", "description", "title"]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    contact: str
    description: str
    title: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ["code", "contact", "description", "state", "title"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    code: int
    contact: str
    description: str
    state: str
    title: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., contact: _Optional[str] = ..., state: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...
