import os
from dotenv import load_dotenv

# .env 파일이 존재하는 경우 로드
load_dotenv()

class Config:
    # 네이버 블로그 계정
    NAVER_ID = os.getenv("NAVER_ID", "ssy139")
    NAVER_PW = os.getenv("NAVER_PW", "")
    NAVER_BLOG_ID = os.getenv("NAVER_BLOG_ID", "ssy139")
    
    # 카카오 / 티스토리 계정 (100% 무인 자동 로그인용)
    KAKAO_ID = os.getenv("KAKAO_ID", "")
    KAKAO_PW = os.getenv("KAKAO_PW", "")
    TISTORY_BLOG_NAME = os.getenv("TISTORY_BLOG_NAME", "essay0606")
    
    SERVER_PORT = int(os.getenv("PORT", 8501))
