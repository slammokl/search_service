from pydantic_settings import BaseSettings, SettingConfigDict 

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncio://postgres:postgres@localhost:5432/posts" 
    elasticsearch_url: str = "http://localhost:9200" 
    index_name: str = "posts" 

    model_config = SettingConfigDict(env_file=".env", extra="ignore") 

settings = Settings() 