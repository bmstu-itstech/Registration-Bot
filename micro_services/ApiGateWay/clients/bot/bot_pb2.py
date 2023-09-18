# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bot.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import clients.bot.base_types_pb2 as base__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tbot.proto\x1a\x10\x62\x61se_types.proto\".\n\rGetBotRequest\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\x05\x12\r\n\x05owner\x18\x02 \x01(\x05\"G\n\x17UpdateBotTgTokenRequest\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\x05\x12\r\n\x05owner\x18\x02 \x01(\x05\x12\r\n\x05token\x18\x03 \x01(\t\"K\n\x1bUpdateBotGoogleTokenRequest\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\x05\x12\r\n\x05owner\x18\x02 \x01(\x05\x12\r\n\x05token\x18\x03 \x01(\t\"\x7f\n\x10\x43reateBotRequest\x12\x11\n\tfrom_user\x18\x01 \x01(\x05\x12\x10\n\x08tg_token\x18\x02 \x01(\t\x12\x14\n\x0csheets_token\x18\x03 \x01(\t\x12\x19\n\x07journal\x18\x04 \x01(\x0b\x32\x08.Journal\x12\x15\n\rstart_message\x18\x05 \x01(\t\"5\n\x10\x44\x65leteBotRequest\x12\x11\n\tfrom_user\x18\x01 \x01(\x05\x12\x0e\n\x06\x62ot_id\x18\x02 \x01(\x05\"9\n\x12GetQuestionRequest\x12\x0e\n\x06\x62ot_id\x18\x01 \x01(\x05\x12\x13\n\x0bquestion_id\x18\x02 \x01(\x05\"h\n\x11SetAnswersRequest\x12\x12\n\ntg_chat_id\x18\x01 \x01(\x03\x12\x0e\n\x06\x62ot_id\x18\x02 \x01(\x05\x12\x18\n\x07\x61nswers\x18\x03 \x03(\x0b\x32\x07.Answer\x12\x15\n\rtelegram_link\x18\x04 \x01(\t\"@\n\x11\x43reateBotResponse\x12\r\n\x05state\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x0e\n\x06\x62ot_id\x18\x03 \x01(\x05\"\x0e\n\x0c\x45mptyRequest2\x8c\x01\n\tBotGetter\x12&\n\x06GetBot\x12\x0e.GetBotRequest\x1a\x0c.BotResponse\x12+\n\x0bGetQuestion\x12\x13.GetQuestionRequest\x1a\x07.Module\x12*\n\nGetAllBots\x12\r.EmptyRequest\x1a\r.BotsResponse2\xa1\x02\n\tBotWorker\x12\x32\n\tCreateBot\x12\x11.CreateBotRequest\x1a\x12.CreateBotResponse\x12-\n\tDeleteBot\x12\x11.DeleteBotRequest\x1a\r.BaseResponse\x12;\n\x10UpdateBotTgToken\x12\x18.UpdateBotTgTokenRequest\x1a\r.BaseResponse\x12\x43\n\x14UpdateBotGoogleToken\x12\x1c.UpdateBotGoogleTokenRequest\x1a\r.BaseResponse\x12/\n\nSetAnswers\x12\x12.SetAnswersRequest\x1a\r.BaseResponseB\x19\xaa\x02\x16\x44\x61taBaseService.Protosb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bot_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\026DataBaseService.Protos'
  _globals['_GETBOTREQUEST']._serialized_start=31
  _globals['_GETBOTREQUEST']._serialized_end=77
  _globals['_UPDATEBOTTGTOKENREQUEST']._serialized_start=79
  _globals['_UPDATEBOTTGTOKENREQUEST']._serialized_end=150
  _globals['_UPDATEBOTGOOGLETOKENREQUEST']._serialized_start=152
  _globals['_UPDATEBOTGOOGLETOKENREQUEST']._serialized_end=227
  _globals['_CREATEBOTREQUEST']._serialized_start=229
  _globals['_CREATEBOTREQUEST']._serialized_end=356
  _globals['_DELETEBOTREQUEST']._serialized_start=358
  _globals['_DELETEBOTREQUEST']._serialized_end=411
  _globals['_GETQUESTIONREQUEST']._serialized_start=413
  _globals['_GETQUESTIONREQUEST']._serialized_end=470
  _globals['_SETANSWERSREQUEST']._serialized_start=472
  _globals['_SETANSWERSREQUEST']._serialized_end=576
  _globals['_CREATEBOTRESPONSE']._serialized_start=578
  _globals['_CREATEBOTRESPONSE']._serialized_end=642
  _globals['_EMPTYREQUEST']._serialized_start=644
  _globals['_EMPTYREQUEST']._serialized_end=658
  _globals['_BOTGETTER']._serialized_start=661
  _globals['_BOTGETTER']._serialized_end=801
  _globals['_BOTWORKER']._serialized_start=804
  _globals['_BOTWORKER']._serialized_end=1093
# @@protoc_insertion_point(module_scope)
