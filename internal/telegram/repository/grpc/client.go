package grpc

import (
	"Registration-Bot/internal/proto"
	"context"
)

type Client struct {
	cl proto.BotGatewayClient
}

func NewAdapter(cl proto.BotGatewayClient) *Client {
	return &Client{cl: cl}
}

func (a *Client) PushAnswers(answers map[int]string) error {
	reqData := make(map[int32]*proto.Answer)
	for k, v := range answers {
		reqData[int32(k)] = &proto.Answer{Data: &proto.Answer_Text{Text: v}}
	}
	_, err := a.cl.SaveAnswers(context.Background(), &proto.AnswersMap{Answers: reqData})
	if err != nil {
		return err
	}
	return nil
}
