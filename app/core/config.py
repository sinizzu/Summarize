import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Summarize"
    PROJECT_VERSION: str = "1.0.0"

    # 데이터베이스 설정
    #DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Weaviate 설정
    WEAVIATE_URL: str = os.getenv("WCS_URL")
    WEAVIATE_API_KEY: str = os.getenv("WCS_API_KEY")

    # 외부 API 키 설정
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TEXTRAZOR_API_KEY: str = os.getenv("TEXTRAZOR_API_KEY")
    DEEPL_AUTH_KEY: str = os.getenv("DEEPL_AUTH_KEY")
    
    # google search 설정
    API_KEY = os.getenv("CUSTOM_SEARCH_API")
    CX = os.getenv("GOOGLE_CX")
    
    # Main FastAPI
    MainFastAPI = os.getenv("MainFastAPI")
    
    # Frontend
    MainFrontend = os.getenv("MainFrontend")
    HJFrontend = os.getenv("HJFrontend")
    JHFrontend = os.getenv("JHFrontend")

    # 애플리케이션 모드
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
