package delivery

type Service interface {
	StartBot(botID int, token string) error
	StopBot(botID int) error
}
