package bot

import (
	"Registration-Bot/internal/domain"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

//go:generate mockery --name Repository
type Repository interface {
	SaveAnswer(botID int, chatID int64, text string) error
	SetModuleID(botID int, chatID int64, questionID int) error
	GetCurrentModule(botID int, chatID int64) (domain.Module, error)
	SetStage(botID int, chatID int64, stage int) error
	GetFinal(botID int) (string, error)
	AddBot(botID int, journal map[int]domain.Module, final string) error
	GetState(botID int, chatID int64) (domain.State, error)
	SetState(botID int, chatID int64, st domain.State) error
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
		stop:  make(chan struct{}),
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
		//case u := <-updates:
		//	go b.handleUpdate(u)
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
