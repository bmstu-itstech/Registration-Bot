package service

import (
	model2 "Registration-Bot/internal/domain"
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
	GetQuestion(chatID int64) (model2.Question, error)

	GetState(chatID int64) (model2.State, error)
	SetState(chatID int64, st model2.State) error
}

//go:generate mockery --name BotAPI
type BotAPI interface {
	Send(m tg.Chattable) (tg.Message, error)
}

type Bot struct {
	api  BotAPI
	log  logrus.FieldLogger
	stop chan struct{}
	repo Repository
}

func (b *Bot) logErr(chatID int64, err error) {
	b.log.WithField("chatID", chatID).Error(err)
}

func (b *Bot) logSend(chatID int64, m tg.Chattable) {
	sent, err := b.api.Send(m)
	if err != nil {
		b.logErr(chatID, err)
	}
	b.log.WithFields(logrus.Fields{
		"chatID":    sent.Chat.ID,
		"messageID": sent.MessageID,
		"text":      sent.Text,
	}).Debug("Sent message")
}

func (b *Bot) sendFinal(m *tg.Message) {
	err := b.repo.SetState(m.Chat.ID, model2.State{
		QuestionID: 0,
		Stage:      model2.Finished,
	})
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}
	text, err := b.repo.GetFinal()
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	b.logSend(m.Chat.ID, reply)
}

func (b *Bot) sendQuestion(m *tg.Message) {
	q, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}

	if q.Rhetorical {
		reply := tg.NewMessage(m.Chat.ID, q.Text)
		b.logSend(m.Chat.ID, reply)

		st, err := b.repo.GetState(m.Chat.ID)
		if err != nil {
			b.logErr(m.Chat.ID, err)
			return
		}
		st.QuestionID = q.NextQuestionID
		err = b.repo.SetState(m.Chat.ID, st)
		if err != nil {
			b.logErr(m.Chat.ID, err)
			return
		}
		b.sendQuestion(m)
	}

	reply := tg.NewMessage(m.Chat.ID, q.Text)
	if q.HasButtons() {
		rows := make([]tg.InlineKeyboardButton, 0)
		for _, button := range q.Buttons {
			rows = append(rows,
				tg.NewInlineKeyboardButtonData(button.Text,
					fmt.Sprintf("%d", button.NextQuestionID)))
		}
		board := tg.NewInlineKeyboardMarkup(rows)
		reply.ReplyMarkup = board
	}
	b.logSend(m.Chat.ID, reply)
}

func (b *Bot) handleMessage(m *tg.Message) {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}

	switch st.Stage {
	case model2.Finished:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		b.logSend(m.Chat.ID, reply)
	case model2.OnApproval:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже в стадии подтверждения анкеты!")
		b.logSend(m.Chat.ID, reply)
	case model2.Unknown:
		b.handleStart(m)
	}

	err = b.repo.SaveAnswer(m.Chat.ID, m.Text)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}
	q, err := b.repo.GetQuestion(m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}

	if q.NextQuestionID == 0 {
		b.sendFinal(m)
		return
	}

	st.QuestionID = q.NextQuestionID
	err = b.repo.SetState(m.Chat.ID, st)
	b.sendQuestion(m)
}

func (b *Bot) handleCallback(c *tg.CallbackQuery) {
	// delete buttons from bot message
	edit := tg.NewEditMessageReplyMarkup(c.Message.Chat.ID, c.Message.MessageID,
		tg.NewInlineKeyboardMarkup())
	b.logSend(c.Message.Chat.ID, edit)
	st, err := b.repo.GetState(c.Message.Chat.ID)
	if err != nil {
		b.logErr(c.Message.Chat.ID, err)
	}

	if st.Stage == model2.Finished {
		reply := tg.NewMessage(c.Message.Chat.ID, "Вы уже заполнили анкету!")
		b.logSend(c.Message.Chat.ID, reply)
	}

	err = b.repo.SaveAnswer(c.Message.Chat.ID, c.Message.Text)
	if err != nil {
		b.logErr(c.Message.Chat.ID, err)
	}

	next, err := strconv.Atoi(c.Data)
	if err != nil {
		b.logErr(c.Message.Chat.ID, err)
	}
	if next == 0 {
		b.sendFinal(c.Message)
	}

	st.QuestionID = next
	err = b.repo.SetState(c.Message.Chat.ID, st)
	if err != nil {
		b.logErr(c.Message.Chat.ID, err)
	}
	b.sendQuestion(c.Message)
}

func (b *Bot) handleStart(m *tg.Message) {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}
	switch st.Stage {
	case model2.Finished:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		b.logSend(m.Chat.ID, reply)
	case model2.InProcess:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже в процессе заполнения анкеты!")
		b.logSend(m.Chat.ID, reply)
	case model2.OnApproval:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже в стадии подтверждения анкеты!")
		b.logSend(m.Chat.ID, reply)
	}
	st.QuestionID = 1
	err = b.repo.SetState(m.Chat.ID, st)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}
	b.sendQuestion(m)
}

func (b *Bot) handleReset(m *tg.Message) {
	err := b.repo.SetState(m.Chat.ID, model2.State{
		QuestionID: 0,
		Stage:      model2.Unknown,
		Answers:    make(map[int]string),
	})
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}
	reply := tg.NewMessage(m.Chat.ID, "Анкета сброшена!")
	b.logSend(m.Chat.ID, reply)
}

func (b *Bot) handleCommand(m *tg.Message) {
	switch m.Command() {
	case "start":
		b.handleStart(m)
	case "reset":
		b.handleReset(m)
	default:
		reply := tg.NewMessage(m.Chat.ID, "Неизвестная команда!")
		b.logSend(m.Chat.ID, reply)
	}
}

func (b *Bot) handleUpdate(u tg.Update) {
	switch {
	case u.CallbackQuery != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.CallbackQuery.Message.Chat.ID,
			"messageID": u.CallbackQuery.Message.MessageID,
			"data":      u.CallbackQuery.Data,
		}).Debug("Received callback")
		b.handleCallback(u.CallbackQuery)

	case u.Message != nil && u.Message.IsCommand():
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
			"command":   u.Message.Command(),
		}).Debug("Received command")
		b.handleCommand(u.Message)

	case u.Message != nil:
		b.log.WithFields(logrus.Fields{
			"chatID":    u.Message.Chat.ID,
			"messageID": u.Message.MessageID,
			"text":      u.Message.Text,
		}).Debug("Received message")
		b.handleMessage(u.Message)
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
