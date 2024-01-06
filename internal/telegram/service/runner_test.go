package service

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/telegram/service/mocks"
	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
	"sync"
	"testing"
)

func TestStartBotNonexistent(t *testing.T) {
	r := NewRunner(&sync.WaitGroup{})
	err := r.StartBot(logrus.New(), mocks.NewRepository(t), 1,
		"incorrect token")
	assert.Error(t, err)
}

func TestStopBot(t *testing.T) {
	r := NewRunner(&sync.WaitGroup{})
	stop := make(chan struct{})
	r.bots[1] = stop
	go func() { <-stop }()
	err := r.StopBot(1)
	assert.NoError(t, err)
	assert.NotContains(t, r.bots, 1)
}

func TestStopBotNonexistent(t *testing.T) {
	r := NewRunner(&sync.WaitGroup{})
	err := r.StopBot(-1)
	assert.ErrorIs(t, err, domain.ErrBotNotFound)
}
