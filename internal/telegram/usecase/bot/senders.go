package bot

import (
	"Registration-Bot/internal/domain"
	"fmt"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
)

func (b *Bot) sendFinal(m *tg.Message) {
	err := b.repo.SetState(b.botID, m.Chat.ID, domain.State{
		QuestionID: 0,
		Stage:      domain.Finished,
	})
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}
	text, err := b.repo.GetFinal(b.botID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}
	reply := tg.NewMessage(m.Chat.ID, text)
	b.logSend(m.Chat.ID, reply)
}

func (b *Bot) sendQuestion(m *tg.Message) {
	q, err := b.repo.GetCurrentModule(b.botID, m.Chat.ID)
	if err != nil {
		b.logErr(m.Chat.ID, err)
		return
	}

	if q.Rhetorical {
		reply := tg.NewMessage(m.Chat.ID, q.Text)
		b.logSend(m.Chat.ID, reply)

		st, err := b.repo.GetState(b.botID, m.Chat.ID)
		if err != nil {
			b.logErr(m.Chat.ID, err)
			return
		}
		st.QuestionID = q.NextModuleID
		err = b.repo.SetState(b.botID, m.Chat.ID, st)
		if err != nil {
			b.logErr(m.Chat.ID, err)
			return
		}
		b.sendQuestion(m)
		return
	}

	reply := tg.NewMessage(m.Chat.ID, q.Text)
	if q.HasButtons() {
		rows := make([]tg.InlineKeyboardButton, 0)
		for _, button := range q.Buttons {
			rows = append(rows,
				tg.NewInlineKeyboardButtonData(button.Text,
					fmt.Sprintf("%d", button.NextModuleID)))
		}
		board := tg.NewInlineKeyboardMarkup(rows)
		reply.ReplyMarkup = board
	}
	b.logSend(m.Chat.ID, reply)
}
