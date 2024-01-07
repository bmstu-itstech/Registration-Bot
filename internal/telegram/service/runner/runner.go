package runner

import (
	"Registration-Bot/internal/domain/errors"
	"Registration-Bot/internal/telegram/service/bot"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"sync"
)

type Runner struct {
	wg   *sync.WaitGroup
	bots map[int]chan struct{}
	log  logrus.FieldLogger
	repo bot.Repository
}

func NewRunner(wg *sync.WaitGroup, log logrus.FieldLogger,
	repo bot.Repository) *Runner {
	return &Runner{
		wg:   wg,
		bots: make(map[int]chan struct{}),
	}
}

// StartBot launches bot with provided id and returns error
// if bot starting failed.
func (r *Runner) StartBot(botID int, token string) error {
	api, err := tg.NewBotAPI(token)
	if err != nil {
		return err
	}

	conf := tg.NewUpdate(0)
	conf.Timeout = 60
	updates, err := api.GetUpdatesChan(conf)
	if err != nil {
		return err
	}

	b := bot.NewBot(make(chan struct{}), api, r.log, r.repo)
	r.bots[botID] = b.Stop

	r.wg.Add(1)
	go func() {
		defer r.wg.Done()
		b.ListenUpdates(updates)
	}()

	return nil
}

// StopBot accepts an id of bot and stops the bot with provided
// ID. If bot with provided ID doesn't exist, returns error.
func (r *Runner) StopBot(botID int) error {
	stop, ok := r.bots[botID]
	if !ok {
		return errors.ErrBotNotFound
	}
	stop <- struct{}{}
	close(stop)
	delete(r.bots, botID)
	return nil
}
