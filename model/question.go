package model

type Button struct {
	ID   int
	Text string
}

type Question struct {
	Text           string
	Buttons        []Button
	NextQuestionID int
}

func (q Question) HasButtons() bool {
	return len(q.Buttons) != 0
}
