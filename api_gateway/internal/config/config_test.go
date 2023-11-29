package config_test

import (
	"apigateway/internal/config"
	"testing"
)

const (
	PATH_TO_EXAMPLE_CONFIG = "../../config/example.yml"
)

// Checks functionality of configuration file decoder
func TestExampleConfiguration(t *testing.T) {
	cfg, err := config.Load(PATH_TO_EXAMPLE_CONFIG)
	if err != nil {
		t.Fatalf(
			"error loading configuration file %s: %s",
			PATH_TO_EXAMPLE_CONFIG,
			err.Error(),
		)
	}

	err = cfg.Validate()
	if err != nil {
		t.Fatalf(
			"error validating configuration %s: %s",
			PATH_TO_EXAMPLE_CONFIG,
			err.Error(),
		)
	}

	t.Logf("Successfully loaded configuration: %v\n", cfg)
}
