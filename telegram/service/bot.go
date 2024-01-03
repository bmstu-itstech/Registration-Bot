package service

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

//go:generate mockery --name Repository
type Repository interface {
	// SaveAnswer is used to save user's answer
	SaveAnswer(string) error
	// GetStart returns start message of bot
	GetStart(int) (string, error)
	// GetFinal returns final message of bot
	GetFinal(int) (string, error)
}

type Bot struct {
	*tg.BotAPI
	id   int
	log  logrus.FieldLogger
	stop chan struct{}
	repo Repository
}

func (b *Bot) handleMessage(u *tg.Message) {
	panic("not implemented!")
}

func (b *Bot) handleCallback(u *tg.CallbackQuery) {
	panic("not implemented!")
}

func (b *Bot) handleStart(u *tg.Message) {
	panic("not implemented!")
}

func (b *Bot) handleReset(u *tg.Message) {
	panic("not implemented!")
}

func (b *Bot) handleCommand(u *tg.Message) {
	switch u.Command() {
	case "start":
		b.handleStart(u)
	case "reset":
		b.handleReset(u)
	default:
		m := tg.NewMessage(u.Chat.ID, "Неизвестная команда!")
		_, err := b.Send(m)
		if err != nil {
			b.log.Error(err)
		}
	}
}

func (b *Bot) listenUpdates(updates tg.UpdatesChannel) {
	b.log.Info("Bot started")
	for {
		select {
		case u := <-updates:
			switch {
			case u.CallbackQuery != nil:
				b.handleCallback(u.CallbackQuery)
			case u.Message != nil && u.Message.IsCommand():
				b.handleCommand(u.Message)
			case u.Message != nil:
				b.handleMessage(u.Message)
			}
		case <-b.stop:
			b.log.Info("Bot stopped")
			return
		}
	}
}
