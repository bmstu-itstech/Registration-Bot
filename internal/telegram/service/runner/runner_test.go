package runner

import (
	"Registration-Bot/internal/domain"
	"Registration-Bot/internal/telegram/service/bot"
	"Registration-Bot/internal/telegram/service/bot/mocks"
	tg "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/sirupsen/logrus"
	"github.com/sirupsen/logrus/hooks/test"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
	"testing"
)

type RunnerTestSuite struct {
	suite.Suite
	log  logrus.FieldLogger
	repo bot.Repository
	r    *Runner
}

func (s *RunnerTestSuite) SetupTest() {
	s.log, _ = test.NewNullLogger()
	s.repo = mocks.NewRepository(s.T())
	s.r = NewRunner(s.log, s.repo)
}

func TestRunnerTestSuite(t *testing.T) {
	suite.Run(t, new(RunnerTestSuite))
}

func (s *RunnerTestSuite) TestStartBotBadToken() {
	err := s.r.StartBot(1, "incorrect token", make(map[int]domain.Module), "")
	assert.Error(s.T(), err)
}

func (s *RunnerTestSuite) TestStopBot() {
	b := bot.NewBot(&tg.BotAPI{}, s.log, s.repo, 1)
	s.r.bots[1] = b
	go b.ListenUpdates(make(tg.UpdatesChannel))
	err := s.r.StopBot(1)
	assert.NoError(s.T(), err)
	assert.NotContains(s.T(), s.r.bots, 1)
}

func (s *RunnerTestSuite) TestStopBotNonexistent() {
	err := s.r.StopBot(-1)
	assert.ErrorIs(s.T(), err, domain.ErrBotNotFound)
}
