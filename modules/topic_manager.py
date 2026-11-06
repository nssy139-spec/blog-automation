"""
순환형 토픽 관리자 (Topic Manager)
- 규칙:
  1) 재테크 -> 생활문화 -> 정부지원금 -> 생활용품 -> 부동산 -> 건강 -> 인테리어 순서로 엄격하게 순환
  2) 단회성 원칙: 글이 생성되는 즉시 포인터가 다음 주제로 전진하여, 발행 실패 여부와 무관하게 이전 글은 폐기하고 무조건 다음 차례의 새로운 주제로 생성
  3) 똑같은 글 중복 방지: 각 카테고리별 고유 키워드 풀에서 순차 소비
"""
import os
import json
from typing import Dict, Any, Tuple
from modules.logger import setup_logger

logger = setup_logger("topic_manager")

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scheduler_state.json")

# 사용자가 지정한 7단계 순환 시퀀스 (재테크 계열과 생활/문화 계열이 정교하게 교차)
ROTATION_SEQUENCE = [
    {"type": "재테크", "category": "finance", "label": "재테크·경제"},
    {"type": "생활문화", "category": "lifestyle", "label": "생활·문화·리뷰"},
    {"type": "정부지원금", "category": "finance", "label": "재테크·경제"},
    {"type": "생활용품", "category": "lifestyle", "label": "생활·문화·리뷰"},
    {"type": "부동산", "category": "finance", "label": "재테크·경제"},
    {"type": "건강", "category": "lifestyle", "label": "생활·문화·리뷰"},
    {"type": "인테리어", "category": "lifestyle", "label": "생활·문화·리뷰"}
]

# 주제별 세부 키워드 풀 (매 회차마다 새로운 주제로 글 생성)
KEYWORD_POOLS = {
    "재테크": [
        "2026 청년 도약 계좌 조건 및 우대금리 비교",
        "직장인 통장 쪼개기 및 13월의 월급 연말정산 절세 전략",
        "사회초년생 종잣돈 1억 모으기 현실 로드맵",
        "금리 인하기 고금리 파킹통장 및 CMA 추천",
        "월배당 ETF 및 미국 배당주 초보 포트폴리오"
    ],
    "생활문화": [
        "주말에 가볼 만한 서울 근교 힐링 전시 및 문화 공간",
        "하루의 에너지를 깨우는 미라클 모닝 10분 루틴",
        "바쁜 현대인을 위한 스트레스 해소 웰니스 라이프",
        "넷플릭스 OTT 숨은 명작 인생 드라마 추천",
        "시간을 아껴주는 노션(Notion) 스케줄 관리법"
    ],
    "정부지원금": [
        "2026년 하반기 숨은 정부지원금 보조금24 조회법",
        "청년 월세 한시 특별지원 신청 자격 및 필수 서류",
        "소상공인 정책자금 및 저금리 대환대출 지원 혜택",
        "취약계층 에너지바우처 및 가스비 환급 신청",
        "근로장려금 및 자녀장려금 신청 자격 총정리"
    ],
    "생활용품": [
        "내돈내산 삶의 질 수직 상승 주방 살림 꿀템 리뷰",
        "다이소 가성비 끝판왕 정리정돈 및 수납용품 추천",
        "욕실 물때와 곰팡이 방지 인기 청소용품 솔직 비교",
        "1인 가구 좁은 원룸 공간활용 옷걸이 및 수납함",
        "피부 자극 없는 친환경 세탁세제 실사용 꿀팁"
    ],
    "부동산": [
        "생애최초 내 집 마련 디딤돌 및 버팀목 대출 요건",
        "아파트 청약통장 1순위 조건 및 신혼부부 특별공급",
        "전세사기 예방을 위한 전세보증금 반환보증보험 가입법",
        "2026 부동산 공시지가 조회 및 보유세 절세 전략",
        "월세 세액공제 신청 방법과 필요 서류 체크포인트"
    ],
    "건강": [
        "직장인 만성피로 탈출 필수 영양제 3대장 조합",
        "거북목과 허리 통증을 없애는 5분 오피스 스트레칭",
        "혈당 스파이크 막는 거꾸로 식사법과 저당 식단",
        "불면증 극복을 위한 수면 위생과 꿀잠 수면 루틴",
        "매일 30분 걷기 운동이 몸에 가져오는 놀라운 변화"
    ],
    "인테리어": [
        "소형 평수 원룸 넓어 보이는 화이트 우드 홈스타일링",
        "아늑한 분위기를 완성하는 감성 간접조명 인테리어",
        "초보자도 쉽게 키우는 공기정화 반려식물 BEST 5",
        "깔끔한 책상 데스크테리어 필수 아이템 및 선 정리법",
        "포근한 계절 맞이 침구 및 패브릭 컬러 조합 가이드"
    ]
}

