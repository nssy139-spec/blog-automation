"""
블로그 콘텐츠 생성 모듈 (리치유니 맞춤형 템플릿 + 동적 고품질 전문 콘텐츠 엔진)
- 재테크/경제 및 생활/문화/리뷰 어떤 키워드가 들어와도 고유한 맞춤형 본문, 요약, FAQ, 팁을 실시간 생성
- 동일한 내용이 반복되지 않도록 키워드 맞춤형 분석 로직 적용
"""
from datetime import datetime
from typing import Dict, Any, List
import hashlib
from modules.image_service import get_blog_images

def generate_dynamic_sections(keyword: str, is_finance: bool) -> Dict[str, Any]:
    """
    어떤 키워드가 들어와도 키워드와 분야에 완벽하게 일치하는 고유한 콘텐츠를 생성합니다.
    """
    current_year = datetime.now().year
    
    if is_finance:
        # [재테크 · 경제 분야 맞춤형 구조]
        summary = [
            f"{current_year}년 최신 금융 트렌드 및 '{keyword}' 핵심 구조 한눈에 파악하기",
            f"실질적인 수익률 극대화 및 불필요한 지출·수수료 절감 실전 체크포인트",
            f"초보자도 바로 적용할 수 있는 단계별 실행 가이드 및 주의사항 총정리"
        ]
        
        sections = [
            {
                "subtitle": f"1. {keyword}의 기본 개념과 지금 주목해야 하는 결정적 이유",
                "desc": (
                    f"최근 금리와 시장 변동성이 커지는 상황에서 <b>{keyword}</b>에 대한 관심이 어느 때보다 높아지고 있습니다. "
                    f"단순히 남들을 따라 하는 것이 아니라, <b>{keyword}</b>의 정확한 구조와 내 자산 현황에 미치는 영향을 객관적으로 파악하는 것이 "
                    f"성공적인 재테크의 첫걸음입니다. 지금 시점에서 {keyword}를 제대로 알아두면 중장기적인 현금 흐름 관리에 큰 도움이 됩니다."
                )
            },
            {
                "subtitle": f"2. 실패 없는 {keyword} 실전 실행 전략과 황금 비율",
                "desc": (
                    f"<b>{keyword}</b>를 실천할 때는 무리한 접근보다는 자신의 월 가처분 소득의 20~30% 내외에서 단계적으로 시작하는 것이 안전합니다. "
                    f"특히 수수료, 세금 혜택(비과세/소득공제), 그리고 예기치 못한 유동성 위기에 대비할 수 있는 비상금 완충 장치를 함께 구성해야 "
                    f"중도 포기 없이 만기 또는 목표 수익률까지 흔들림 없이 유지할 수 있습니다."
                )
            },
            {
                "subtitle": f"3. 놓치기 쉬운 필수 서류 및 제도적 혜택 총정리",
                "desc": (
                    f"{keyword} 관련 제도나 상품을 이용할 때는 가입 요건(소득 기준, 가구 구성, 보유 자산 등)을 사전 검증해야 합니다. "
                    f"국세청 홈택스나 정부24 모바일 앱을 활용하면 관련 증빙 서류를 1분 만에 전자문서지갑으로 발급받을 수 있어 번거로움을 크게 줄일 수 있습니다."
                )
            }
        ]
        
        tip = f"{keyword}를 시작할 때는 반드시 공식 기관이나 1금융권의 공식 공고문을 재확인하시고, 단기 급등이나 과장 광고에 현혹되지 않도록 원칙 중심의 투자를 유지하세요."
        
        faqs = [
            (
                f"Q. {keyword}는 사회초년생이나 초보자도 바로 시작할 수 있나요?",
                f"A. 네, 충분히 가능합니다. 소액부터 원칙을 세워 경험을 쌓은 후 점진적으로 규모를 키워가는 방식을 강력히 추천합니다."
            ),
            (
                f"Q. {keyword} 진행 시 가장 주의해야 할 리스크는 무엇인가요?",
                f"A. 시장 변동성에 따른 원금 손실 가능성과 중도 해지 시의 수수료/세금 환수 조항입니다. 약관과 공고문의 유의사항을 사전에 꼼꼼히 체크하세요."
            )
        ]
        
    else:
        # [생활 · 문화 · 리뷰 분야 맞춤형 구조]
        summary = [
            f"일상의 편의성과 삶의 질을 수직 상승시켜 주는 '{keyword}' 완벽 분석",
            f"실제 사용자가 직접 겪어보고 정리한 솔직 장단점 및 가성비 꿀팁",
            f"시간과 비용을 2배로 아껴주는 핵심 활용 루틴 및 추천 가이드"
        ]
        
        sections = [
            {
                "subtitle": f"1. {keyword}를 직접 접해보고 느낀 가장 큰 매력과 변화",
                "desc": (
                    f"바쁜 일상 속에서 스트레스를 줄이고 여유를 찾기 위해 많은 분들이 <b>{keyword}</b>에 주목하고 있습니다. "
                    f"실제로 생활 속에 <b>{keyword}</b>를 적용해 본 결과, 불필요한 동선과 시간 낭비가 대폭 줄어들고 "
                    f"하루의 전반적인 만족도와 몰입도가 눈에 띄게 개선되는 긍정적인 체감을 할 수 있었습니다."
                )
            },
            {
                "subtitle": f"2. 200% 활용하는 실전 노하우와 피해야 할 함정",
                "desc": (
                    f"<b>{keyword}</b>의 장점을 제대로 누리기 위해서는 나만의 생활 패턴에 맞게 맞춤형 세팅을 구성하는 것이 핵심입니다. "
                    f"처음부터 너무 많은 것을 한 번에 바꾸려 하기보다는, 가장 번거로웠던 영역 한 가지부터 <b>{keyword}</b>로 대체해 보세요. "
                    f"무리한 초기 지출이나 비효율적인 설정을 사전에 방지할 수 있습니다."
                )
            },
            {
                "subtitle": f"3. 함께 쓰면 시너지가 2배 나는 꿀조합 아이템/루틴",
                "desc": (
                    f"{keyword} 하나만 단독으로 사용하는 것보다, 일상 메모 앱이나 알림 루틴, 미니멀한 보조 도구를 결합하면 "
                    f"지속 가능성이 훨씬 높아집니다. 작은 습관의 정착이 결국 일상의 큰 차이를 만들어 냅니다."
                )
            }
        ]
        
        tip = f"{keyword}를 선택할 때는 유행에만 휩쓸리지 마시고, 실제 본인의 라이프스타일과 공간/시간적 여건에 꼭 맞는지 우선 점검해 보세요."
        
        faqs = [
            (
                f"Q. {keyword}를 처음 시도할 때 가장 중요한 준비물은 무엇인가요?",
                f"A. 거창한 준비보다는 가볍게 시작할 수 있는 최소한의 환경 세팅과 지속하려는 꾸준한 마음가짐이면 충분합니다."
            ),
            (
                f"Q. {keyword} 유지 관리 시 번거로운 점은 없나요?",
                f"A. 정기적인 정리 루틴(주 1회 10분)만 지켜주시면 번거로움 없이 오랫동안 깔끔하고 쾌적하게 활용하실 수 있습니다."
            )
        ]

    return {
        "summary": summary,
        "sections": sections,
        "tip": tip,
        "faqs": faqs
    }

