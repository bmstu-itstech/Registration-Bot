package local

import (
	"Registration-Bot/internal/domain"
)

type Repository struct {
	Bots map[int]*Bot
}

func NewRepository(bots map[int]*Bot) *Repository {
	return &Repository{Bots: bots}
}

type Bot struct {
	Final   string
	States  map[int64]domain.State
	Modules map[int]domain.Module
}

func (r *Repository) AddBot(botID int, journal map[int]domain.Module, final string) error {
	_, ok := r.Bots[botID]
	if ok {
		return domain.ErrBotConflict
	}
	r.Bots[botID] = &Bot{
		Final:   final,
		States:  make(map[int64]domain.State),
		Modules: journal,
	}
	return nil
}

func (r *Repository) DeleteBot(botID int) error {
	_, ok := r.Bots[botID]
	if !ok {
		return domain.ErrBotNotFound
	}
	delete(r.Bots, botID)
	return nil
}

func (r *Repository) GetState(botID int, chatID int64) (domain.State, error) {
	b, ok := r.Bots[botID]
	if !ok {
		return domain.State{}, domain.ErrBotNotFound
	}
	st, ok := b.States[chatID]
	if !ok {
		return domain.State{}, domain.ErrUserNotFound
	}
	return st, nil
}

func (r *Repository) SetState(botID int, chatID int64, st domain.State) error {
	b, ok := r.Bots[botID]
	if !ok {
		return domain.ErrBotNotFound
	}
	b.States[chatID] = st
	return nil
}

// SaveAnswer is used to save user's answer
func (r *Repository) SaveAnswer(botID int, chatID int64, text string) error {
	st, err := r.GetState(botID, chatID)
	if err != nil {
		return err
	}
	st.Answers[st.QuestionID] = text
	return r.SetState(botID, chatID, st)
}

// SetModuleID sets current module ID for user
func (r *Repository) SetModuleID(botID int, chatID int64, questionID int) error {
	st, err := r.GetState(botID, chatID)
	if err != nil {
		return err
	}
	st.QuestionID = questionID
	return r.SetState(botID, chatID, st)
}

// SetStage sets user's questionnaire stage
func (r *Repository) SetStage(botID int, chatID int64, stage int) error {
	st, err := r.GetState(botID, chatID)
	if err != nil {
		return err
	}
	st.Stage = stage
	return r.SetState(botID, chatID, st)
}

// GetCurrentModule returns user's current module
func (r *Repository) GetCurrentModule(botID int, chatID int64) (domain.Module, error) {
	st, err := r.GetState(botID, chatID)
	if err != nil {
		return domain.Module{}, err
	}
	return r.Bots[botID].Modules[st.QuestionID], nil
}

// GetFinal returns final message of bot
func (r *Repository) GetFinal(botID int) (string, error) {
	b, ok := r.Bots[botID]
	if !ok {
		return "", domain.ErrBotNotFound
	}
	return b.Final, nil
}

func (r *Repository) PushAnswers(botID int, chatID int64) error {
	b, ok := r.Bots[botID]
	if !ok {
		return domain.ErrBotNotFound
	}
	_, ok = b.States[chatID]
	if !ok {
		return domain.ErrUserNotFound
	}
	return nil
}
