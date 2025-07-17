from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    openai_key: str
    model: str
    base_url: str

    class Config:
        env_file = '.env'


class Settings(BaseSettings):
    app_title: str = 'Fake News Detector'
    app_description: str = 'Custom utility to validate whether your source is fake or not'


open_api_setting = OpenAISettings()
settings = Settings()
