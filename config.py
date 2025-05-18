from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # OpenAI API 설정
    OPENAI_API_KEY: str
    
    # 카카오톡 API 설정
    KAKAO_API_KEY: Optional[str] = None
    
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./news_bot.db"
    
    # 크롤링 설정
    CRAWL_INTERVAL_MINUTES: int = 60
    NEWS_CATEGORIES: list[str] = ["경제", "사회", "정치", "국제"]
    
    # 메시지 설정
    MAX_SUMMARY_LENGTH: int = 200
    MAX_KEYWORDS: int = 5
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 