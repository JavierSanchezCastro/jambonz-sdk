from pydantic_settings import BaseSettings, SettingsConfigDict


class JambonzSettings(BaseSettings):
    account_sid: str
    api_key: str
    base_url: str = "https://api.jambonz.cloud"
    timeout: float = 30.0
    max_retries: int = 3

    model_config = SettingsConfigDict(env_prefix="JAMBONZ_", env_file=".env")
