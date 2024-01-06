package service

import (
	"Registration-Bot/model"
	"fmt"
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
	GetQuestion(chatID int64) (model.Question, error)

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

func (b *Bot) sendFinal(send chan tg.Chattable, m *tg.Message) error {
	err := b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 0,
		Stage:      model.Finished,
	})
	if err != nil {
		return err
	}
	text, err := b.repo.GetFinal()
	if err != nil {
		return err
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	send <- reply
	return nil
}

func (b *Bot) sendQuestion(send chan tg.Chattable, m *tg.Message) error {
	q, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		return err
	}

	if q.Rhetorical {
		reply := tg.NewMessage(m.Chat.ID, q.Text)
		send <- reply
		err = b.repo.SetState(m.Chat.ID, model.State{
			QuestionID: q.NextQuestionID,
			Stage:      model.InProcess,
		})
		if err != nil {
			return err
		}
		return b.sendQuestion(send, m)
	}

	reply := tg.NewMessage(m.Chat.ID, q.Text)

	if !q.HasButtons() {
		send <- reply
		return nil
	}

	rows := make([]tg.InlineKeyboardButton, 0)
	for _, button := range q.Buttons {
		rows = append(rows,
			tg.NewInlineKeyboardButtonData(button.Text,
				fmt.Sprintf("%d", button.NextQuestionID)))
	}
	board := tg.NewInlineKeyboardMarkup(rows)
	reply.ReplyMarkup = board
	send <- reply
	return nil
}

func (b *Bot) handleMessage(send chan tg.Chattable, m *tg.Message) error {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		return err
	}

	switch st.Stage {
	case model.Finished:
		send <- tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		return nil
	case model.OnApproval:
		send <- tg.NewMessage(m.Chat.ID, "Вы уже в стадии подтверждения анкеты!")
		return nil
	case model.Unknown:
		return b.handleStart(send, m)
	}

	err = b.repo.SaveAnswer(m.Chat.ID, m.Text)
	if err != nil {
		return err
	}
	return b.sendQuestion(send, m)
}

func (b *Bot) handleCallback(send chan tg.Chattable, c *tg.CallbackQuery) error {
	// delete buttons from bot message
	edit := tg.NewEditMessageReplyMarkup(c.Message.Chat.ID, c.Message.MessageID,
		tg.NewInlineKeyboardMarkup())
	send <- edit

	st, err := b.repo.GetState(c.Message.Chat.ID)
	if err != nil {
		return err
	}

	if st.Stage == model.Finished {
		send <- tg.NewMessage(c.Message.Chat.ID, "Вы уже заполнили анкету!")
		return nil
	}

	err = b.repo.SaveAnswer(c.Message.Chat.ID, c.Message.Text)
	if err != nil {
		return err
	}
	return b.sendQuestion(send, c.Message)
}

func (b *Bot) handleStart(send chan tg.Chattable, m *tg.Message) error {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		return err
	}
	switch st.Stage {
	case model.Finished:
		send <- tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		return nil
	case model.InProcess:
		send <- tg.NewMessage(m.Chat.ID, "Вы уже в процессе заполнения анкеты!")
		return nil
	case model.OnApproval:
		send <- tg.NewMessage(m.Chat.ID, "Вы уже в стадии подтверждения анкеты!")
		return nil
	}
	err = b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 1,
		Stage:      model.InProcess,
	})
	if err != nil {
		return err
	}
	return b.sendQuestion(send, m)
}

func (b *Bot) handleReset(send chan tg.Chattable, m *tg.Message) error {
	err := b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 0,
		Stage:      model.Unknown,
	})
	if err != nil {
		return err
	}
	send <- tg.NewMessage(m.Chat.ID, "Анкета сброшена!")
	return nil
}

func (b *Bot) handleCommand(send chan tg.Chattable, m *tg.Message) error {
	b.log.WithFields(logrus.Fields{
		"chatID":    m.Chat.ID,
		"messageID": m.MessageID,
		"command":   m.Command(),
	}).Debug("Received command")

	switch m.Command() {
	case "start":
		return b.handleStart(send, m)
	case "reset":
		return b.handleReset(send, m)
	default:
		send <- tg.NewMessage(m.Chat.ID, "Неизвестная команда!")
		return nil
	}
}

func (b *Bot) logSend(send chan tg.Chattable) {
	for {
		select {
		case s := <-send:
			sent, err := b.api.Send(s)
			if err != nil {
				b.log.Error(err)
			} else {
				b.log.WithFields(logrus.Fields{
					"chatID":    sent.Chat.ID,
					"messageID": sent.MessageID,
				}).Debug("Bot sent message")
			}
		case <-b.stop:
			return
		}
	}
}

func (b *Bot) handleUpdate(u tg.Update) {
	// we use chan to send messages separately from func
	var send chan tg.Chattable
	var err error

	go b.logSend(send)

	switch {
	case u.CallbackQuery != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.CallbackQuery.Message.Chat.ID,
			"messageID": u.CallbackQuery.Message.MessageID,
			"data":      u.CallbackQuery.Data,
		}).Debug("Received callback")
		err = b.handleCallback(send, u.CallbackQuery)

	case u.Message != nil && u.Message.IsCommand():
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
			"command":   u.Message.Command(),
		}).Debug("Received command")
		err = b.handleCommand(send, u.Message)

	case u.Message != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
		}).Debug("Received message")
		err = b.handleMessage(send, u.Message)
	}

	if err != nil {
		b.log.Error(err)
		return
	}
}

func (b *Bot) listenUpdates(updates tg.UpdatesChannel) {
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
