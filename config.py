from pydantic_settings import BaseSettings


class OpenAPISettings(BaseSettings):
    openapi_key: str

    class Config:
        env_file = '.env'


class Settings(BaseSettings):
    app_title: str = 'Fake News Detector'
    app_description: str = 'Custom utility to validate whether your source is fake or not'
