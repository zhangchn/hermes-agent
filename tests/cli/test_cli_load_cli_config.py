"""Tests for load_cli_config() in cli.py"""

import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

class TestLoadConfigCliConfig:
    """load_cli_config() must be able to open config.yml with utf-8 encoding"""
    
    @pytest.fixture
    def config_env(self, tmp_path, monkeypatch):
        """Isolated config environment with a writable config.yaml."""
        hermes_home = tmp_path / ".hermes"
        hermes_home.mkdir()
        config_path = hermes_home / "config.yaml"
        config_path.write_text(yaml.dump({
            "model": {"default": "test-model", "provider": "openrouter"},
            "display": {"skin": "test-skin"},
        }) + "\n# ── Fallback Model ──────\n", encoding="utf-8")
        monkeypatch.setattr("cli._hermes_home", hermes_home)
        return config_path

    def test_load_cli_config_encoding(self, config_env):
        from cli import load_cli_config
        
        config = load_cli_config()
        assert config["model"]["default"] == "test-model"
        assert config["model"]["provider"] == "openrouter"
        assert config["display"]["skin"] == "test-skin"
