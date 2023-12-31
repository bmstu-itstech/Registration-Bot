package service

import (
	"Registration-Bot/model"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"sync"
)

type Repository interface {
}

type Runner struct {
	*sync.WaitGroup
	bots map[int]chan struct{}
	repo Repository
}

func NewRunner(wg *sync.WaitGroup, repo Repository) *Runner {
	return &Runner{
		WaitGroup: wg,
		bots:      make(map[int]chan struct{}),
		repo:      repo,
	}
}

// StartBot launches bot with provided id and returns error
// if bot starting failed.
func (r *Runner) StartBot(logger *logrus.Logger, botID int, token string) error {
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
		BotAPI: api,
		id:     botID,
		log:    logger.WithField("botID", botID),
		stop:   make(chan struct{}),
	}

	r.bots[botID] = bot.stop

	r.Add(1)
	go func() {
		defer r.Done()
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
	return nil
}
