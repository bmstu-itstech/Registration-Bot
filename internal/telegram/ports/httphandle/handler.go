package httphandle

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/telegram/repository/local"
	"Registration-Bot/internal/telegram/usecase/runner"
	"github.com/sirupsen/logrus"
	"net/http"
)

func NewHandler(log *logrus.Logger, repo *local.Repository, uc *runner.Runner, journal map[int]domain.Module) *Handler {
	return &Handler{
		log:     log,
		repo:    repo,
		uc:      uc,
		journal: journal,
	}
}

type Handler struct {
	log     *logrus.Logger
	repo    *local.Repository
	uc      *runner.Runner
	journal map[int]domain.Module
}

var BotID = 0

func (h *Handler) Handle(w http.ResponseWriter, r *http.Request) {
	h.log.Info("Bot created")
	token := r.FormValue("token")
	h.repo.AddBot(BotID, h.journal, "Приходите на наше мероприятие!")
	err := h.uc.StartBot(BotID, token, h.journal, "Приходите на наше мероприятие!")
	if err != nil {
		h.log.Error(err)
		return
	}
	BotID++
	w.WriteHeader(http.StatusOK)
}
