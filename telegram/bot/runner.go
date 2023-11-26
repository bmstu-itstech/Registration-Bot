package bot

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"sync"
)

type Service interface {
}

type Bot struct {
	api     *tg.BotAPI
	stop    chan struct{}
	running bool
}

type Runner struct {
	wg   *sync.WaitGroup
	bots map[int]*Bot
	s    Service
}

func NewRunner(service Service) *Runner {
	return &Runner{
		s: service,
	}
}
