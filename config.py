import os
from dotenv import load_dotenv

# .env 파일이 존재하는 경우 로드
load_dotenv()

class Config:
    NAVER_ID = os.getenv("NAVER_ID", "")
    NAVER_PW = os.getenv("NAVER_PW", "")
    NAVER_BLOG_ID = os.getenv("NAVER_BLOG_ID", "")
    
    TISTORY_ACCESS_TOKEN = os.getenv("TISTORY_ACCESS_TOKEN", "")
    TISTORY_BLOG_NAME = os.getenv("TISTORY_BLOG_NAME", "")
    SERVER_PORT = int(os.getenv("PORT", 8501))
