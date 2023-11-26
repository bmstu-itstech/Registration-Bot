package bot

import (
	"Registration-Bot/model"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
)

// AddBot adds bot with provided id and token to RAM and
// returns error if it failed to create a new tgbotapi.BotAPI instance
func (r *Runner) AddBot(botID int, token string) error {
	bot, err := tg.NewBotAPI(token)
	if err != nil {
		return err
	}
	if _, ok := r.bots[botID]; ok {
		return model.ErrBotConflict
	}
	r.bots[botID] = &Bot{
		api:  bot,
		stop: make(chan struct{}),
	}
	return nil
}

// DeleteBot removes bot from memory if it was found and it is not running now
func (r *Runner) DeleteBot(botID int) error {
	bot, ok := r.bots[botID]
	if !ok {
		return model.ErrBotNotFound
	}
	if bot.running {
		return model.ErrBotInUse
	}
	delete(r.bots, botID)
	return nil
}

// RunBot launches bot with provided id and returns error
// if some error occurred while starting bot or handling request
func (r *Runner) RunBot(botID int) error {
	bot, ok := r.bots[botID]
	if !ok {
		return model.ErrBotNotFound
	}

	conf := tg.NewUpdate(0)
	conf.Timeout = 60
	updates, err := bot.api.GetUpdatesChan(conf)
	if err != nil {
		return err
	}

	go func() {
		defer r.wg.Done()
		bot.running = true
		select {
		case u := <-updates:
			go r.HandleUpdate(botID, bot.api, u)
		case <-bot.stop:
			return
		}
	}()

	return nil
}

// StopBot stops bot if it exists, all the incoming requests
// will be processed after next launch
func (r *Runner) StopBot(botID int) error {
	bot, ok := r.bots[botID]
	if !ok {
		return model.ErrBotNotFound
	}
	bot.stop <- struct{}{}
	close(bot.stop)
	return nil
}
