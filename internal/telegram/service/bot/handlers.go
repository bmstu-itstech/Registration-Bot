package bot

import (
	"Registration-Bot/internal/domain"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"strconv"
)

func (b *Bot) handleMessage(m *tg.Message) {
	st, err := b.repo.GetState(m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
	}

	switch st.Stage {
	case domain.Finished:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		b.logSend(m.Chat.ID, reply)
	case domain.OnApproval:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже в стадии подтверждения анкеты!")
		b.logSend(m.Chat.ID, reply)
	case domain.Unknown:
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

	if st.Stage == domain.Finished {
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
	case domain.Finished:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже заполнили анкету!")
		b.logSend(m.Chat.ID, reply)
	case domain.InProcess:
		reply := tg.NewMessage(m.Chat.ID, "Вы уже в процессе заполнения анкеты!")
		b.logSend(m.Chat.ID, reply)
	case domain.OnApproval:
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
	err := b.repo.SetState(m.Chat.ID, domain.State{
		QuestionID: 0,
		Stage:      domain.Unknown,
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
