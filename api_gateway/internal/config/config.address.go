package config

import (
	"fmt"
)


type Address struct {
	Host string
	Port uint16
}


func (addr *Address) String() string {
	return fmt.Sprintf("%s:%d", addr.Host, addr.Port)
}
