package main

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/telegram/ports/httphandle"
	"Registration-Bot/internal/telegram/repository/local"
	"Registration-Bot/internal/telegram/usecase/runner"
	"github.com/sirupsen/logrus"
	"net/http"
)

// http server listening on port 8080
func main() {

	journal := make(map[int]domain.Module)
	journal[1] = domain.Module{
		Text:         "Привет! Это тестовая анкета",
		Buttons:      nil,
		NextModuleID: 2,
		Rhetorical:   true,
	}
	journal[2] = domain.Module{
		Text:         "Напиши свои ФИО",
		Buttons:      nil,
		NextModuleID: 3,
		Rhetorical:   false,
	}
	journal[3] = domain.Module{
		Text: "Из какого ты ВУЗа?",
		Buttons: []domain.Button{
			{
				Text:         "МГТУ",
				NextModuleID: 4,
			},
			{
				Text:         "Другой вуз",
				NextModuleID: 5,
			},
		},
		Rhetorical: false,
	}
	journal[4] = domain.Module{
		Text:         "Из какой ты группы?",
		Buttons:      nil,
		NextModuleID: 5,
		Rhetorical:   false,
	}
	journal[5] = domain.Module{
		Text:         "Из какого ты ВУЗа?",
		Buttons:      nil,
		NextModuleID: 0,
		Rhetorical:   false,
	}

	bots := make(map[int]*local.Bot)
	repo := local.NewRepository(bots)
	run := runner.NewRunner(logrus.New(), repo)
	handler := httphandle.NewHandler(logrus.New(), repo, run, journal)

	http.Handle("/", http.FileServer(http.Dir("./static")))
	http.HandleFunc("/new", handler.Handle)
	err := http.ListenAndServe(":8888", nil)
	if err != nil {
		panic(err)
	}

}