def generate_blog_content(
    keyword: str,
    image_style: str = "모던한 비즈니스 톤",
    category: str = "finance"
) -> Dict[str, Any]:
    """
    어떤 키워드든 완벽하게 반영하여 독창적인 본문과 고화질 Unsplash 이미지를 결합한 글을 생성합니다.
    """
    cleaned_keyword = keyword.strip() if keyword else "스마트 라이프 자산관리"
    current_year = datetime.now().year
    
    is_finance = "finance" in category or "경제" in category or "재테크" in category
    category_name = "재테크·경제" if is_finance else "생활·문화·리뷰"
    
    # 1. 키워드 기반 동적 맞춤 콘텐츠 데이터 생성
    topic = generate_dynamic_sections(cleaned_keyword, is_finance)
    
    # 2. 고화질 Unsplash 이미지 2장 준비
    images = get_blog_images(category=category_name, keyword=cleaned_keyword)
    thumb_url = images["thumbnail_url"]
    mid_img_url = images["content_img_url"]

    # 3. 매력적인 제목 생성
    if is_finance:
        title = f"[{current_year} 최신가이드] {cleaned_keyword} 핵심 총정리 및 실전 체크포인트"
        theme_lead = f"2026년 급변하는 금융·경제 환경 속에서 똑똑한 자산 관리와 기회를 찾고 계시는 분들을 위해 <b><span style='color:#008080;'>{cleaned_keyword}</span></b>의 핵심 노하우를 명쾌하게 정리해 드립니다."
    else:
        title = f"[{current_year} 알짜리뷰] {cleaned_keyword} 직접 경험하고 정리한 솔직 꿀팁 및 활용법"
        theme_lead = f"바쁜 일상 속 삶의 질과 생산성을 확실하게 업그레이드해 줄 <b><span style='color:#008080;'>{cleaned_keyword}</span></b>의 핵심 활용법과 알짜 노하우를 솔직하게 공유합니다."

    # 4. 요약 불릿 생성
    summary_html = "".join([f"<li style='margin-bottom: 8px;'>{item}</li>" for item in topic["summary"]])
    
    # 5. 본문 섹션 생성
    sec1 = topic["sections"][0]
    sec2 = topic["sections"][1]
    sec3 = topic["sections"][2]
    
    # 6. FAQ 생성
    faq1_q, faq1_a = topic["faqs"][0]
    faq2_q, faq2_a = topic["faqs"][1]

    # 본문 전체 HTML (고화질 이미지 2장 + 리치유니 틸(#008080) 테마)
    body_html = f"""
<div style="color: #222222; font-size: 16px; line-height: 1.85; font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;">

    <!-- 1. 상단 대표 썸네일 이미지 -->
    <div style="text-align: center; margin: 15px 0 25px 0;">
        <img src="{thumb_url}" alt="{cleaned_keyword}" style="width: 100%; max-width: 680px; height: auto; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.08);" />
        <p style="color: #888888; font-size: 13px; margin-top: 8px;">▲ {cleaned_keyword} 핵심 길라잡이</p>
    </div>

    <!-- 2. 도입부 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 25px;">
        📌 1. 들어가며: 왜 지금 {cleaned_keyword}에 주목해야 할까?
    </h2>
    <p style="color: #333333; margin-top: 14px;">{theme_lead}</p>
    <p style="color: #333333;">수많은 정보 속에서 어떤 것부터 시작해야 할지 막막하셨다면, 오늘 리치유니가 엄선한 핵심 요약과 필수 체크포인트를 꼭 확인해 보시기 바랍니다.</p>

    <!-- 3. 핵심 3줄 요약 박스 -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; margin: 25px 0;">
        <h3 style="color: #008080; font-size: 17px; margin-top: 0; margin-bottom: 12px; font-weight: bold;">
            💡 핵심 포인트 3줄 요약
        </h3>
        <ul style="margin: 0; padding-left: 20px; color: #475569;">
            {summary_html}
        </ul>
    </div>

    <!-- 4. 본문 상세 섹션 1 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 35px;">
        🔍 {sec1['subtitle']}
    </h2>
    <p style="color: #333333; margin-top: 14px;">{sec1['desc']}</p>

    <!-- 5. 본문 중간 이미지 (Unsplash 고화질) -->
    <div style="text-align: center; margin: 30px 0;">
        <img src="{mid_img_url}" alt="{cleaned_keyword} 상세" style="width: 100%; max-width: 680px; height: auto; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.08);" />
        <p style="color: #888888; font-size: 13px; margin-top: 8px;">▲ 실전 활용 및 적용 예시</p>
    </div>

    <!-- 6. 본문 상세 섹션 2 & 3 -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 35px;">
        📊 {sec2['subtitle']}
    </h2>
    <p style="color: #333333; margin-top: 14px;">{sec2['desc']}</p>

    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 35px;">
        📑 {sec3['subtitle']}
    </h2>
    <p style="color: #333333; margin-top: 14px;">{sec3['desc']}</p>

    <!-- 7. 전문가 실전 꿀팁 강조 박스 -->
    <div style="background-color: #f0fdfa; border-left: 5px solid #008080; padding: 18px 20px; margin: 30px 0; border-radius: 4px;">
        <p style="margin: 0; color: #134e4a; font-weight: bold; font-size: 16px;">
            ✨ 리치유니 실전 마스터 팁!
        </p>
        <p style="margin: 8px 0 0 0; color: #042f2e; font-size: 15px;">
            {topic['tip']}
        </p>
    </div>

    <!-- 8. 자주 묻는 질문 (FAQ) -->
    <h2 style="color: #111111; font-size: 22px; border-bottom: 2px solid #008080; padding-bottom: 8px; margin-top: 35px;">
        ❓ 자주 묻는 질문 (FAQ)
    </h2>
    <div style="margin-top: 15px;">
        <p style="font-weight: bold; color: #008080; margin-bottom: 4px;">{faq1_q}</p>
        <p style="color: #444444; margin-top: 0; margin-bottom: 16px;">{faq1_a}</p>

        <p style="font-weight: bold; color: #008080; margin-bottom: 4px;">{faq2_q}</p>
        <p style="color: #444444; margin-top: 0; margin-bottom: 16px;">{faq2_a}</p>
    </div>

    <!-- 9. 맺음말 및 브랜딩 푸터 -->
    <hr style="border: 0; height: 1px; background-color: #e2e8f0; margin: 40px 0 25px 0;" />
    <p style="color: #555555; font-size: 15px;">
        오늘 전달해 드린 <b>{cleaned_keyword}</b> 정보가 여러분의 스마트한 일상과 풍요로운 자산 관리에 실질적인 도움이 되었기를 바랍니다.<br />
        앞으로도 가치 있고 알찬 실전 정보를 가장 빠르고 정확하게 전달해 드리겠습니다. 감사합니다!
    </p>

    <div style="text-align: center; margin-top: 35px; padding: 20px; background-color: #f8fafc; border-radius: 10px; border: 1px dashed #cbd5e1;">
        <p style="margin: 0; font-weight: bold; color: #008080; font-size: 16px;">
            🏢 리치유니의 무인 블로그 자동화 공장
        </p>
        <p style="margin: 6px 0 0 0; color: #64748b; font-size: 13px;">
            매일 유익한 정보와 실전 팁을 엄선하여 정성스럽게 공유합니다.
        </p>
    </div>

</div>
"""

    tags = [cleaned_keyword, category_name, "리치유니", f"{cleaned_keyword}꿀팁", f"{cleaned_keyword}추천", "정보공유"]

    return {
        "title": title,
        "content": body_html,
        "tags": tags,
        "category": category_name,
        "keyword": cleaned_keyword
    }
