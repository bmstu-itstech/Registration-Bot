// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0
// 	protoc        v3.19.6
// source: proto/bot.proto

package pb

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type GetBotRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	BotId int32 `protobuf:"varint,1,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
	Owner int32 `protobuf:"varint,2,opt,name=owner,proto3" json:"owner,omitempty"`
}

func (x *GetBotRequest) Reset() {
	*x = GetBotRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetBotRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetBotRequest) ProtoMessage() {}

func (x *GetBotRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetBotRequest.ProtoReflect.Descriptor instead.
func (*GetBotRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{0}
}

func (x *GetBotRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

func (x *GetBotRequest) GetOwner() int32 {
	if x != nil {
		return x.Owner
	}
	return 0
}

type UpdateBotTgTokenRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	BotId int32  `protobuf:"varint,1,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
	Owner int32  `protobuf:"varint,2,opt,name=owner,proto3" json:"owner,omitempty"`
	Token string `protobuf:"bytes,3,opt,name=token,proto3" json:"token,omitempty"`
}

func (x *UpdateBotTgTokenRequest) Reset() {
	*x = UpdateBotTgTokenRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UpdateBotTgTokenRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UpdateBotTgTokenRequest) ProtoMessage() {}

func (x *UpdateBotTgTokenRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UpdateBotTgTokenRequest.ProtoReflect.Descriptor instead.
func (*UpdateBotTgTokenRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{1}
}

func (x *UpdateBotTgTokenRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

func (x *UpdateBotTgTokenRequest) GetOwner() int32 {
	if x != nil {
		return x.Owner
	}
	return 0
}

func (x *UpdateBotTgTokenRequest) GetToken() string {
	if x != nil {
		return x.Token
	}
	return ""
}

type UpdateBotGoogleTokenRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	BotId int32  `protobuf:"varint,1,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
	Owner int32  `protobuf:"varint,2,opt,name=owner,proto3" json:"owner,omitempty"`
	Token string `protobuf:"bytes,3,opt,name=token,proto3" json:"token,omitempty"`
}

func (x *UpdateBotGoogleTokenRequest) Reset() {
	*x = UpdateBotGoogleTokenRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UpdateBotGoogleTokenRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UpdateBotGoogleTokenRequest) ProtoMessage() {}

func (x *UpdateBotGoogleTokenRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UpdateBotGoogleTokenRequest.ProtoReflect.Descriptor instead.
func (*UpdateBotGoogleTokenRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{2}
}

func (x *UpdateBotGoogleTokenRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

func (x *UpdateBotGoogleTokenRequest) GetOwner() int32 {
	if x != nil {
		return x.Owner
	}
	return 0
}

func (x *UpdateBotGoogleTokenRequest) GetToken() string {
	if x != nil {
		return x.Token
	}
	return ""
}

type CreateBotRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	FromUser     int32    `protobuf:"varint,1,opt,name=from_user,json=fromUser,proto3" json:"from_user,omitempty"`
	TgToken      string   `protobuf:"bytes,2,opt,name=tg_token,json=tgToken,proto3" json:"tg_token,omitempty"`
	SheetsToken  string   `protobuf:"bytes,3,opt,name=sheets_token,json=sheetsToken,proto3" json:"sheets_token,omitempty"`
	Journal      *Journal `protobuf:"bytes,4,opt,name=journal,proto3" json:"journal,omitempty"`
	StartMessage string   `protobuf:"bytes,5,opt,name=start_message,json=startMessage,proto3" json:"start_message,omitempty"`
	EndMessage   string   `protobuf:"bytes,6,opt,name=end_message,json=endMessage,proto3" json:"end_message,omitempty"`
}

func (x *CreateBotRequest) Reset() {
	*x = CreateBotRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *CreateBotRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*CreateBotRequest) ProtoMessage() {}

func (x *CreateBotRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use CreateBotRequest.ProtoReflect.Descriptor instead.
func (*CreateBotRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{3}
}

func (x *CreateBotRequest) GetFromUser() int32 {
	if x != nil {
		return x.FromUser
	}
	return 0
}

func (x *CreateBotRequest) GetTgToken() string {
	if x != nil {
		return x.TgToken
	}
	return ""
}

func (x *CreateBotRequest) GetSheetsToken() string {
	if x != nil {
		return x.SheetsToken
	}
	return ""
}

func (x *CreateBotRequest) GetJournal() *Journal {
	if x != nil {
		return x.Journal
	}
	return nil
}

func (x *CreateBotRequest) GetStartMessage() string {
	if x != nil {
		return x.StartMessage
	}
	return ""
}

func (x *CreateBotRequest) GetEndMessage() string {
	if x != nil {
		return x.EndMessage
	}
	return ""
}

type DeleteBotRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	FromUser int32 `protobuf:"varint,1,opt,name=from_user,json=fromUser,proto3" json:"from_user,omitempty"`
	BotId    int32 `protobuf:"varint,2,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
}

func (x *DeleteBotRequest) Reset() {
	*x = DeleteBotRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *DeleteBotRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*DeleteBotRequest) ProtoMessage() {}

func (x *DeleteBotRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use DeleteBotRequest.ProtoReflect.Descriptor instead.
func (*DeleteBotRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{4}
}

func (x *DeleteBotRequest) GetFromUser() int32 {
	if x != nil {
		return x.FromUser
	}
	return 0
}

func (x *DeleteBotRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

type GetQuestionRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	BotId      int32 `protobuf:"varint,1,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
	QuestionId int32 `protobuf:"varint,2,opt,name=question_id,json=questionId,proto3" json:"question_id,omitempty"`
}

func (x *GetQuestionRequest) Reset() {
	*x = GetQuestionRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetQuestionRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetQuestionRequest) ProtoMessage() {}

func (x *GetQuestionRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetQuestionRequest.ProtoReflect.Descriptor instead.
func (*GetQuestionRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{5}
}

func (x *GetQuestionRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

func (x *GetQuestionRequest) GetQuestionId() int32 {
	if x != nil {
		return x.QuestionId
	}
	return 0
}

type SetAnswersRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	TgChatId     int64     `protobuf:"varint,1,opt,name=tg_chat_id,json=tgChatId,proto3" json:"tg_chat_id,omitempty"`
	BotId        int32     `protobuf:"varint,2,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
	Answers      []*Answer `protobuf:"bytes,3,rep,name=answers,proto3" json:"answers,omitempty"`
	TelegramLink string    `protobuf:"bytes,4,opt,name=telegram_link,json=telegramLink,proto3" json:"telegram_link,omitempty"`
}

func (x *SetAnswersRequest) Reset() {
	*x = SetAnswersRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[6]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SetAnswersRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SetAnswersRequest) ProtoMessage() {}

func (x *SetAnswersRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[6]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SetAnswersRequest.ProtoReflect.Descriptor instead.
func (*SetAnswersRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{6}
}

func (x *SetAnswersRequest) GetTgChatId() int64 {
	if x != nil {
		return x.TgChatId
	}
	return 0
}

func (x *SetAnswersRequest) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

func (x *SetAnswersRequest) GetAnswers() []*Answer {
	if x != nil {
		return x.Answers
	}
	return nil
}

func (x *SetAnswersRequest) GetTelegramLink() string {
	if x != nil {
		return x.TelegramLink
	}
	return ""
}

type CreateBotResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	State string `protobuf:"bytes,1,opt,name=state,proto3" json:"state,omitempty"`
	Code  int32  `protobuf:"varint,2,opt,name=code,proto3" json:"code,omitempty"`
	BotId int32  `protobuf:"varint,3,opt,name=bot_id,json=botId,proto3" json:"bot_id,omitempty"`
}

func (x *CreateBotResponse) Reset() {
	*x = CreateBotResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[7]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *CreateBotResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*CreateBotResponse) ProtoMessage() {}

func (x *CreateBotResponse) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[7]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use CreateBotResponse.ProtoReflect.Descriptor instead.
func (*CreateBotResponse) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{7}
}

func (x *CreateBotResponse) GetState() string {
	if x != nil {
		return x.State
	}
	return ""
}

func (x *CreateBotResponse) GetCode() int32 {
	if x != nil {
		return x.Code
	}
	return 0
}

func (x *CreateBotResponse) GetBotId() int32 {
	if x != nil {
		return x.BotId
	}
	return 0
}

type EmptyRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *EmptyRequest) Reset() {
	*x = EmptyRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_bot_proto_msgTypes[8]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *EmptyRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*EmptyRequest) ProtoMessage() {}

