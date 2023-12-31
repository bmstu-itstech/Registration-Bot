package service

import (
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
)

type Bot struct {
	*tg.BotAPI
	id   int
	log  logrus.FieldLogger
	stop chan struct{}
}

func (b *Bot) chooseHandler(u tg.Update) {
	panic("not implemented")
}

func (b *Bot) listenUpdates(updates tg.UpdatesChannel) {
	b.log.Info("Bot started")
	for {
		select {
		case u := <-updates:
			b.chooseHandler(u)
		case <-b.stop:
			b.log.Info("Bot stopped")
			return
		}
	}
}
