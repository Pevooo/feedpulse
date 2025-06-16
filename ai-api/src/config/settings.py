import weakref
from typing import Dict, List, Set, Any
from src.config.updatable import Updatable


class Settings:
    """
    Manages application settings and notifies registered observers upon updates.

    Settings are defined as class attributes. To add a new setting, define its default value
    as a class attribute and register it in the appropriate settings collection:
      - BOOLEAN_SETTINGS: a set of names for boolean settings.
      - NUMBER_SETTINGS: a dict mapping numeric setting names to a list of valid integer values.

    The class supports updating settings from a JSON-like dict and notifies observers after changes.
    """

    # Registered observers
    _observers: weakref.WeakSet[Updatable] = weakref.WeakSet()

    # Configuration for setting types
    BOOLEAN_SETTINGS: Set[str] = {
        "enable_facebook_data_collection",
        "enable_instagram_data_collection",
    }

    NUMBER_SETTINGS: Dict[str, List[int]] = {
        "processing_batch_size": [1, 2, 4, 8, 16, 32],
        "global_model_provider_retry_delay": [30, 60, 90, 120, 150, 180],
        "global_model_provider_retry_count": [1, 2, 3, 4, 5],
        "routing_component_temperature_x10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "chat_component_temperature_x10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "format_component_temperature_x10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "query_component_temperature_x10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "visualization_component_temperature_x10": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    }

    # Default settings values
    enable_facebook_data_collection: bool = True
    enable_instagram_data_collection: bool = True
    processing_batch_size: int = 32

    # Global Model Provider Settings
    global_model_provider_retry_delay: int = 60
    global_model_provider_retry_count: int = 3

    # Polling Data Streamer Settings
    polling_data_streamer_trigger_time: int = 60

    # Chatbot Component Temperatures
    routing_component_temperature_x10: int = 10
    chat_component_temperature_x10: int = 10
    format_component_temperature_x10: int = 10
    query_component_temperature_x10: int = 10
    visualization_component_temperature_x10: int = 10

    @classmethod
    def register_observer(cls, observer: Updatable) -> None:
        """
        Registers an observer to be notified when settings change.
        """
        cls._observers.add(observer)

    @classmethod
    def remove_observer(cls, observer: Updatable) -> None:
        """
        Removes a previously registered observer.
        """
        cls._observers.discard(observer)

    @classmethod
    def _notify_observers(cls) -> None:
        """
        Notifies all registered observers about the settings update.
        """
        for observer in list(cls._observers):
            observer.update()

    @classmethod
    def get_settings(cls) -> List[Dict[str, Any]]:
        """
        Returns a list of settings metadata dictionaries.

        Each dictionary contains:
          - settingName: the identifier of the setting.
          - settingValue: the current value of the setting.
          - prettyName: a human-readable name generated from the identifier.
          - type: the type of the setting ('bool' or 'int').
          - choices: valid options for the setting.
        """
        settings_list: List[Dict[str, Any]] = []

        # Process boolean settings
        for setting in cls.BOOLEAN_SETTINGS:
            settings_list.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "bool",
                    "choices": [True, False],
                }
            )

        # Process number settings
        for setting, choices in cls.NUMBER_SETTINGS.items():
            settings_list.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "int",
                    "choices": choices,
                }
            )

        return settings_list

    @classmethod
    def update_settings(cls, settings: Dict[str, List[Dict[str, str]]]) -> bool:
        """
        Updates settings based on the provided dictionary.

        The settings dict must have a key "settingsList" containing a list of dictionaries, each with:
          - settingName: the name of the setting to update.
          - settingValue: the new value (as a string).

        Returns True if all settings were updated successfully, otherwise False.
        Observers are notified after attempting to update all settings.
        """
        success = True

        if "settingsList" not in settings:
            return False

        for setting in settings.get("settingsList", []):
            name = setting.get("settingName")
            value = setting.get("settingValue")
            if name is None or value is None:
                success = False
                continue
            success &= cls._update_setting(name, value)

        cls._notify_observers()
        return success

    @classmethod
    def _update_setting(cls, name: str, value: str) -> bool:
        """
        Determines the type of the setting and updates its value accordingly.
        """
        if name in cls.BOOLEAN_SETTINGS:
            return cls._update_bool_setting(name, value)
        elif name in cls.NUMBER_SETTINGS:
            return cls._update_int_setting(name, value)
        else:
            # Unknown setting
            return False

    @classmethod
    def _update_int_setting(cls, name: str, value: str) -> bool:
        """
        Validates and updates an integer setting.
        """
        try:
            int_value = int(value)
        except ValueError:
            return False

        if int_value not in cls.NUMBER_SETTINGS[name]:
            return False

        setattr(cls, name, int_value)
        return True

    @classmethod
    def _update_bool_setting(cls, name: str, value: str) -> bool:
        """
        Validates and updates a boolean setting.
        """
        normalized = value.strip().lower()

        if name not in cls.BOOLEAN_SETTINGS:
            return False

        if normalized == "true":
            setattr(cls, name, True)
            return True
        elif normalized == "false":
            setattr(cls, name, False)
            return True
        else:
            return False
