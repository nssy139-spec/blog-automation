"""
블로그 콘텐츠 생성 모듈 (리치유니 맞춤형 템플릿 + 실제 이미지 삽입 엔진)
- 재테크/경제 및 생활/문화/리뷰 멀티 카테고리 지원
"""
from datetime import datetime
from typing import Dict, Any, Optional
from modules.image_service import get_blog_images

CATEGORY_MAP = {
    "finance": "재테크·경제",
    "lifestyle": "생활·문화·리뷰"
}

def generate_blog_content(
    keyword: str,
    image_style: str = "모던한 비즈니스 톤",
    category: str = "finance"
) -> Dict[str, Any]:
    """
    키워드, 스타일, 카테고리를 바탕으로 고화질 이미지가 삽입된 블로그 글을 생성합니다.
    """
    cleaned_keyword = keyword.strip()
    current_year = datetime.now().year
    
    # 카테고리 판별
    is_finance = "finance" in category or "경제" in category or "재테크" in category
    category_name = "재테크·경제" if is_finance else "생활·문화·리뷰"
    
    # 고화질 이미지 2장 준비 (상단 대표 썸네일 + 본문 중간 이미지)
    images = get_blog_images(category=category_name, keyword=cleaned_keyword)
    thumb_url = images["thumbnail_url"]
    mid_img_url = images["content_img_url"]

    # 카테고리별 맞춤 제목
    if is_finance:
        title = f"[{current_year} 최신분석] {cleaned_keyword} 핵심 총정리 및 필수 체크포인트"
        sub_intro = f"최근 많은 분들이 주목하고 계시는 <b><span style='color:#008080;'>{cleaned_keyword}</span></b>에 대해 경제적 혜택과 신청 자격 중심으로 가장 핵심적인 내용만 알기 쉽게 정리해 드립니다."
        tip_title = f"{cleaned_keyword} 진행 시 핵심 TIP"
        tip_body = f"<b><span style='color:#008080;'>{cleaned_keyword}</span></b> 진행 시 가장 중요한 점은 기한 내 누락 없는 사전 서류 준비와 우대금리/지원 조건을 꼼꼼히 대조하는 것입니다."
    else:
        title = f"[{current_year} 알짜리뷰] {cleaned_keyword} 직접 알아본 솔직 꿀팁 및 활용법"
        sub_intro = f"일상의 편리함을 한 단계 올려주는 <b><span style='color:#008080;'>{cleaned_keyword}</span></b>에 대해 바쁜 일상 속 꼭 알아두면 유익한 정보와 실사용 팁을 알기 쉽게 전해드립니다."
        tip_title = f"{cleaned_keyword} 200% 활용 꿀팁"
        tip_body = f"<b><span style='color:#008080;'>{cleaned_keyword}</span></b>을(를) 활용할 때는 나의 생활 패턴에 맞춰 불필요한 지출과 시간을 줄이는 루틴을 만들어 두는 것이 가장 효과적입니다."

    # 본문 구성 (HTML - 네이버 블로그/티스토리 모두 100% 호환되는 인라인 이미지 포함)
    body_html = f"""
<div style="color: #222222; font-size: 16px; line-height: 1.8; font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;">

    <!-- 1. 상단 대표 썸네일 이미지 -->
    <div style="text-align: center; margin: 20px 0 30px 0;">
        <img src="{thumb_url}" alt="{cleaned_keyword}" style="width: 100%; max-width: 680px; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);" />
        <p style="color: #888888; font-size: 13px; margin-top: 8px;">▲ {cleaned_keyword} 핵심 가이드</p>
    </div>

    <!-- 2. 도입부 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 25px;">
        📌 1. 들어가며: {cleaned_keyword}이란?
    </h2>
    <p style="color: #333333; margin-top: 14px;">{sub_intro}</p>
    <p style="color: #333333;">정보가 방대하여 혼란스러우셨다면, 본 포스팅의 핵심 요약과 단계별 체크리스트를 차근차근 확인해 보세요.</p>

    <hr style="border: 0; height: 1px; background: #e5e7eb; margin: 30px 0;">

    <!-- 3. 핵심 요약 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px;">
        🎯 2. {cleaned_keyword} 주요 핵심 내용 및 요약
    </h2>
    <ul style="color: #333333; margin-top: 14px; padding-left: 20px;">
        <li style="margin-bottom: 8px;"><b>핵심 대상 및 기준:</b> 최신 공고 기준 주요 자격 요건 및 대상자 확인 필수</li>
        <li style="margin-bottom: 8px;"><b>놓치기 쉬운 혜택:</b> 추가 우대 혜택 및 실질적 체감 효용 중심 점검</li>
        <li style="margin-bottom: 8px;"><b>접수 및 신청 기간:</b> 기한 마감 전 사전 구비 서류 준비 권장</li>
    </ul>

    <!-- 리치유니 시그니처 틸 컬러 강조 박스 -->
    <div style="background-color: #f0fdfa; border-left: 5px solid #008080; padding: 18px 20px; margin: 25px 0; border-radius: 6px; color: #134e4a;">
        <b style="font-size: 16px;">💡 리치유니 핵심 포인트 TIP:</b><br>
        <span style="display:inline-block; margin-top:6px;">{tip_body}</span>
    </div>

    <!-- 4. 본문 중간 이미지 -->
    <div style="text-align: center; margin: 30px 0;">
        <img src="{mid_img_url}" alt="{cleaned_keyword} 상세 안내" style="width: 100%; max-width: 680px; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);" />
        <p style="color: #888888; font-size: 13px; margin-top: 8px;">▲ 단계별 핵심 체크포인트</p>
    </div>

    <!-- 5. 단계별 가이드 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px;">
        🚀 3. 단계별 실천 및 진행 순서
    </h2>
    <ol style="color: #333333; margin-top: 14px; padding-left: 20px;">
        <li style="margin-bottom: 8px;">공식 웹사이트 또는 지정 모바일 앱 접속 및 본인 인증</li>
        <li style="margin-bottom: 8px;"><b>{cleaned_keyword}</b> 세부 요건 및 지원 대상 여부 사전 모의 조회</li>
        <li style="margin-bottom: 8px;">필요 서류 및 증빙 자료 확인 후 최종 접수 제출</li>
        <li style="margin-bottom: 8px;">승인 결과 통보 수령 및 후속 조치 이행</li>
    </ol>

    <!-- 6. 자주 묻는 질문 FAQ -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 30px;">
        ❓ 4. 자주 묻는 질문 (FAQ)
    </h2>
    <div style="margin-top: 14px; background: #fafafa; padding: 16px; border-radius: 8px;">
        <p style="color: #111111; margin-bottom: 6px;"><b>Q1. 기존에 이미 혜택을 받은 이력이 있어도 재신청이 가능한가요?</b></p>
        <p style="color: #555555; margin-bottom: 14px;">A. 항목별 세부 규정 및 공고 지침에 따라 상이하므로 해당 기관의 최신 지침을 재확인해야 합니다.</p>
        <p style="color: #111111; margin-bottom: 6px;"><b>Q2. 제출 서류의 유효기간은 어떻게 되나요?</b></p>
        <p style="color: #555555; margin-bottom: 0;">A. 통상 발급일로부터 1개월~3개월 이내의 서류 제출이 권장됩니다.</p>
    </div>

    <hr style="border: 0; height: 1px; background: #e5e7eb; margin: 30px 0;">

    <p style="text-align: right; color: #888888; font-size: 13px;">발행일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>
""".strip()

    tags = [
        cleaned_keyword.replace(" ", ""),
        category_name.split("·")[0],
        "정보공유",
        "핵심요약",
        "리치유니블로그"
    ]

    return {
        "title": title,
        "content": body_html,
        "keyword": cleaned_keyword,
        "category": category_name,
        "image_style": image_style,
        "thumbnail_url": thumb_url,
        "mid_img_url": mid_img_url,
        "tags": tags,
        "created_at": datetime.now().isoformat()
    }
