"""
블로그 콘텐츠 생성 모듈 (리치유니 맞춤형 템플릿 적용)
"""
from datetime import datetime
from typing import Dict, Any

def generate_blog_content(keyword: str, image_style: str) -> Dict[str, Any]:
    """
    키워드와 이미지 스타일을 바탕으로 구조화된 블로그 글을 생성합니다.
    - 리치유니 맞춤 스타일: 이탤릭(기울임) 없음, 핵심 키워드 굵기(Bold) 및 테마 컬러 포인트 강조
    """
    cleaned_keyword = keyword.strip()
    current_year = datetime.now().year
    
    title = f"[{current_year} 최신분석] {cleaned_keyword} 핵심 총정리 및 필수 체크포인트"
    
    # 본문 구성 (HTML/마크다운 혼합 - 블로그 플랫폼 및 다크/라이트 모드 완벽 호환)
    body_html = f"""
<div style="color: #222222; font-size: 15px; line-height: 1.75;">
<h2 style="color: #111111; margin-top: 10px;">📌 1. 들어가며: {cleaned_keyword}이란?</h2>
<p style="color: #333333;">최근 많은 분들이 주목하고 계시는 <b><span style="color:#008080;">{cleaned_keyword}</span></b>에 대해 가장 핵심적인 내용만 알기 쉽게 정리해 드립니다.</p>
<p style="color: #333333;">정보가 방대하여 혼란스러우셨다면, 본 포스팅의 핵심 요약과 단계별 안내를 차근차근 확인해 보세요.</p>

<hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

<h2 style="color: #111111;">🎯 2. {cleaned_keyword} 핵심 요약 및 주요 변경점</h2>
<ul style="color: #333333;">
    <li><b>지원 대상 및 조건:</b> 최신 공고 기준 세부 자격 요건 충족 필수</li>
    <li><b>핵심 혜택:</b> 놓치기 쉬운 우대 사항 및 실질적 혜택 중심 확인</li>
    <li><b>신청 및 접수 시기:</b> 마감 전 사전 서류 준비 권장</li>
</ul>

<div style="background-color: #f0fdfa; border-left: 4px solid #008080; padding: 15px; margin: 15px 0; border-radius: 4px; color: #134e4a;">
    <b>💡 리치유니 핵심 포인트 TIP:</b><br>
    <b><span style="color:#008080;">{cleaned_keyword}</span></b> 진행 시 가장 중요한 점은 기한 내 누락 없는 서류 제출입니다. 사전 체크리스트를 반드시 확인하시기 바랍니다.
</div>

<h2 style="color: #111111;">🚀 3. 단계별 신청 및 진행 방법</h2>
<ol style="color: #333333;">
    <li>공식 홈페이지 또는 지정 창구 접속 및 본인 인증</li>
    <li><b>{cleaned_keyword}</b> 대상자 여부 조회 및 사전 자격 검증</li>
    <li>필요 서류 구비 후 온라인 또는 방문 접수 완료</li>
    <li>심사 결과 확인 및 확정 안내 수령</li>
</ol>

<h2 style="color: #111111;">❓ 4. 자주 묻는 질문 (FAQ)</h2>
<p style="color: #333333;"><b>Q1. 이전 신청 이력이 있어도 재신청이 가능한가요?</b><br>
A. 세부 자격 요건 및 규정에 따라 상이하므로 해당 기관의 최신 지침을 재확인해야 합니다.</p>

<p style="color: #333333;"><b>Q2. 제출 서류 유효기간은 어떻게 되나요?</b><br>
A. 통상 발급일로부터 1개월~3개월 이내의 최신 서류를 권장합니다.</p>

<hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

<p style="text-align: right; color: #888888; font-size: 13px;">발행일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>
""".strip()

    tags = [cleaned_keyword.replace(" ", ""), "정보공유", "최신가이드", "핵심요약", "블로그자동화"]
    
    return {
        "title": title,
        "content": body_html,
        "keyword": cleaned_keyword,
        "image_style": image_style,
        "tags": tags,
        "created_at": datetime.now().isoformat()
    }

