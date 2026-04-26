from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Farfor MVP API'
    secret_key: str = 'change-me'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24

    database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/farfor'

    s3_endpoint_url: str | None = None
    s3_region: str = 'us-east-1'
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_bucket: str = 'farfor-media'
    media_base_url: str = 'http://localhost:8000/media'


settings = Settings()
