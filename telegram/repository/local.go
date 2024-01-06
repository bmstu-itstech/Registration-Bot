package repository

import "Registration-Bot/model"

type Repository struct {
	BotID     int
	Final     string
	Users     map[int64]model.State
	Questions map[int]model.Question
}

func (r *Repository) SaveAnswer(chatID int64, answer string) error {
	state, ok := r.Users[chatID]
	if !ok {
		return model.ErrUserNotFound
	}
	r.Users[chatID].Answers[state.QuestionID] = answer
	return nil
}

func (r *Repository) GetFinal() (string, error) {
	return r.Final, nil
}

func (r *Repository) GetQuestion(chatID int64) (model.Question, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return model.Question{}, model.ErrUserNotFound
	}
	q, ok := r.Questions[state.QuestionID]
	if !ok {
		return model.Question{}, model.ErrQuestionNotFound
	}
	return q, nil
}

func (r *Repository) GetState(chatID int64) (model.State, error) {
	state, ok := r.Users[chatID]
	if !ok {
		return model.State{
			Answers: make(map[int]string),
		}, nil
	}
	return state, nil
}

func (r *Repository) SetState(chatID int64, st model.State) error {
	r.Users[chatID] = st
	return nil
}

func NewRepository(botID int, final string, questions map[int]model.Question) *Repository {
	return &Repository{
		BotID:     botID,
		Final:     final,
		Users:     make(map[int64]model.State),
		Questions: questions,
	}
}
