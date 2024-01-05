package service

import (
	"Registration-Bot/model"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

//go:generate mockery --name Repository
type Repository interface {
	// SaveAnswer is used to save user's answer
	SaveAnswer(chatID int64, answer string) error
	// GetFinal returns final message of bot
	GetFinal() (string, error)
	// GetQuestion gets current question text
	GetQuestion(chatID int64) (string, error)

	GetState(chatID int64) (model.State, error)
	SetState(chatID int64, st model.State) error
}

type Bot struct {
	api  *tg.BotAPI
	id   int
	log  logrus.FieldLogger
	stop chan struct{}
	repo Repository
}

func (b *Bot) handleFinal(m *tg.Message) (tg.Message, error) {
	panic("not implemented!")
}

func (b *Bot) handleMessage(m *tg.Message) (tg.Message, error) {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}
	switch st.Stage {
	case model.Finished:
		return b.api.Send(tg.NewMessage(m.Chat.ID,
			"Вы уже заполнили анкету!"))
	case model.OnApproval:
		return b.handleFinal(m)
	case model.Unknown:
		return b.handleStart(m)
	}
	return tg.Message{}, err
}

func (b *Bot) handleCallback(c *tg.CallbackQuery) (tg.Message, error) {
	st, err := b.repo.GetState(c.Message.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}
	if st.Stage == model.Finished {
		return b.api.Send(tg.NewMessage(c.Message.Chat.ID,
			"Вы уже заполнили анкету!"))
	}
	return tg.Message{}, err
}

func (b *Bot) handleStart(m *tg.Message) (tg.Message, error) {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}
	switch st.Stage {
	case model.Finished:
		return b.api.Send(tg.NewMessage(m.Chat.ID,
			"Вы уже заполнили анкету!"))
	case model.InProcess:
		return b.api.Send(tg.NewMessage(m.Chat.ID,
			"Вы уже в процессе заполнения анкеты!"))
	case model.OnApproval:
		return b.api.Send(tg.NewMessage(m.Chat.ID,
			"Вы уже в стадии подтверждения анкеты!"))
	}
	err = b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 1,
		Stage:      model.InProcess,
	})
	if err != nil {
		return tg.Message{}, err
	}
	text, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	return b.api.Send(reply)
}

func (b *Bot) handleReset(m *tg.Message) (tg.Message, error) {
	err := b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 0,
		Stage:      model.Unknown,
	})
	if err != nil {
		return tg.Message{}, err
	}
	reply := tg.NewMessage(m.Chat.ID, "Анкета сброшена!")
	return b.api.Send(reply)
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
