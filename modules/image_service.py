"""
이미지 스타일 및 프롬프트 생성 모듈
"""
from typing import Dict, Any

STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    "따뜻한 필름 감성": {
        "theme": "warm film photography, 35mm aesthetic, soft natural lighting, pastel tone",
        "badge_color": "#D97706",
        "description": "감성적이고 따뜻한 필름 색감의 썸네일"
    },
    "모던한 비즈니스 톤": {
        "theme": "clean minimal business graphic, corporate modern, sharp contrasts, deep navy & teal",
        "badge_color": "#0D9488",
        "description": "신뢰감을 주는 현대적이고 깔끔한 비즈니스 디자인"
    },
    "아기자기한 일러스트 톤": {
        "theme": "cute flat 2D vector illustration, vibrant friendly colors, cozy design",
        "badge_color": "#EC4899",
        "description": "친근하고 직관적인 플랫 일러스트 스타일"
    }
}

def create_image_metadata(keyword: str, style_name: str) -> Dict[str, Any]:
    preset = STYLE_PRESETS.get(style_name, STYLE_PRESETS["모던한 비즈니스 톤"])
    
    prompt = f"Blog banner for '{keyword}', {preset['theme']}, 16:9 aspect ratio, high resolution, professional typography"
    
    return {
        "style_name": style_name,
        "badge_color": preset["badge_color"],
        "prompt": prompt,
        "description": preset["description"],
        "aspect_ratio": "16:9",
        "status": "ready"
    }

