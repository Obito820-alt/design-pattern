"""Singleton Pattern example: load application configuration once."""
import json
from pathlib import Path
from threading import Lock
from typing import Any, Optional


class ConfigManager:
    _instance: Optional["ConfigManager"] = None
    _instance_lock = Lock()

    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: Optional[str] = None):
        if self._initialized:
            return
        self._config_path = Path(config_path) if config_path else Path(__file__).with_name("config.json")
        self._config = self._load_config()
        self._initialized = True

    @classmethod
    def get_instance(cls, config_path: Optional[str] = None) -> "ConfigManager":
        return cls(config_path)

    def _load_config(self) -> dict:
        with self._config_path.open("r", encoding="utf-8") as config_file:
            return json.load(config_file)

    def get(self, key: str, default: Any = None) -> Any:
        value: Any = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value


if __name__ == "__main__":
    config = ConfigManager.get_instance()
    print("Database host:", config.get("database.host"))
    print("Debug:", config.get("app.debug"))
    print("Same instance:", config is ConfigManager.get_instance())
