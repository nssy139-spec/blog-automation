"""
블로그 콘텐츠 생성 모듈 (리치유니 7대 전문 분야 엔진)
- 재테크, 정부지원금, 부동산, 생활문화, 생활용품, 건강, 인테리어 7개 분야별 고유 특화 서식
- 키워드에 따라 살아있는 전문 데이터, 3줄 요약, 고화질 Unsplash 이미지 2장, 꿀팁, FAQ 실시간 생성
"""
from datetime import datetime
from typing import Dict, Any, List
from modules.image_service import get_blog_images

def generate_specialized_sections(keyword: str, topic_type: str = "재테크") -> Dict[str, Any]:
    """
    7대 주제(재테크, 정부지원금, 부동산, 생활문화, 생활용품, 건강, 인테리어)에 최적화된 전문 콘텐츠를 생성합니다.
    """
    current_year = datetime.now().year
    
    # 1. [재테크]
    if "재테크" in topic_type or "금융" in keyword or "적금" in keyword or "투자" in keyword:
        summary = [
            f"{current_year}년 최신 금융 흐름과 '{keyword}' 핵심 수익 구조 파악",
            "가처분 소득 대비 황금 분배율 및 불필요한 수수료·세금 절감법",
            "사회초년생부터 직장인까지 실패 없이 목돈 만드는 실전 액션플랜"
        ]
        sections = [
            {
                "subtitle": f"1. {keyword}의 기본 원리와 지금 주목해야 하는 결정적 이유",
                "desc": (
                    f"최근 금리 변동과 경제 불확실성이 커진 상황에서 <b>{keyword}</b>에 대한 관심이 매우 뜨겁습니다. "
                    f"단순히 유행을 따르는 것이 아니라, <b>{keyword}</b>의 정확한 수익/이자 구조와 만기 환급 혜택을 파악하는 것이 "
                    f"성공적인 자산 형성의 기본입니다. 지금 시점에 명확한 계획을 세워두면 중장기적인 종잣돈 마련에 큰 힘이 됩니다."
                )
            },
            {
                "subtitle": f"2. 수익률을 극대화하는 실전 자산 배분 전략",
                "desc": (
                    f"<b>{keyword}</b>를 실천할 때는 월 소득의 20~30% 내외에서 무리 없이 지속할 수 있는 규모로 시작해야 합니다. "
                    f"비과세 혜택과 정부 기여금, 복리 효과를 온전히 누리기 위해서는 중도 해지를 방지할 수 있는 '비상금 통장'을 반드시 병행 분리 운용하세요."
                )
            },
            {
                "subtitle": f"3. 우대금리 및 절세 혜택 100% 챙기는 체크포인트",
                "desc": (
                    f"주거래 은행의 급여 이체, 카드 실적, 마케팅 동의 등 손쉽게 달성할 수 있는 우대 요건들을 사전에 확인해야 최고 금리를 적용받을 수 있습니다. "
                    f"연말정산 소득공제 및 세액공제와 연계되는 항목인지도 꼼꼼히 체크해 두시기 바랍니다."
                )
            }
        ]
        tip = f"{keyword}를 시작할 때는 단기적인 성과에 조급해하지 말고, 1년 이상 흔들림 없이 유지할 수 있는 현실적인 금액으로 시작하는 것이 가장 현명합니다."
        faqs = [
            (f"Q. {keyword}는 사회초년생도 부담 없이 시작할 수 있나요?", "A. 네, 최소 금액부터 시작하여 소득 증가에 따라 증액하는 방식으로 누구나 쉽게 시작할 수 있습니다."),
            (f"Q. {keyword} 중도 해지 시 불이익이 큰가요?", "A. 비과세 혜택이 취소되거나 기본 이율만 적용될 수 있으므로, 반드시 만기까지 유지 가능한 여유 자금으로 운용하세요.")
        ]

    # 2. [정부지원금]
    elif "정부지원금" in topic_type or "지원금" in keyword or "바우처" in keyword:
        summary = [
            f"{current_year}년 정부 복지·지원금 핵심 신설 혜택 및 신청 자격 총정리",
            "중위소득 기준 및 가구원 수별 지원 금액 한눈에 확인하기",
            "정부24 및 복지로를 통한 온라인 간편 원스톱 신청 가이드"
        ]
        sections = [
            {
                "subtitle": f"1. 2026년 {keyword} 주요 지원 대상 및 자격 기준",
                "desc": (
                    f"올해 새롭게 개편된 <b>{keyword}</b> 정책은 실질적인 생활비 부담을 덜어주기 위해 지원 대상과 소득 요건이 대폭 완화되었습니다. "
                    f"건강보험료 본인부담금과 가구원 합산 소득을 기준으로 지원 대상 여부가 결정되므로, 본인의 해당 구간을 먼저 확인하는 것이 필수적입니다."
                )
            },
            {
                "subtitle": f"2. 놓치면 손해보는 숨은 지원금 조회 및 신청 절차",
                "desc": (
                    f"정부24의 '보조금24' 포털이나 모바일 '복지로' 앱에 접속하여 간편인증을 진행하면, 본인이 받을 수 있는 <b>{keyword}</b> 관련 혜택이 자동 매칭됩니다. "
                    f"주민등록등본, 소득금액증명원 등 필요 서류는 전자지갑을 통해 클릭 한 번으로 자동 첨부됩니다."
                )
            },
            {
                "subtitle": f"3. 신청 기한 및 예산 조기 소진 대비 요령",
                "desc": (
                    f"많은 정부 지원 사업은 예산 소진 시 선착순으로 접수가 조기 마감되는 경우가 흔합니다. "
                    f"신청 개시일 오전에 미리 공인인증 또는 간편인증 로그인을 완료하고 접수하는 것이 가장 안전합니다."
                )
            }
        ]
        tip = "공고문상의 '중복 수혜 제한' 항목을 반드시 먼저 확인하세요. 지자체 고유 사업과 국비 사업 간 중복 가능 여부를 행정복지센터에 문의하면 정확합니다."
        faqs = [
            ("Q. 무직자나 아르바이트생도 신청 가능한가요?", "A. 고용 형태보다는 가구 소득 인정액 기준이 우선시되므로, 요건을 충족하면 신청 가능 대상이 됩니다."),
            ("Q. 온라인 신청이 어려운 어르신은 어떻게 하나요?", "A. 신분증을 지참하여 주민등록지 관할 행정복지센터(주민센터)에 방문하시면 담당 공무원이 접수를 도와드립니다.")
        ]

    # 3. [부동산]
    elif "부동산" in topic_type or "청약" in keyword or "대출" in keyword or "전세" in keyword:
        summary = [
            f"{current_year}년 내 집 마련 및 주거 안정을 위한 '{keyword}' 완벽 가이드",
            "정부 정책 대출(디딤돌/버팀목) 저금리 조건 및 청약 가점 전략",
            "전세사기 완벽 예방 및 보증보험(HUG/HF) 필수 가입 체크리스트"
        ]
        sections = [
            {
                "subtitle": f"1. {keyword} 시장 동향과 필수적으로 알아야 할 핵심 법규",
                "desc": (
                    f"최근 부동산 시장에서는 금리 추이와 정부의 공급 정책에 맞춰 <b>{keyword}</b>에 대한 전략적인 접근이 필수적입니다. "
                    f"주택담보대출비율(LTV), 총부채원리금상환비율(DSR) 등 대출 규제와 세제 개편 사항을 명확히 숙지해야 무리한 영끌을 피할 수 있습니다."
                )
            },
            {
                "subtitle": f"2. 실거주자를 위한 현실적인 자금 조달 계획",
                "desc": (
                    f"시중은행 일반 대출에 비해 금리가 월등히 낮은 <b>{keyword}</b> 관련 정책 금융 상품(디딤돌, 버팀목, 신생아 특례 등)의 "
                    f"자격 조건을 먼저 검토하세요. 부부 합산 소득과 자산 기준을 맞춘다면 수천만 원의 이자 비용을 절감할 수 있습니다."
                )
            },
            {
                "subtitle": f"3. 계약 전 반드시 확인해야 할 등기부등본 및 권리분석",
                "desc": (
                    f"계약 당일 및 잔금 지급 당일 등기부등본 갑구의 가압류·경매개시결정, 을구의 근저당권 설정액을 실시간 열람해야 합니다. "
                    f"전세보증금 반환보증보험 가입 가능 여부를 특약 사항에 명시하는 것은 보증금을 지키는 절대적 안전장치입니다."
                )
            }
        ]
        tip = "계약서 특약란에 '임대인은 잔금 지급일 익일까지 담보권을 설정하지 아니하며, 위반 시 계약을 무효로 하고 계약금을 즉시 반환한다'는 문구를 반드시 추가하세요."
        faqs = [
            ("Q. 무주택 세대주 조건은 언제까지 유지해야 하나요?", "A. 대출 실행일 및 등기 완료 시점까지 무주택 세대주 자격을 반드시 유지하셔야 불이익이 없습니다."),
            ("Q. 전세보증보험 가입은 언제 신청하는 것이 가장 좋나요?", "A. 잔금 지급과 전입신고 및 확정일자를 받은 직후 지체 없이 신청하시는 것이 가장 안전합니다.")
        ]

    # 4. [생활문화]
    elif "생활문화" in topic_type or "루틴" in keyword or "여행" in keyword or "전시" in keyword:
        summary = [
            f"지친 일상에 확실한 쉼표를 찍어주는 '{keyword}' 힐링 가이드",
            "바쁜 일상 속 시간과 스트레스를 획기적으로 줄여주는 라이프 꿀팁",
            "주말과 여가 시간을 200% 알차게 보내는 문화 & 공간 큐레이션"
        ]
        sections = [
            {
                "subtitle": f"1. 왜 지금 우리에게 {keyword}가 필요한가?",
                "desc": (
                    f"정신없이 흘러가는 도시 생활 속에서 나만의 온전한 여유를 찾는 <b>{keyword}</b>의 가치는 날로 커지고 있습니다. "
                    f"거창한 계획 없이도 일상 속 작은 루틴이나 주말 짧은 문화 나들이를 통해 마음에 신선한 에너지를 채워줄 수 있습니다."
                )
            },
            {
                "subtitle": f"2. 직접 경험해보고 추천하는 알짜 실천 노하우",
                "desc": (
                    f"<b>{keyword}</b>를 제대로 즐기기 위해서는 타인의 시선이나 트렌드에 얽매이지 않고, 본인이 가장 편안함을 느끼는 템포를 찾는 것이 중요합니다. "
                    f"주변의 조용한 힐링 스팟을 방문하거나, 하루 10분 온전히 나만을 위한 몰입 시간을 확보해 보세요."
                )
            },
            {
                "subtitle": f"3. 삶의 활력을 지속시켜 주는 데일리 습관 팁",
                "desc": (
                    f"좋은 경험을 일회성으로 끝내지 않고 스마트폰 메모 앱이나 사진 기록으로 남겨두면, "
                    f"힘든 순간마다 꺼내볼 수 있는 든든한 일상의 버팀목이 됩니다. 작은 성취와 휴식이 번아웃을 막아줍니다."
                )
            }
        ]
        tip = "휴식을 취할 때는 스마트폰 알림을 1시간만 무음으로 설정해 보세요. 디지털 디톡스가 결합될 때 뇌의 피로가 놀랍도록 빠르게 회복됩니다."
        faqs = [
            ("Q. 주말에 혼자서도 부담 없이 즐길 수 있나요?", "A. 물론입니다. 혼자만의 시간일수록 오롯이 내 감각에 집중할 수 있어 힐링 효과가 배가됩니다."),
            ("Q. 바쁜 직장인은 어떻게 시간을 내야 할까요?", "A. 주말 반나절이나 퇴근 후 30분 정도의 자투리 시간을 활용하는 것부터 가볍게 시작해 보세요.")
        ]

    # 5. [생활용품]
    elif "생활용품" in topic_type or "살림" in keyword or "청소" in keyword or "다이소" in keyword:
        summary = [
            f"실제 써보고 검증한 삶의 질 수직 상승 '{keyword}' 실사용 리뷰",
            "불필요한 지출을 막아주는 가성비 및 내구성 꼼꼼 비교 분석",
            "살림 동선과 청소 시간을 절반으로 줄여주는 실전 활용 꿀팁"
        ]
        sections = [
            {
                "subtitle": f"1. {keyword}를 직접 사용해보고 체감한 핵심 장점",
                "desc": (
                    f"매일 반복되는 집안일과 정리정돈에 들이는 시간을 획기적으로 줄여주는 <b>{keyword}</b>는 "
                    f"살림의 피로도를 낮추는 최고의 효자 아이템입니다. 단순한 유행템을 넘어 일상의 번거로움을 똑똑하게 해결해 줍니다."
                )
            },
            {
                "subtitle": f"2. 구매 전 반드시 체크해야 할 스펙과 가성비 포인트",
                "desc": (
                    f"<b>{keyword}</b>를 선택할 때는 화려한 디자인보다는 관리의 용이성(물세척 가능 여부, 내구성)과 수납 호환성을 먼저 따져보아야 합니다. "
                    f"고가의 브랜드 제품과 가성비 제품 간의 실질적인 성능 차이를 꼼꼼히 비교하면 합리적인 소비가 가능합니다."
                )
            },
            {
                "subtitle": f"3. 200% 활용도를 끌어올리는 살림 노하우",
                "desc": (
                    f"해당 제품을 한 가지 용도로만 쓰지 않고 주방, 욕실, 세탁실 등 다용도로 확장 활용할 수 있는 아이디어를 적용해 보세요. "
                    f"라벨링 테이프나 투명 정리함과 함께 조합하면 시각적으로도 훨씬 정돈된 공간이 완성됩니다."
                )
            }
        ]
        tip = "새 살림템을 들일 때는 기존에 쓰지 않는 낡은 물건 하나를 비우는 '1 In 1 Out' 원칙을 지키면 언제나 깔끔한 집안 상태를 유지할 수 있습니다."
        faqs = [
            ("Q. 원룸처럼 좁은 집에서도 유용하게 쓸 수 있나요?", "A. 네, 공간을 적게 차지하면서 수직 공간을 활용하는 구조라 좁은 평수일수록 만족도가 더욱 높습니다."),
            ("Q. 세척이나 위생 관리가 번거롭지는 않나요?", "A. 분리 세척이 간편한 구조의 제품을 선택하시면 주 1회 가벼운 물세척만으로도 청결하게 유지됩니다.")
        ]

    # 6. [건강]
    elif "건강" in topic_type or "스트레칭" in keyword or "영양제" in keyword or "식단" in keyword:
        summary = [
            f"지치지 않는 활력과 면역력을 위한 '{keyword}' 실전 건강 루틴",
            "무리한 운동 없이 일상 속에서 실천하는 바른 자세 및 영양 관리",
            "피로 회복과 숙면을 부르는 전문가 추천 데일리 체크리스트"
        ]
        sections = [
            {
                "subtitle": f"1. {keyword}가 우리 몸의 컨디션에 미치는 결정적 영향",
                "desc": (
                    f"현대인의 불규칙한 생활 습관과 좌식 생활은 만성 피로와 근골격계 통증을 유발하는 주원인입니다. "
                    f"일상 속에서 <b>{keyword}</b>를 꾸준히 챙기면 체내 순환과 대사 균형이 회복되어 하루를 시작하는 피로감이 현저히 줄어듭니다."
                )
            },
            {
                "subtitle": f"2. 누구나 당장 따라 할 수 있는 5분 실천법",
                "desc": (
                    f"시간을 내어 헬스장에 가지 않더라도, 아침 기상 직후와 업무 중간에 <b>{keyword}</b> 관련 동작이나 습관을 실천해 보세요. "
                    f"바른 호흡과 가벼운 이완 동작만으로도 굳어 있던 근육이 풀리고 혈액 순환이 원활해지는 즉각적인 체감을 할 수 있습니다."
                )
            },
            {
                "subtitle": f"3. 식단 및 수면과의 완벽한 시너지 루틴",
                "desc": (
                    f"단순한 관리 하나에 의존하기보다, 취침 1시간 전 스마트폰 멀리하기, 저당 식단 유지하기와 병행할 때 그 효과는 배가됩니다. "
                    f"규칙적인 생체 리듬이 정착되면 면역력 강화는 자연스럽게 따라옵니다."
                )
            }
        ]
        tip = "건강 관리는 한 번에 무리하게 하는 것보다, 매일 5분씩이라도 같은 시간에 꾸준히 지속하는 반복성이 핵심입니다."
        faqs = [
            ("Q. 바쁜 일상 중에 언제 실천하는 것이 가장 효과적인가요?", "A. 아침 기상 직후 공복 시간이나 취침 30분 전 이완 루틴으로 진행하시는 것을 가장 추천합니다."),
            ("Q. 기존에 앓고 있는 통증이 있어도 무리가 없나요?", "A. 본인의 가동 범위 내에서 통증이 느껴지지 않는 부드러운 강도로 시작하시고, 통증 발생 시 즉시 멈추세요.")
        ]

    # 7. [인테리어]
    else:
        summary = [
            f"적은 비용으로 집안 분위기를 180도 바꾸는 '{keyword}' 홈스타일링",
            "공간을 1.5배 넓어 보이게 만드는 컬러 매칭 및 가구 배치 공식",
            "감성 조명과 소품을 활용한 나만의 아늑한 힐링 하우스 완성법"
        ]
        sections = [
            {
                "subtitle": f"1. {keyword}로 시작하는 감성 홈 인테리어의 매력",
                "desc": (
                    f"집은 단순한 주거 공간을 넘어 하루의 피로를 씻어내고 온전한 쉼을 얻는 곳이어야 합니다. "
                    f"<b>{keyword}</b>를 활용한 미니멀하고 따뜻한 스타일링은 적은 예산으로도 집 전체의 무드를 드라마틱하게 바꿔줍니다."
                )
            },
            {
                "subtitle": f"2. 실패 없는 컬러 톤앤매너와 조명 배치 공식",
                "desc": (
                    f"베이스 컬러(화이트/베이지) 70%, 보조 컬러(우드/그레이) 25%, 포인트 소품 컬러 5%의 황금 비율을 적용해 보세요. "
                    f"여기에 3000K 전구색 간접 조명을 구석에 배치하면 밤마다 카페 같은 아늑한 분위기를 연출할 수 있습니다."
                )
            },
            {
                "subtitle": f"3. 작은 평수도 시각적으로 시원하게 트여 보이는 꿀팁",
                "desc": (
                    f"낮은 가구를 배치하여 시야를 확보하고, 바닥에 물건을 두지 않는 공중 부양 수납법을 활용하세요. "
                    f"반려식물 한두 점을 더하면 생동감 넘치는 플랜테리어가 손쉽게 완성됩니다."
                )
            }
        ]
        tip = "가구를 사기 전에 바닥에 마스킹 테이프로 실제 크기를 먼저 붙여보세요. 동선 방해나 답답함을 미리 완벽하게 방지할 수 있습니다."
        faqs = [
            ("Q. 전월세 집에서도 못 자국 없이 인테리어가 가능한가요?", "A. 꼭꼬핀이나 무타공 벽걸이 선반, 스탠드형 조명을 활용하시면 벽 손상 없이 완벽하게 꾸밀 수 있습니다."),
            ("Q. 인테리어 소품은 어떤 것부터 구비하는 게 좋나요?", "A. 가성비가 가장 높은 간접 스탠드 조명과 패브릭 쿠션 커버부터 시작해 보시는 것을 추천합니다.")
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
    category: str = "finance",
    topic_type: str = "재테크"
) -> Dict[str, Any]:
    """
    7개 전문 분야(재테크/정부지원금/부동산/생활문화/생활용품/건강/인테리어)에 맞춰 
    풍부하고 고유한 글과 고화질 Unsplash 이미지 2장을 결합하여 생성합니다.
    """
    cleaned_keyword = keyword.strip() if keyword else "스마트 라이프 꿀팁"
    current_year = datetime.now().year
    
    is_finance = "finance" in category or "경제" in category or "재테크" in category
    category_name = "재테크·경제" if is_finance else "생활·문화·리뷰"
    
    # 1. 전문 분야별 동적 맞춤 콘텐츠 데이터 생성
    topic = generate_specialized_sections(cleaned_keyword, topic_type)
    
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
        theme_lead = f"바쁜 일상 속 삶의 질과 만족도를 확실하게 업그레이드해 줄 <b><span style='color:#008080;'>{cleaned_keyword}</span></b>의 핵심 활용법과 알짜 노하우를 솔직하게 공유합니다."

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

    tags = [cleaned_keyword, category_name, topic_type, "리치유니", f"{cleaned_keyword}꿀팁", f"{cleaned_keyword}추천", "정보공유"]

    return {
        "title": title,
        "content": body_html,
        "tags": tags,
        "category": category_name,
        "topic_type": topic_type,
        "keyword": cleaned_keyword
    }
