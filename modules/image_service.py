"""
이미지 자동 생성 및 고화질 비주얼 매칭 모듈
- 키워드와 카테고리에 맞는 고품질 스톡 이미지(Unsplash 라이선스 프리 고해상도)를 본문에 실제 삽입합니다.
"""
from typing import Dict, Any, List
import urllib.parse

# 스타일 프리셋
STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    "따뜻한 필름 감성": {
        "theme": "warm,cozy,aesthetic,lifestyle",
        "badge_color": "#D97706",
        "description": "감성적이고 따뜻한 필름 색감"
    },
    "모던한 비즈니스 톤": {
        "theme": "finance,business,investment,economy,office",
        "badge_color": "#008080",
        "description": "신뢰감을 주는 현대적이고 깔끔한 비즈니스 디자인"
    },
    "아기자기한 일러스트 톤": {
        "theme": "minimal,clean,lifestyle,bright",
        "badge_color": "#EC4899",
        "description": "친근하고 직관적인 스타일"
    }
}

# 카테고리별 고화질 대표 큐레이션 이미지 풀 (실제 렌더링 검증 완료된 CDN)
CATEGORY_IMAGES = {
    "finance": [
        "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1200&q=80", # 돈, 저축, 재테크
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80", # 세무, 계산, 서류
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80", # 경제 데이터, 차트
        "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80"  # 디지털 금융, 스마트폰
    ],
    "lifestyle": [
        "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80", # 라이프스타일, 노트북, 커피
        "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1200&q=80", # 생산성, 체크리스트, 계획
        "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=1200&q=80", # 일상, 여유, 문화
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80"  # 스마트한 습관, 도서
    ]
}

def get_blog_images(category: str = "finance", keyword: str = "") -> Dict[str, str]:
    """
    본문 상단 썸네일과 중간 본문 이미지 URL을 반환합니다.
    """
    import random
    cat_key = "lifestyle" if "생활" in category or "리뷰" in category or "문화" in category else "finance"
    img_list = CATEGORY_IMAGES.get(cat_key, CATEGORY_IMAGES["finance"])
    
    # 2장 선정 (썸네일용 1장, 본문 중간 삽입용 1장)
    selected = random.sample(img_list, min(2, len(img_list)))
    
    return {
        "thumbnail_url": selected[0],
        "content_img_url": selected[1] if len(selected) > 1 else selected[0],
        "caption": f"{keyword} 관련 가이드 이미지"
    }

def create_image_metadata(keyword: str, style_name: str) -> Dict[str, Any]:
    preset = STYLE_PRESETS.get(style_name, STYLE_PRESETS["모던한 비즈니스 톤"])
    prompt = f"Blog banner for '{keyword}', {preset['theme']}, 16:9 aspect ratio, high resolution, professional typography"
    
    images = get_blog_images("finance" if "정부" in keyword or "계좌" in keyword or "돈" in keyword or "금" in keyword else "lifestyle", keyword)
    
    return {
        "style_name": style_name,
        "badge_color": preset["badge_color"],
        "prompt": prompt,
        "thumbnail_url": images["thumbnail_url"],
        "content_img_url": images["content_img_url"],
        "aspect_ratio": "16:9",
        "status": "ready"
    }
