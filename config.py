from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    openai_key: str
    model: str
    base_url: str

    model_config = SettingsConfigDict(env_file='.env')

class ConcurrencyLimit(BaseSettings):
    max_limit: int = 5

class SearchConfig(BaseSettings):
    max_search: int = 5

class Settings(BaseSettings):
    app_title: str = 'Fake News Detector'
    app_description: str = 'Custom utility to validate whether your source is fake or not'



def get_openai_settings():
    return OpenAISettings()


settings = Settings()
