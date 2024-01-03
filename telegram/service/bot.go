package service

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

const (
	Unknown = iota
	InProcess
	OnApproval
	Finished
)

//go:generate mockery --name Repository
type Repository interface {
	// SaveAnswer is used to save user's answer
	SaveAnswer(string) error
	// GetStart returns start message of bot
	GetStart(int) (string, error)
	// GetFinal returns final message of bot
	GetFinal(int) (string, error)
	// GetStage returns user's current questionnaire stage
	GetStage(int64) (int, error)
}

type Bot struct {
	api  *tg.BotAPI
	id   int
	log  logrus.FieldLogger
	stop chan struct{}
	repo Repository
}

func (b *Bot) handleMessage(m *tg.Message) (tg.Message, error) {
	panic("not implemented!")
}

func (b *Bot) handleCallback(c *tg.CallbackQuery) (tg.Message, error) {
	panic("not implemented!")
}

func (b *Bot) handleStart(m *tg.Message) (tg.Message, error) {
	text, err := b.repo.GetStart(b.id)
	if err != nil {
		return tg.Message{}, err
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	s, err := b.api.Send(reply)
	return s, err
}

func (b *Bot) handleReset(m *tg.Message) (tg.Message, error) {
	panic("not implemented!")
}

func (b *Bot) handleCommand(m *tg.Message) (tg.Message, error) {
	b.log.WithFields(logrus.Fields{
		"chatID":    m.Chat.ID,
		"messageID": m.MessageID,
		"command":   m.Command(),
	}).Debug("Received command")

	switch m.Command() {
	case "start":
		return b.handleStart(m)
	case "reset":
		return b.handleReset(m)
	default:
		reply := tg.NewMessage(m.Chat.ID, "Неизвестная команда!")
		return b.api.Send(reply)
	}
}

func (b *Bot) listenUpdates(updates tg.UpdatesChannel) {
	b.log.Info("Bot started")
	for {
		var sent tg.Message
		var err error

		select {
		case u := <-updates:
			switch {
			case u.CallbackQuery != nil:
				sent, err = b.handleCallback(u.CallbackQuery)
			case u.Message != nil && u.Message.IsCommand():
				sent, err = b.handleCommand(u.Message)
			case u.Message != nil:
				sent, err = b.handleMessage(u.Message)
			}
		case <-b.stop:
			b.log.Info("Bot stopped")
			return
		}

		if err != nil {
			b.log.Error(err)
		} else {
			b.log.WithFields(logrus.Fields{
				"chatID":    sent.Chat.ID,
				"messageID": sent.MessageID,
			}).Debug("Bot sent message")
		}
	}
}
