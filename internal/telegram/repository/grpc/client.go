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

func (a *Client) PushAnswers(answers map[int32]string) error {
	_, err := a.cl.SaveAnswers(context.Background(), &proto.AnswersMap{Answers: answers})
	if err != nil {
		return err
	}
	return nil
}
