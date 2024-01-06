package repository

import (
	model2 "Registration-Bot/internal/domain"
	"Registration-Bot/internal/domain/errors"
)

type Repository struct {
	BotID     int
	Final     string
	Users     map[int64]model2.State
	Questions map[int]model2.Question
}

func (r *Repository) SaveAnswer(chatID int64, answer string) error {
	state, ok := r.Users[chatID]
	if !ok {
		return errors.ErrUserNotFound
	}
	r.Users[chatID].Answers[state.QuestionID] = answer
	return nil
}

func (r *Repository) GetFinal() (string, error) {
	return r.Final, nil
}

func (r *Repository) GetQuestion(chatID int64) (model2.Question, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return model2.Question{}, errors.ErrUserNotFound
	}
	q, ok := r.Questions[state.QuestionID]
	if !ok {
		return model2.Question{}, errors.ErrQuestionNotFound
	}
	return q, nil
}

func (r *Repository) GetState(chatID int64) (model2.State, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return model2.State{
			Answers: make(map[int]string),
		}, nil
	}
	return state, nil
}

func (r *Repository) SetState(chatID int64, st model2.State) error {
	r.Users[chatID] = st
	return nil
}

func NewRepository(botID int, final string, questions map[int]model2.Question) *Repository {
	return &Repository{
		BotID:     botID,
		Final:     final,
		Users:     make(map[int64]model2.State),
		Questions: questions,
	}
}