func (x *EmptyRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_bot_proto_msgTypes[8]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use EmptyRequest.ProtoReflect.Descriptor instead.
func (*EmptyRequest) Descriptor() ([]byte, []int) {
	return file_proto_bot_proto_rawDescGZIP(), []int{8}
}

var File_proto_bot_proto protoreflect.FileDescriptor

var file_proto_bot_proto_rawDesc = []byte{
	0x0a, 0x0f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x62, 0x6f, 0x74, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x1a, 0x16, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x62, 0x61, 0x73, 0x65, 0x5f, 0x74, 0x79,
	0x70, 0x65, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x3c, 0x0a, 0x0d, 0x47, 0x65, 0x74,
	0x42, 0x6f, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x15, 0x0a, 0x06, 0x62, 0x6f,
	0x74, 0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74, 0x49,
	0x64, 0x12, 0x14, 0x0a, 0x05, 0x6f, 0x77, 0x6e, 0x65, 0x72, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05,
	0x52, 0x05, 0x6f, 0x77, 0x6e, 0x65, 0x72, 0x22, 0x5c, 0x0a, 0x17, 0x55, 0x70, 0x64, 0x61, 0x74,
	0x65, 0x42, 0x6f, 0x74, 0x54, 0x67, 0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65,
	0x73, 0x74, 0x12, 0x15, 0x0a, 0x06, 0x62, 0x6f, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01,
	0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74, 0x49, 0x64, 0x12, 0x14, 0x0a, 0x05, 0x6f, 0x77, 0x6e,
	0x65, 0x72, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x6f, 0x77, 0x6e, 0x65, 0x72, 0x12,
	0x14, 0x0a, 0x05, 0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05,
	0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x22, 0x60, 0x0a, 0x1b, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x42,
	0x6f, 0x74, 0x47, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x52, 0x65, 0x71,
	0x75, 0x65, 0x73, 0x74, 0x12, 0x15, 0x0a, 0x06, 0x62, 0x6f, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01,
	0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74, 0x49, 0x64, 0x12, 0x14, 0x0a, 0x05, 0x6f,
	0x77, 0x6e, 0x65, 0x72, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x6f, 0x77, 0x6e, 0x65,
	0x72, 0x12, 0x14, 0x0a, 0x05, 0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09,
	0x52, 0x05, 0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x22, 0xd7, 0x01, 0x0a, 0x10, 0x43, 0x72, 0x65, 0x61,
	0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x1b, 0x0a, 0x09,
	0x66, 0x72, 0x6f, 0x6d, 0x5f, 0x75, 0x73, 0x65, 0x72, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x08, 0x66, 0x72, 0x6f, 0x6d, 0x55, 0x73, 0x65, 0x72, 0x12, 0x19, 0x0a, 0x08, 0x74, 0x67, 0x5f,
	0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x07, 0x74, 0x67, 0x54,
	0x6f, 0x6b, 0x65, 0x6e, 0x12, 0x21, 0x0a, 0x0c, 0x73, 0x68, 0x65, 0x65, 0x74, 0x73, 0x5f, 0x74,
	0x6f, 0x6b, 0x65, 0x6e, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x73, 0x68, 0x65, 0x65,
	0x74, 0x73, 0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x12, 0x22, 0x0a, 0x07, 0x6a, 0x6f, 0x75, 0x72, 0x6e,
	0x61, 0x6c, 0x18, 0x04, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x08, 0x2e, 0x4a, 0x6f, 0x75, 0x72, 0x6e,
	0x61, 0x6c, 0x52, 0x07, 0x6a, 0x6f, 0x75, 0x72, 0x6e, 0x61, 0x6c, 0x12, 0x23, 0x0a, 0x0d, 0x73,
	0x74, 0x61, 0x72, 0x74, 0x5f, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x18, 0x05, 0x20, 0x01,
	0x28, 0x09, 0x52, 0x0c, 0x73, 0x74, 0x61, 0x72, 0x74, 0x4d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65,
	0x12, 0x1f, 0x0a, 0x0b, 0x65, 0x6e, 0x64, 0x5f, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x18,
	0x06, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0a, 0x65, 0x6e, 0x64, 0x4d, 0x65, 0x73, 0x73, 0x61, 0x67,
	0x65, 0x22, 0x46, 0x0a, 0x10, 0x44, 0x65, 0x6c, 0x65, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65,
	0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x1b, 0x0a, 0x09, 0x66, 0x72, 0x6f, 0x6d, 0x5f, 0x75, 0x73,
	0x65, 0x72, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x08, 0x66, 0x72, 0x6f, 0x6d, 0x55, 0x73,
	0x65, 0x72, 0x12, 0x15, 0x0a, 0x06, 0x62, 0x6f, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x02, 0x20, 0x01,
	0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74, 0x49, 0x64, 0x22, 0x4c, 0x0a, 0x12, 0x47, 0x65, 0x74,
	0x51, 0x75, 0x65, 0x73, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12,
	0x15, 0x0a, 0x06, 0x62, 0x6f, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x05, 0x62, 0x6f, 0x74, 0x49, 0x64, 0x12, 0x1f, 0x0a, 0x0b, 0x71, 0x75, 0x65, 0x73, 0x74, 0x69,
	0x6f, 0x6e, 0x5f, 0x69, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x0a, 0x71, 0x75, 0x65,
	0x73, 0x74, 0x69, 0x6f, 0x6e, 0x49, 0x64, 0x22, 0x90, 0x01, 0x0a, 0x11, 0x53, 0x65, 0x74, 0x41,
	0x6e, 0x73, 0x77, 0x65, 0x72, 0x73, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x1c, 0x0a,
	0x0a, 0x74, 0x67, 0x5f, 0x63, 0x68, 0x61, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28,
	0x03, 0x52, 0x08, 0x74, 0x67, 0x43, 0x68, 0x61, 0x74, 0x49, 0x64, 0x12, 0x15, 0x0a, 0x06, 0x62,
	0x6f, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74,
	0x49, 0x64, 0x12, 0x21, 0x0a, 0x07, 0x61, 0x6e, 0x73, 0x77, 0x65, 0x72, 0x73, 0x18, 0x03, 0x20,
	0x03, 0x28, 0x0b, 0x32, 0x07, 0x2e, 0x41, 0x6e, 0x73, 0x77, 0x65, 0x72, 0x52, 0x07, 0x61, 0x6e,
	0x73, 0x77, 0x65, 0x72, 0x73, 0x12, 0x23, 0x0a, 0x0d, 0x74, 0x65, 0x6c, 0x65, 0x67, 0x72, 0x61,
	0x6d, 0x5f, 0x6c, 0x69, 0x6e, 0x6b, 0x18, 0x04, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0c, 0x74, 0x65,
	0x6c, 0x65, 0x67, 0x72, 0x61, 0x6d, 0x4c, 0x69, 0x6e, 0x6b, 0x22, 0x54, 0x0a, 0x11, 0x43, 0x72,
	0x65, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12,
	0x14, 0x0a, 0x05, 0x73, 0x74, 0x61, 0x74, 0x65, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05,
	0x73, 0x74, 0x61, 0x74, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x63, 0x6f, 0x64, 0x65, 0x18, 0x02, 0x20,
	0x01, 0x28, 0x05, 0x52, 0x04, 0x63, 0x6f, 0x64, 0x65, 0x12, 0x15, 0x0a, 0x06, 0x62, 0x6f, 0x74,
	0x5f, 0x69, 0x64, 0x18, 0x03, 0x20, 0x01, 0x28, 0x05, 0x52, 0x05, 0x62, 0x6f, 0x74, 0x49, 0x64,
	0x22, 0x0e, 0x0a, 0x0c, 0x45, 0x6d, 0x70, 0x74, 0x79, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x32, 0x8c, 0x01, 0x0a, 0x09, 0x42, 0x6f, 0x74, 0x47, 0x65, 0x74, 0x74, 0x65, 0x72, 0x12, 0x26,
	0x0a, 0x06, 0x47, 0x65, 0x74, 0x42, 0x6f, 0x74, 0x12, 0x0e, 0x2e, 0x47, 0x65, 0x74, 0x42, 0x6f,
	0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x0c, 0x2e, 0x42, 0x6f, 0x74, 0x52, 0x65,
	0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x2b, 0x0a, 0x0b, 0x47, 0x65, 0x74, 0x51, 0x75, 0x65,
	0x73, 0x74, 0x69, 0x6f, 0x6e, 0x12, 0x13, 0x2e, 0x47, 0x65, 0x74, 0x51, 0x75, 0x65, 0x73, 0x74,
	0x69, 0x6f, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x07, 0x2e, 0x4d, 0x6f, 0x64,
	0x75, 0x6c, 0x65, 0x12, 0x2a, 0x0a, 0x0a, 0x47, 0x65, 0x74, 0x41, 0x6c, 0x6c, 0x42, 0x6f, 0x74,
	0x73, 0x12, 0x0d, 0x2e, 0x45, 0x6d, 0x70, 0x74, 0x79, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74,
	0x1a, 0x0d, 0x2e, 0x42, 0x6f, 0x74, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x32,
	0xa1, 0x02, 0x0a, 0x09, 0x42, 0x6f, 0x74, 0x57, 0x6f, 0x72, 0x6b, 0x65, 0x72, 0x12, 0x32, 0x0a,
	0x09, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x12, 0x11, 0x2e, 0x43, 0x72, 0x65,
	0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x12, 0x2e,
	0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73,
	0x65, 0x12, 0x2d, 0x0a, 0x09, 0x44, 0x65, 0x6c, 0x65, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x12, 0x11,
	0x2e, 0x44, 0x65, 0x6c, 0x65, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x1a, 0x0d, 0x2e, 0x42, 0x61, 0x73, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65,
	0x12, 0x3b, 0x0a, 0x10, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x54, 0x67, 0x54,
	0x6f, 0x6b, 0x65, 0x6e, 0x12, 0x18, 0x2e, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74,
	0x54, 0x67, 0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x0d,
	0x2e, 0x42, 0x61, 0x73, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x43, 0x0a,
	0x14, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x42, 0x6f, 0x74, 0x47, 0x6f, 0x6f, 0x67, 0x6c, 0x65,
	0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x12, 0x1c, 0x2e, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x42, 0x6f,
	0x74, 0x47, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x54, 0x6f, 0x6b, 0x65, 0x6e, 0x52, 0x65, 0x71, 0x75,
	0x65, 0x73, 0x74, 0x1a, 0x0d, 0x2e, 0x42, 0x61, 0x73, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e,
	0x73, 0x65, 0x12, 0x2f, 0x0a, 0x0a, 0x53, 0x65, 0x74, 0x41, 0x6e, 0x73, 0x77, 0x65, 0x72, 0x73,
	0x12, 0x12, 0x2e, 0x53, 0x65, 0x74, 0x41, 0x6e, 0x73, 0x77, 0x65, 0x72, 0x73, 0x52, 0x65, 0x71,
	0x75, 0x65, 0x73, 0x74, 0x1a, 0x0d, 0x2e, 0x42, 0x61, 0x73, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f,
	0x6e, 0x73, 0x65, 0x42, 0x0d, 0x5a, 0x0b, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2f,
	0x70, 0x62, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_proto_bot_proto_rawDescOnce sync.Once
	file_proto_bot_proto_rawDescData = file_proto_bot_proto_rawDesc
)

func file_proto_bot_proto_rawDescGZIP() []byte {
	file_proto_bot_proto_rawDescOnce.Do(func() {
		file_proto_bot_proto_rawDescData = protoimpl.X.CompressGZIP(file_proto_bot_proto_rawDescData)
	})
	return file_proto_bot_proto_rawDescData
}

var file_proto_bot_proto_msgTypes = make([]protoimpl.MessageInfo, 9)
var file_proto_bot_proto_goTypes = []interface{}{
	(*GetBotRequest)(nil),               // 0: GetBotRequest
	(*UpdateBotTgTokenRequest)(nil),     // 1: UpdateBotTgTokenRequest
	(*UpdateBotGoogleTokenRequest)(nil), // 2: UpdateBotGoogleTokenRequest
	(*CreateBotRequest)(nil),            // 3: CreateBotRequest
	(*DeleteBotRequest)(nil),            // 4: DeleteBotRequest
	(*GetQuestionRequest)(nil),          // 5: GetQuestionRequest
	(*SetAnswersRequest)(nil),           // 6: SetAnswersRequest
	(*CreateBotResponse)(nil),           // 7: CreateBotResponse
	(*EmptyRequest)(nil),                // 8: EmptyRequest
	(*Journal)(nil),                     // 9: Journal
	(*Answer)(nil),                      // 10: Answer
	(*BotResponse)(nil),                 // 11: BotResponse
	(*Module)(nil),                      // 12: Module
	(*BotsResponse)(nil),                // 13: BotsResponse
	(*BaseResponse)(nil),                // 14: BaseResponse
}
var file_proto_bot_proto_depIdxs = []int32{
	9,  // 0: CreateBotRequest.journal:type_name -> Journal
	10, // 1: SetAnswersRequest.answers:type_name -> Answer
	0,  // 2: BotGetter.GetBot:input_type -> GetBotRequest
	5,  // 3: BotGetter.GetQuestion:input_type -> GetQuestionRequest
	8,  // 4: BotGetter.GetAllBots:input_type -> EmptyRequest
	3,  // 5: BotWorker.CreateBot:input_type -> CreateBotRequest
	4,  // 6: BotWorker.DeleteBot:input_type -> DeleteBotRequest
	1,  // 7: BotWorker.UpdateBotTgToken:input_type -> UpdateBotTgTokenRequest
	2,  // 8: BotWorker.UpdateBotGoogleToken:input_type -> UpdateBotGoogleTokenRequest
	6,  // 9: BotWorker.SetAnswers:input_type -> SetAnswersRequest
	11, // 10: BotGetter.GetBot:output_type -> BotResponse
	12, // 11: BotGetter.GetQuestion:output_type -> Module
	13, // 12: BotGetter.GetAllBots:output_type -> BotsResponse
	7,  // 13: BotWorker.CreateBot:output_type -> CreateBotResponse
	14, // 14: BotWorker.DeleteBot:output_type -> BaseResponse
	14, // 15: BotWorker.UpdateBotTgToken:output_type -> BaseResponse
	14, // 16: BotWorker.UpdateBotGoogleToken:output_type -> BaseResponse
	14, // 17: BotWorker.SetAnswers:output_type -> BaseResponse
	10, // [10:18] is the sub-list for method output_type
	2,  // [2:10] is the sub-list for method input_type
	2,  // [2:2] is the sub-list for extension type_name
	2,  // [2:2] is the sub-list for extension extendee
	0,  // [0:2] is the sub-list for field type_name
}

func init() { file_proto_bot_proto_init() }
func file_proto_bot_proto_init() {
	if File_proto_bot_proto != nil {
		return
	}
	file_proto_base_types_proto_init()
	if !protoimpl.UnsafeEnabled {
		file_proto_bot_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*GetBotRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UpdateBotTgTokenRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UpdateBotGoogleTokenRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*CreateBotRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*DeleteBotRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[5].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*GetQuestionRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[6].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SetAnswersRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[7].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*CreateBotResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_bot_proto_msgTypes[8].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*EmptyRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_proto_bot_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   9,
			NumExtensions: 0,
			NumServices:   2,
		},
		GoTypes:           file_proto_bot_proto_goTypes,
		DependencyIndexes: file_proto_bot_proto_depIdxs,
		MessageInfos:      file_proto_bot_proto_msgTypes,
	}.Build()
	File_proto_bot_proto = out.File
	file_proto_bot_proto_rawDesc = nil
	file_proto_bot_proto_goTypes = nil
	file_proto_bot_proto_depIdxs = nil
}