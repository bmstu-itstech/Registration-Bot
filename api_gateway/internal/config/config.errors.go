package config

import "fmt"


type ErrNotValidConfig struct {
	comment string
}

// Error with information about an invalid field
func newErrNotValidConfig(argName, must, got string) *ErrNotValidConfig {
	comment := fmt.Sprintf("%s must be %s", argName, must)
	if got != "" {
		comment += fmt.Sprintf("; got %s", got)
	}
	return &ErrNotValidConfig{ comment: comment }
} 


func (err *ErrNotValidConfig) Error() string {
	return fmt.Sprintf("ErrNotValidConfig: %s", err.comment)
}
