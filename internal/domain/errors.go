package domain

import "errors"

var ErrBotNotFound = errors.New("bot with provided id was not found")
var ErrUserNotFound = errors.New("user with provided id was not found")
var ErrQuestionNotFound = errors.New("question with provided id was not found")
