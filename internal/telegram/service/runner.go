package service

import (
	"Registration-Bot/internal/model"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"sync"
)

type Runner struct {
	wg   *sync.WaitGroup
	bots map[int]chan struct{}
}

func NewRunner(wg *sync.WaitGroup) *Runner {
	return &Runner{
		wg:   wg,
		bots: make(map[int]chan struct{}),
	}
}

// StartBot launches bot with provided id and returns error
// if bot starting failed.
func (r *Runner) StartBot(logger *logrus.Logger, repo Repository,
	botID int, token string) error {
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

	bot := &Bot{
		api:  api,
		log:  logger.WithField("botID", botID),
		stop: make(chan struct{}),
		repo: repo,
	}

	r.bots[botID] = bot.stop

	r.wg.Add(1)
	go func() {
		defer r.wg.Done()
		bot.listenUpdates(updates)
	}()

	return nil
}

// StopBot accepts an id of bot and stops the bot with provided
// ID. If bot with provided ID doesn't exist, returns error.
func (r *Runner) StopBot(botID int) error {
	stop, ok := r.bots[botID]
	if !ok {
		return model.ErrBotNotFound
	}
	stop <- struct{}{}
	close(stop)
	delete(r.bots, botID)
	return nil
}
