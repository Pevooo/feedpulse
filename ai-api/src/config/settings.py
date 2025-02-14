# This class is responsible for managing the setting of the whole app. You can add a setting by adding it in the class
# alongside with its default value and also add it in `BOOLEAN_SETTINGS` if it's a boolean or in `MODEL_SETTINGS` if
# it's a model setting (This is for remote config purposes)


class Settings:
    """
    This class encapsulates all the AI Api configurations.
    """

    BOOLEAN_SETTINGS = {
        "enable_facebook_data_collection",
        "enable_instagram_data_collection",
    }

    NUMBER_SETTINGS = {
        "processing_batch_size": [1, 2, 4, 8, 16, 32],
    }

    # Features
    enable_facebook_data_collection: bool = True
    enable_instagram_data_collection: bool = True

    processing_batch_size: int = 1

    @classmethod
    def get_settings(cls) -> list[dict[str, str]]:
        settings = []
        for setting in cls.BOOLEAN_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "bool",
                    "choices": ["true", "false"],
                },
            )

        for setting in cls.NUMBER_SETTINGS:
            settings.append(
                {
                    "settingName": setting,
                    "settingValue": getattr(cls, setting),
                    "prettyName": " ".join(setting.split("_")).title(),
                    "type": "int",
                    "choices": cls.NUMBER_SETTINGS[setting],
                }
            )

        return settings

    @classmethod
    def update_settings(cls, settings: dict[str, list[dict[str, str]]]) -> bool:
        updated = True
        for setting in settings["settingsList"]:

            # Set updated to false if there's one or more setting(s) failed to update
            updated &= cls._set_setting(setting["settingName"], setting["settingValue"])

        return updated

    @classmethod
    def _set_setting(cls, setting_name: str, value: str) -> bool:
        changed = False
        if setting_name in cls.BOOLEAN_SETTINGS:
            changed = cls._set_bool_setting(setting_name, value)
        elif setting_name in cls.NUMBER_SETTINGS:
            changed = cls._set_int_setting(setting_name, value)
        return changed

    @classmethod
    def _set_int_setting(cls, setting_name: str, value: str) -> bool:
        try:
            value = int(value)
        except ValueError:
            return False

        if value not in cls.NUMBER_SETTINGS[setting_name]:
            return False
        setattr(cls, setting_name, value)
        return True

    @classmethod
    def _set_bool_setting(cls, setting_name: str, boolean: str) -> bool:
        if boolean.lower() != "false" and boolean.lower() != "true":
            return False

        if boolean.lower() == "true":
            setattr(cls, setting_name, True)
        elif boolean.lower() == "false":
            setattr(cls, setting_name, False)

        return True
