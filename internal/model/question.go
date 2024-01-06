package model

type Button struct {
	Text           string
	NextQuestionID int
}

type Question struct {
	Text           string
	Buttons        []Button
	NextQuestionID int
	Rhetorical     bool
}

func (q Question) HasButtons() bool {
	return q.Buttons != nil && len(q.Buttons) != 0
}
