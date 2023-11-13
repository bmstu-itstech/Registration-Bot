package config

import (
	"fmt"

	"github.com/spf13/viper"
)


func Load(path string) (*Config, error) {
	viper.SetConfigFile(path)
	err := viper.ReadInConfig()
	if err != nil {
		return nil, err
	}

	cfg := &Config{
		ApiGateway: Address{
			viper.GetString("apigateway.host"),
			viper.GetUint16("apigateway.port"),
		},
		DatabaseService: Address{
			viper.GetString("databaseservice.host"),
			viper.GetUint16("databaseservice.port"),
		},
	}

	return cfg, nil
}


func (cfg *Config) Validate() error {
	if cfg.ApiGateway.Host == "" {
		return newErrNotValidConfig(
			"apigateway.host",
			"not empty",
			"",
		)	
	}

	if cfg.ApiGateway.Port == 0 {
		return newErrNotValidConfig(
			"apigateway.port",
			"in range [1-65536]",
			fmt.Sprintf("%d", cfg.ApiGateway.Port),
		)
	}

	if cfg.DatabaseService.Host == "" {
		return newErrNotValidConfig(
			"databaseservice.host",
			"not empty",
			"",
		)	
	}

	if cfg.DatabaseService.Port == 0 {
		return newErrNotValidConfig(
			"databaseservice.port",
			"in range [1-65536]",
			fmt.Sprintf("%d", cfg.DatabaseService.Port),
		)
	}

	return nil
}
