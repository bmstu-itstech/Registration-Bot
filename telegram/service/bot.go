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

func (b *Bot) handleMessage(m *tg.Message) {
	panic("not implemented!")
}

func (b *Bot) handleCallback(c *tg.CallbackQuery) {
	panic("not implemented!")
}

func (b *Bot) handleStart(m *tg.Message) {
	text, err := b.repo.GetStart(b.id)
	if err != nil {
		b.log.Error(err)
		return
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	s, err := b.Send(reply)
	if err != nil {
		b.log.Error(err)
		return
	}
	b.log.WithFields(logrus.Fields{
		"chatID":    s.Chat.ID,
		"messageID": s.MessageID,
	}).Debug("Bot sent message")
}

func (b *Bot) handleReset(m *tg.Message) {
	panic("not implemented!")
}

func (b *Bot) handleCommand(m *tg.Message) {
	b.log.WithFields(logrus.Fields{
		"chatID":    m.Chat.ID,
		"messageID": m.MessageID,
		"command":   m.Command(),
	}).Debug("Received command")

	switch m.Command() {
	case "start":
		b.handleStart(m)
	case "reset":
		b.handleReset(m)
	default:
		m := tg.NewMessage(m.Chat.ID, "Неизвестная команда!")
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
