// Code generated by mockery v0.0.0-dev. DO NOT EDIT.

package mocks

import (
	domain "Registration-Bot/internal/domain"

	mock "github.com/stretchr/testify/mock"
)

// Repository is an autogenerated mock type for the Repository type
type Repository struct {
	mock.Mock
}

// GetFinal provides a mock function with given fields:
func (_m *Repository) GetFinal() (string, error) {
	ret := _m.Called()

	var r0 string
	var r1 error
	if rf, ok := ret.Get(0).(func() (string, error)); ok {
		return rf()
	}
	if rf, ok := ret.Get(0).(func() string); ok {
		r0 = rf()
	} else {
		r0 = ret.Get(0).(string)
	}

	if rf, ok := ret.Get(1).(func() error); ok {
		r1 = rf()
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// GetQuestion provides a mock function with given fields: chatID
func (_m *Repository) GetQuestion(chatID int64) (domain.Question, error) {
	ret := _m.Called(chatID)

	var r0 domain.Question
	var r1 error
	if rf, ok := ret.Get(0).(func(int64) (domain.Question, error)); ok {
		return rf(chatID)
	}
	if rf, ok := ret.Get(0).(func(int64) domain.Question); ok {
		r0 = rf(chatID)
	} else {
		r0 = ret.Get(0).(domain.Question)
	}

	if rf, ok := ret.Get(1).(func(int64) error); ok {
		r1 = rf(chatID)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// GetState provides a mock function with given fields: chatID
func (_m *Repository) GetState(chatID int64) (domain.State, error) {
	ret := _m.Called(chatID)

	var r0 domain.State
	var r1 error
	if rf, ok := ret.Get(0).(func(int64) (domain.State, error)); ok {
		return rf(chatID)
	}
	if rf, ok := ret.Get(0).(func(int64) domain.State); ok {
		r0 = rf(chatID)
	} else {
		r0 = ret.Get(0).(domain.State)
	}

	if rf, ok := ret.Get(1).(func(int64) error); ok {
		r1 = rf(chatID)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// SaveAnswer provides a mock function with given fields: chatID, answer
func (_m *Repository) SaveAnswer(chatID int64, answer string) error {
	ret := _m.Called(chatID, answer)

	var r0 error
	if rf, ok := ret.Get(0).(func(int64, string) error); ok {
		r0 = rf(chatID, answer)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// SetState provides a mock function with given fields: chatID, st
func (_m *Repository) SetState(chatID int64, st domain.State) error {
	ret := _m.Called(chatID, st)

	var r0 error
	if rf, ok := ret.Get(0).(func(int64, domain.State) error); ok {
		r0 = rf(chatID, st)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// NewRepository creates a new instance of Repository. It also registers a testing interface on the mock and a cleanup function to assert the mocks expectations.
// The first argument is typically a *testing.T value.
func NewRepository(t interface {
	mock.TestingT
	Cleanup(func())
}) *Repository {
	mock := &Repository{}
	mock.Mock.Test(t)

	t.Cleanup(func() { mock.AssertExpectations(t) })

	return mock
}
