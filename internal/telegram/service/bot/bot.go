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

//go:generate mockery --name API
type API interface {
	Send(m tg.Chattable) (tg.Message, error)
}

type Bot struct {
	stop  chan struct{}
	api   API
	log   logrus.FieldLogger
	repo  Repository
	botID int
}

func NewBot(api API, log logrus.FieldLogger, repo Repository, botID int) *Bot {
	return &Bot{
		api:   api,
		log:   log,
		repo:  repo,
		botID: botID,
	}
}

func (b *Bot) ListenUpdates(updates tg.UpdatesChannel) {
	b.log.Info("Bot started")
	for {
		select {
		case u := <-updates:
			go b.handleUpdate(u)
		case <-b.stop:
			b.log.Info("Bot stopped")
			return
		}
	}
}

func (b *Bot) Stop() {
	b.stop <- struct{}{}
	close(b.stop)
}
