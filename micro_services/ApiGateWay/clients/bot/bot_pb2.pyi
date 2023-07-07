import my_types.base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateBotRequest(_message.Message):
    __slots__ = ["from_user", "journal", "sheets_token", "tg_token"]
    FROM_USER_FIELD_NUMBER: _ClassVar[int]
    JOURNAL_FIELD_NUMBER: _ClassVar[int]
    SHEETS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TG_TOKEN_FIELD_NUMBER: _ClassVar[int]
    from_user: int
    journal: _base_types_pb2.Journal
    sheets_token: str
    tg_token: str
    def __init__(self, from_user: _Optional[int] = ..., tg_token: _Optional[str] = ..., sheets_token: _Optional[str] = ..., journal: _Optional[_Union[_base_types_pb2.Journal, _Mapping]] = ...) -> None: ...

class CreateBotResponse(_message.Message):
    __slots__ = ["bot_id", "code", "state"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    code: int
    state: str
    def __init__(self, state: _Optional[str] = ..., code: _Optional[int] = ..., bot_id: _Optional[int] = ...) -> None: ...

class DeleteBotRequest(_message.Message):
    __slots__ = ["bot_id", "from_user"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_USER_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    from_user: int
    def __init__(self, from_user: _Optional[int] = ..., bot_id: _Optional[int] = ...) -> None: ...

class GetBotRequest(_message.Message):
    __slots__ = ["bot_id", "owner"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    owner: int
    def __init__(self, bot_id: _Optional[int] = ..., owner: _Optional[int] = ...) -> None: ...

class GetQuestionRequest(_message.Message):
    __slots__ = ["bot_id", "question_id"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    question_id: int
    def __init__(self, bot_id: _Optional[int] = ..., question_id: _Optional[int] = ...) -> None: ...

class SetAnswersRequest(_message.Message):
    __slots__ = ["answers", "bot_id", "tg_chat_id"]
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    TG_CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    answers: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.Answer]
    bot_id: int
    tg_chat_id: int
    def __init__(self, tg_chat_id: _Optional[int] = ..., bot_id: _Optional[int] = ..., answers: _Optional[_Iterable[_Union[_base_types_pb2.Answer, _Mapping]]] = ...) -> None: ...

class UpdateBotGoogleTokenRequest(_message.Message):
    __slots__ = ["bot_id", "owner", "token"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    owner: int
    token: str
    def __init__(self, bot_id: _Optional[int] = ..., owner: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class UpdateBotTgTokenRequest(_message.Message):
    __slots__ = ["bot_id", "owner", "token"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    owner: int
    token: str
    def __init__(self, bot_id: _Optional[int] = ..., owner: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...
