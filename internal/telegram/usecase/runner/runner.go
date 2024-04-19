package runner

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/telegram/usecase/bot"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

type Runner struct {
	bots map[int]*bot.Bot
	log  logrus.FieldLogger
	repo bot.Repository
}

func NewRunner(log logrus.FieldLogger, repo bot.Repository) *Runner {
	return &Runner{
		bots: make(map[int]*bot.Bot),
		log:  log,
		repo: repo,
	}
}

// StartBot launches bot with provided id and returns error
// if bot starting failed.
func (r *Runner) StartBot(botID int, token string, journal map[int]domain.Module,
	final string) error {
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

	b := bot.NewBot(api, r.log, r.repo, botID)
	r.bots[botID] = b

	go b.ListenUpdates(updates)

	return nil
}

// StopBot accepts an id of bot and stops the bot with provided
// ID. If bot with provided ID doesn't exist, returns error.
func (r *Runner) StopBot(botID int) error {
	b, ok := r.bots[botID]
	if !ok {
		return domain.ErrBotNotFound
	}
	b.Stop()
	delete(r.bots, botID)
	return nil
}
