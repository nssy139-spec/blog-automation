"""
클라우드 완전 무인 자동 포스팅 러너 (GitHub Actions 크론용)
- 컴퓨터가 꺼져 있어도 클라우드 서버가 매일 정해진 시간에 이 스크립트를 실행합니다.
"""
import os
import random
from datetime import datetime
from config import Config
from modules.logger import setup_logger
from modules.generator import generate_blog_content
from modules.image_service import create_image_metadata, STYLE_PRESETS
from modules.publisher import publish_to_naver_email, publish_to_tistory

logger = setup_logger("cloud_runner")

# 자동 발행용 추천 키워드 풀 (매일 자동으로 최신 글감 순환)
AUTO_KEYWORD_POOL = [
    "2026년 하반기 정부지원금 혜택 총정리",
    "2026년 청년 도약 계좌 신청 조건 및 우대금리",
    "직장인을 위한 연말정산 절세 꿀팁 가이드",
    "2026년 소상공인 정책자금 신청 절차 및 필수 서류",
    "AI 기반 업무 생산성 극대화 추천 도구 BEST 5",
    "스마트한 재테크 초보자를 위한 월급 관리 루틴"
]

def run_automated_pipeline():
    logger.info("=== [클라우드 무인 자동 발행 파이프라인 가동] ===")
    
    # 1. 오늘의 키워드 선정 (환경변수로 지정되거나 키워드 풀에서 자동 선택)
    target_keyword = os.getenv("CUSTOM_KEYWORD", "").strip()
    if not target_keyword:
        target_keyword = random.choice(AUTO_KEYWORD_POOL)
    
    # 2. 이미지 스타일 선정
    style_names = list(STYLE_PRESETS.keys())
    selected_style = random.choice(style_names)
    
    logger.info(f"오늘의 주제: [{target_keyword}] | 스타일: [{selected_style}]")

    # 3. 리치유니 맞춤형 콘텐츠 생성
    blog_data = generate_blog_content(keyword=target_keyword, image_style=selected_style)
    logger.info(f"콘텐츠 생성 완료 - 제목: {blog_data['title']}")

    # 4. 네이버 블로그 자동 발행 시도
    naver_id = os.getenv("NAVER_ID", Config.NAVER_ID)
    naver_pw = os.getenv("NAVER_PW", Config.NAVER_PW)
    naver_blog_id = os.getenv("NAVER_BLOG_ID", Config.NAVER_BLOG_ID) or naver_id

    if naver_id and naver_pw:
        logger.info(f"네이버 블로그 발행 시작 ({naver_id})")
        res_naver = publish_to_naver_email(
            naver_id=naver_id,
            naver_password=naver_pw,
            title=blog_data["title"],
            content_html=blog_data["content"],
            blog_id=naver_blog_id
        )
        if res_naver.get("success"):
            logger.info(f"🎉 네이버 블로그 자동 발행 성공! URL: {res_naver.get('post_url')}")
        else:
            logger.warning(f"⚠️ 네이버 발행 실패: {res_naver.get('message')}")
    else:
        logger.info("네이버 인증 정보가 설정되지 않아 발행을 건너뜁니다.")

    # 5. 티스토리 자동 발행 시도
    t_token = os.getenv("TISTORY_ACCESS_TOKEN", Config.TISTORY_ACCESS_TOKEN)
    t_name = os.getenv("TISTORY_BLOG_NAME", Config.TISTORY_BLOG_NAME)

    if t_token and t_name:
        logger.info(f"티스토리 자동 발행 시작 ({t_name})")
        res_tistory = publish_to_tistory(
            access_token=t_token,
            blog_name=t_name,
            title=blog_data["title"],
            content=blog_data["content"],
            visibility=3, # 즉시 공개
            tags=blog_data.get("tags")
        )
        if res_tistory.get("success"):
            logger.info(f"🎉 티스토리 자동 발행 성공! URL: {res_tistory.get('post_url')}")
        else:
            logger.warning(f"⚠️ 티스토리 발행 실패: {res_tistory.get('message')}")
    else:
        logger.info("티스토리 인증 정보가 설정되지 않아 발행을 건너뜁니다.")

    logger.info("=== [클라우드 무인 자동 발행 완료] ===")

if __name__ == "__main__":
    run_automated_pipeline()

