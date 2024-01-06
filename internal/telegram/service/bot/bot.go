package bot

import (
	"Registration-Bot/internal/domain"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

//go:generate mockery --name Repository
type Repository interface {
	// SaveAnswer is used to save user's answer
	SaveAnswer(chatID int64, answer string) error
	// GetFinal returns final message of bot
	GetFinal() (string, error)
	// GetQuestion returns current Question using user's saved state
	GetQuestion(chatID int64) (domain.Question, error)

	GetState(chatID int64) (domain.State, error)
	SetState(chatID int64, st domain.State) error
}

//go:generate mockery --name BotAPI
type API interface {
	Send(m tg.Chattable) (tg.Message, error)
}

type Bot struct {
	Stop chan struct{}
	api  API
	log  logrus.FieldLogger
	repo Repository
}

func NewBot(stop chan struct{}, api API, log logrus.FieldLogger,
	repo Repository) *Bot {
	return &Bot{stop, api, log, repo}
}

func (b *Bot) ListenUpdates(updates tg.UpdatesChannel) {
	b.log.Info("Bot started")
	for {
		select {
		case u := <-updates:
			go b.handleUpdate(u)
		case <-b.Stop:
			b.log.Info("Bot stopped")
			return
		}
	}
}
