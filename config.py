from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_title: str = 'Fake News Detector'
    app_description: str = 'Custom utility to validate whether your source is fake or not'

    openai_key: str = ''
    model: str = 'gpt-4'
    base_url: str = 'https://api.openai.com/v1'

    max_concurrency_limit: int = 5

    max_search_results: int = 5

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
