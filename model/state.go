package model

const (
	Unknown = iota
	InProcess
	OnApproval
	Finished
)

type State struct {
	QuestionID int
	Stage      int
}
