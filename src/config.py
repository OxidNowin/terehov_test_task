from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str
    redis_port: str
    redis_index: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_index}"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