def load_state() -> Dict[str, Any]:
    """현재 스케줄러 상태를 로드합니다."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "sequence_index": 0,
        "keyword_indices": {k: 0 for k in KEYWORD_POOLS.keys()},
        "last_generated_topic": None,
        "history": []
    }

def save_state(state: Dict[str, Any]):
    """스케줄러 상태를 파일에 영구 저장합니다."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"스케줄러 상태 저장 실패: {e}")

def get_next_topic_and_advance() -> Dict[str, str]:
    """
    [핵심 원칙]
    - 이번 차례의 주제와 키워드를 즉시 반환하고,
    - 호출되는 순간 무조건 다음 주제로 포인터를 전진시킵니다.
    - 따라서 발행에 실패하거나 중간에 중단되어도, 이전 글은 폐기되고
      다음 실행 시에는 100% 무조건 다음 순서의 주제로 넘어갑니다.
    """
    state = load_state()
    seq_idx = state.get("sequence_index", 0) % len(ROTATION_SEQUENCE)
    current_step = ROTATION_SEQUENCE[seq_idx]
    topic_type = current_step["type"]
    category = current_step["category"]
    label = current_step["label"]

    # 해당 주제의 키워드 풀에서 키워드 선정
    kw_indices = state.setdefault("keyword_indices", {})
    kw_idx = kw_indices.get(topic_type, 0)
    pool = KEYWORD_POOLS[topic_type]
    selected_keyword = pool[kw_idx % len(pool)]

    # [즉시 전진]: 이번 글을 써먹든 못 써먹든 무조건 다음 차례로 변경하여 중복/재탕 원천 차단!
    next_seq_idx = (seq_idx + 1) % len(ROTATION_SEQUENCE)
    kw_indices[topic_type] = (kw_idx + 1) % len(pool)
    state["sequence_index"] = next_seq_idx
    state["last_generated_topic"] = {
        "type": topic_type,
        "keyword": selected_keyword,
        "category": category
    }
    save_state(state)

    logger.info(
        f"🎯 [주제 선정 & 포인터 전진] 현재: {topic_type}('{selected_keyword}') "
        f"-> 다음 예정 차례: {ROTATION_SEQUENCE[next_seq_idx]['type']}"
    )

    return {
        "topic_type": topic_type,
        "keyword": selected_keyword,
        "category": category,
        "label": label,
        "next_topic_type": ROTATION_SEQUENCE[next_seq_idx]["type"]
    }

def peek_current_topic() -> Dict[str, str]:
    """전진시키지 않고 현재 차례가 무엇인지만 미리 확인합니다 (UI 표시용)."""
    state = load_state()
    seq_idx = state.get("sequence_index", 0) % len(ROTATION_SEQUENCE)
    current_step = ROTATION_SEQUENCE[seq_idx]
    topic_type = current_step["type"]
    pool = KEYWORD_POOLS[topic_type]
    kw_idx = state.get("keyword_indices", {}).get(topic_type, 0)
    selected_keyword = pool[kw_idx % len(pool)]
    
    return {
        "topic_type": topic_type,
        "keyword": selected_keyword,
        "category": current_step["category"],
        "label": current_step["label"]
    }
