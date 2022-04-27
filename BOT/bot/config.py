from typing import Union

from pydantic import BaseModel, Field

from . import root_path


class BaseBotConfig(BaseModel):
    __config_filenames__ = ("_config_dev.json", "config.json")

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")

    @classmethod
    def load_any(cls):
        for filepath in cls.__config_filepaths__():
            if filepath.exists():
                return cls.parse_file(filepath)

    @classmethod
    def __config_filepaths__(cls):
        for filename in cls.__config_filenames__:
            yield root_path / filename


class OrmConfig(BaseModel):
    database_url: str = Field("sqlite://{sqlite_path}")


class RegistrationConfig(BaseModel):
    registration_channel_id: Union[int, str] = Field(
        "ID канала, в который пишут участники"
    )
    bot_send_channel_id: Union[int, str] = Field("ID канала, в который пишет бот")
    registration_role_id: Union[int, str] = Field(
        "ID роли, которую выдавать после регистрации"
    )


class BotConfig(BaseBotConfig):
    registration: RegistrationConfig = Field(RegistrationConfig())
    database: OrmConfig = Field(OrmConfig())
