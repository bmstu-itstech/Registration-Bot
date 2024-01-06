package service

import (
	"Registration-Bot/model"
	"fmt"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"strconv"
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

//go:generate mockery --name BotAPI
type BotAPI interface {
	Send(tg.Chattable) (tg.Message, error)
}

type Bot struct {
	api  BotAPI
	log  logrus.FieldLogger
	stop chan struct{}
	repo Repository
}

func (b *Bot) sendFinal(m *tg.Message) (tg.Message, error) {
	err := b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 0,
		Stage:      model.Finished,
	})
	if err != nil {
		return tg.Message{}, err
	}
	text, err := b.repo.GetFinal()
	if err != nil {
		return tg.Message{}, err
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	return b.api.Send(reply)
}

func (b *Bot) sendQuestion(m *tg.Message) (tg.Message, error) {
	q, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}

	if q.Rhetorical {
		reply := tg.NewMessage(m.Chat.ID, q.Text)
		sent, err := b.api.Send(reply)
		if err != nil {
			return tg.Message{}, err
		}

		b.log.WithFields(logrus.Fields{
			"chatID":    sent.Chat.ID,
			"messageID": sent.MessageID,
		}).Debug("Bot sent message")

		st, err := b.repo.GetState(m.Chat.ID)
		if err != nil {
			return tg.Message{}, err
		}
		st.QuestionID = q.NextQuestionID
		err = b.repo.SetState(m.Chat.ID, st)
		if err != nil {
			return tg.Message{}, err
		}
		return b.sendQuestion(m)
	}

	reply := tg.NewMessage(m.Chat.ID, q.Text)

	if !q.HasButtons() {
		return b.api.Send(reply)
	}

	rows := make([]tg.InlineKeyboardButton, 0)
	for _, button := range q.Buttons {
		rows = append(rows,
			tg.NewInlineKeyboardButtonData(button.Text,
				fmt.Sprintf("%d", button.NextQuestionID)))
	}
	board := tg.NewInlineKeyboardMarkup(rows)
	reply.ReplyMarkup = board
	return b.api.Send(reply)
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
		return b.api.Send(tg.NewMessage(m.Chat.ID,
			"Вы уже в стадии подтверждения анкеты!"))
	case model.Unknown:
		return b.handleStart(m)
	}

	err = b.repo.SaveAnswer(m.Chat.ID, m.Text)
	if err != nil {
		return tg.Message{}, err
	}
	q, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}

	if q.NextQuestionID == 0 {
		return b.sendFinal(m)
	}

	st.QuestionID = q.NextQuestionID
	err = b.repo.SetState(m.Chat.ID, st)
	return b.sendQuestion(m)
}

func (b *Bot) handleCallback(c *tg.CallbackQuery) (tg.Message, error) {
	// delete buttons from bot message
	edit := tg.NewEditMessageReplyMarkup(c.Message.Chat.ID, c.Message.MessageID,
		tg.NewInlineKeyboardMarkup())
	sent, err := b.api.Send(edit)
	if err != nil {
		return tg.Message{}, err
	}
	b.log.Info(sent)
	st, err := b.repo.GetState(c.Message.Chat.ID)
	if err != nil {
		return tg.Message{}, err
	}

	if st.Stage == model.Finished {
		return b.api.Send(tg.NewMessage(c.Message.Chat.ID,
			"Вы уже заполнили анкету!"))
	}

	err = b.repo.SaveAnswer(c.Message.Chat.ID, c.Message.Text)
	if err != nil {
		return tg.Message{}, err
	}

	next, err := strconv.Atoi(c.Data)
	if err != nil {
		return tg.Message{}, err
	}
	if next == 0 {
		return b.sendFinal(c.Message)
	}

	st.QuestionID = next
	err = b.repo.SetState(c.Message.Chat.ID, st)
	if err != nil {
		return tg.Message{}, err
	}
	return b.sendQuestion(c.Message)
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
	st.QuestionID = 1
	err = b.repo.SetState(m.Chat.ID, st)
	if err != nil {
		return tg.Message{}, err
	}
	return b.sendQuestion(m)
}

func (b *Bot) handleReset(m *tg.Message) (tg.Message, error) {
	err := b.repo.SetState(m.Chat.ID, model.State{
		QuestionID: 0,
		Stage:      model.Unknown,
		Answers:    make(map[int]string),
	})
	if err != nil {
		return tg.Message{}, err
	}
	reply := tg.NewMessage(m.Chat.ID, "Анкета сброшена!")
	return b.api.Send(reply)
}

func (b *Bot) handleCommand(m *tg.Message) (tg.Message, error) {
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

func (b *Bot) handleUpdate(u tg.Update) {
	var sent tg.Message
	var err error

	switch {
	case u.CallbackQuery != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.CallbackQuery.Message.Chat.ID,
			"messageID": u.CallbackQuery.Message.MessageID,
			"data":      u.CallbackQuery.Data,
		}).Debug("Received callback")
		sent, err = b.handleCallback(u.CallbackQuery)

	case u.Message != nil && u.Message.IsCommand():
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
			"command":   u.Message.Command(),
		}).Debug("Received command")
		sent, err = b.handleCommand(u.Message)

	case u.Message != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
		}).Debug("Received message")
		sent, err = b.handleMessage(u.Message)
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
