package service

import (
	"Registration-Bot/model"
	"github.com/stretchr/testify/assert"
	"sync"
	"testing"
)

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
	assert.ErrorIs(t, err, model.ErrBotNotFound)
}
