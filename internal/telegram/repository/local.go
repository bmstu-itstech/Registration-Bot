package repository

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/domain/errors"
)

type Repository struct {
	BotID     int
	Final     string
	Users     map[int64]domain.State
	Questions map[int]domain.Question
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

func (r *Repository) GetQuestion(chatID int64) (domain.Question, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return domain.Question{}, errors.ErrUserNotFound
	}
	q, ok := r.Questions[state.QuestionID]
	if !ok {
		return domain.Question{}, errors.ErrQuestionNotFound
	}
	return q, nil
}

func (r *Repository) GetState(chatID int64) (domain.State, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return domain.State{
			Answers: make(map[int]string),
		}, nil
	}
	return state, nil
}

func (r *Repository) SetState(chatID int64, st domain.State) error {
	r.Users[chatID] = st
	return nil
}

func NewRepository(botID int, final string, questions map[int]domain.Question) *Repository {
	return &Repository{
		BotID:     botID,
		Final:     final,
		Users:     make(map[int64]domain.State),
		Questions: questions,
	}
}
