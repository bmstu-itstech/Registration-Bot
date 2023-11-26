package bot

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"sync"
)

type Repository interface {
}

type Bot struct {
	api     *tg.BotAPI
	stop    chan struct{}
	running bool
}

type Runner struct {
	wg   *sync.WaitGroup
	bots map[int]*Bot
	repo Repository
}

func NewRunner(wg *sync.WaitGroup, repo Repository) *Runner {
	return &Runner{
		wg:   wg,
		bots: make(map[int]*Bot),
		repo: repo,
	}
}
