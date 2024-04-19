package domain

type Module struct {
	Text         string
	Buttons      []Button
	NextModuleID int
	Rhetorical   bool
}

func (m Module) HasButtons() bool {
	return m.Buttons != nil && len(m.Buttons) != 0
}

type Button struct {
	Text         string
	NextModuleID int
}
