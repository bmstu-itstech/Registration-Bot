package grpc

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/proto"
	"context"
	"errors"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
)

type Service interface {
	StartBot(botID int, token string) error
	StopBot(botID int) error
}

// Server is an implementation of proto.BotRunnerServer
type Server struct {
	service Service
	proto.UnimplementedBotRunnerServer
}

func NewServer(s Service) proto.BotRunnerServer {
	return &Server{
		service: s,
	}
}

// StartBot accepts botID, token and log level in request and starts a bot with
// provided parameters.
func (s *Server) StartBot(_ context.Context, req *proto.StartBotRequest) (*emptypb.Empty, error) {
	err := s.service.StartBot(int(req.GetId()), req.GetToken())
	if err != nil && errors.Is(err, domain.ErrBotConflict) {
		return nil, status.Errorf(codes.AlreadyExists, err.Error())
	}
	if err != nil {
		return nil, status.Error(codes.Internal, err.Error())
	}
	return &emptypb.Empty{}, nil
}

// StopBot accepts botID in request and stops the bot with provided ID if it exists.
func (s *Server) StopBot(_ context.Context, req *proto.StopBotRequest) (*emptypb.Empty, error) {
	err := s.service.StopBot(int(req.GetId()))
	if err != nil && errors.Is(err, domain.ErrBotNotFound) {
		return nil, status.Errorf(codes.NotFound, err.Error())
	}
	if err != nil {
		return nil, status.Errorf(codes.Internal, err.Error())
	}
	return &emptypb.Empty{}, nil
}
