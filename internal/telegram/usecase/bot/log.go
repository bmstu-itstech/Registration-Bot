package bot

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

func (b *Bot) logErr(chatID int64, err error) {
	b.log.WithField("chatID", chatID).Error(err)
}

func (b *Bot) logSend(chatID int64, m tg.Chattable) {
	sent, err := b.api.Send(m)
	if err != nil {
		b.logErr(chatID, err)
		//return
	}
	b.log.WithFields(logrus.Fields{
		"chatID":    sent.Chat.ID,
		"messageID": sent.MessageID,
		"text":      sent.Text,
	}).Debug("Sent message")
}
