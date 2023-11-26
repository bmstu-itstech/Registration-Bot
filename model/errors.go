package model

import "errors"

var ErrBotNotFound = errors.New("bot with provided id was not found")
var ErrBotConflict = errors.New("bot with provided id was already added")
var ErrBotInUse = errors.New("cannot perform action with bot until it's stopped")
