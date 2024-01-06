package repository

import "Registration-Bot/model"

type User struct {
	Answers map[int]string
	State   model.State
}

type Repository struct {
	BotID     int
	Final     string
	Users     map[int64]*User
	Questions map[int]model.Question
}

func (r *Repository) AddUser(chatID int64) error {
	_, ok := r.Users[chatID]
	if !ok {
		r.Users[chatID] = &User{
			Answers: make(map[int]string),
			State:   model.State{},
		}
	}
	return nil
}

func (r *Repository) DeleteUser(chatID int64) error {
	delete(r.Users, chatID)
	return nil
}

func (r *Repository) SaveAnswer(chatID int64, answer string) error {
	user, ok := r.Users[chatID]
	if !ok {
		return model.ErrUserNotFound
	}
	r.Users[chatID].Answers[user.State.QuestionID] = answer
	return nil
}

func (r *Repository) GetFinal() (string, error) {
	return r.Final, nil
}

func (r *Repository) GetQuestion(chatID int64) (model.Question, error) {
	user, ok := r.Users[chatID]
	if !ok {
		return model.Question{}, model.ErrUserNotFound
	}
	q, ok := r.Questions[user.State.QuestionID]
	if !ok {
		return model.Question{}, model.ErrQuestionNotFound
	}
	return q, nil
}

func (r *Repository) GetState(chatID int64) (model.State, error) {
	user, ok := r.Users[chatID]
	if !ok {
		return model.State{}, model.ErrUserNotFound
	}
	return user.State, nil
}

func (r *Repository) SetState(chatID int64, st model.State) error {
	user, ok := r.Users[chatID]
	if !ok {
		return model.ErrUserNotFound
	}
	user.State = st
	return nil
}

func NewRepository(botID int, final string, questions map[int]model.Question) *Repository {
	return &Repository{
		BotID:     botID,
		Final:     final,
		Users:     make(map[int64]*User),
		Questions: questions,
	}
}
