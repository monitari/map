# 기본 이념 스펙트럼
ideological_spectrum = ['Far-left', 'Left', 'Center-left', 'Centrist', 'Center-right', 'Right','Far-right']

party_preference = { # 정당 선호도 (행정구역: {보수주의: 0.0, 진보주의: 0.0})
    # 아이리카 주
    "메초오비카": {"Conservative": 1.10, "Progressive": 0.90},
    "아브레": {"Conservative": 0.86, "Progressive": 1.14},
    "피에트라": {"Conservative": 0.83, "Progressive": 1.17},
    "아이리카": {"Conservative": 1.00, "Progressive": 1.00},
    "메르네": {"Conservative": 0.85, "Progressive": 1.15},
    "츠비키": {"Conservative": 0.92, "Progressive": 1.08},
    "하르바트": {"Conservative": 1.07, "Progressive": 0.93},

    # 그라나데 주
    "안파키": {"Conservative": 1.23, "Progressive": 0.77},
    "아파그라나다": {"Conservative": 1.14, "Progressive": 0.86},
    "페카그라나다": {"Conservative": 1.06, "Progressive": 0.94},
    "그라나다": {"Conservative": 1.12, "Progressive": 0.88},
    "보피노": {"Conservative": 1.22, "Progressive": 0.78},
    "메르노": {"Conservative": 1.13, "Progressive": 0.87},

    # 그미즈리 주
    "오크모": {"Conservative": 1.10, "Progressive": 0.90},
    "미톤노": {"Conservative": 0.97, "Progressive": 1.03},
    "페아그": {"Conservative": 0.91, "Progressive": 1.09},
    "그미즈리": {"Conservative": 0.85, "Progressive": 1.15},
    "아센시": {"Conservative": 1.02, "Progressive": 0.98},
    "메깅고": {"Conservative": 0.94, "Progressive": 1.06},
    "호오토": {"Conservative": 1.11, "Progressive": 0.89},
    "키에오": {"Conservative": 1.20, "Progressive": 0.80},

    # 도마니 주
    "오브니": {"Conservative": 0.92, "Progressive": 1.08},
    "바스바드": {"Conservative": 1.07, "Progressive": 0.93},
    "케릴티": {"Conservative": 0.91, "Progressive": 1.09},
    "메고기": {"Conservative": 1.04, "Progressive": 0.96},
    "에링고": {"Conservative": 0.95, "Progressive": 1.05},
    "커피": {"Conservative": 0.95, "Progressive": 1.05},
    "즈조이": {"Conservative": 1.01, "Progressive": 0.99},
    "가안": {"Conservative": 0.92, "Progressive": 1.08},
    "브고홀": {"Conservative": 1.20, "Progressive": 0.80},
    "모옹홀": {"Conservative": 1.21, "Progressive": 0.79},
    "메옹": {"Conservative": 1.12, "Progressive": 0.88},

    # 림덴시 주
    "파미즈": {"Conservative": 0.89, "Progressive": 1.11},
    "스피가": {"Conservative": 0.90, "Progressive": 1.10},
    "아르고": {"Conservative": 0.79, "Progressive": 1.21},
    "모리고": {"Conservative": 0.78, "Progressive": 1.22},
    "펜보드": {"Conservative": 0.97, "Progressive": 1.03},
    "메바치": {"Conservative": 0.92, "Progressive": 1.08},
    "모호카": {"Conservative": 1.20, "Progressive": 0.80},
    "린토카": {"Conservative": 1.12, "Progressive": 0.88},
    "낙소": {"Conservative": 0.86, "Progressive": 1.14},
    "보빈": {"Conservative": 0.88, "Progressive": 1.12},
    "라토카": {"Conservative": 1.08, "Progressive": 0.92},
    "세오고": {"Conservative": 0.90, "Progressive": 1.10},
    "시안": {"Conservative": 0.84, "Progressive": 1.16},
    "보어": {"Conservative": 1.02, "Progressive": 0.98},

    # 메세기 주
    "크라나": {"Conservative": 0.91, "Progressive": 1.09},
    "나다이": {"Conservative": 0.92, "Progressive": 1.08},
    "옹피오": {"Conservative": 1.02, "Progressive": 0.98},
    "메세기": {"Conservative": 0.95, "Progressive": 1.05},
    "포크란": {"Conservative": 0.79, "Progressive": 1.21},
    "크레이": {"Conservative": 0.93, "Progressive": 1.07},
    "안파기": {"Conservative": 1.04, "Progressive": 0.96},

    # 미네바 주
    "아리나": {"Conservative": 0.79, "Progressive": 1.21},
    "만토": {"Conservative": 0.75, "Progressive": 1.25},
    "메가": {"Conservative": 0.76, "Progressive": 1.24},
    "코에가": {"Conservative": 0.82, "Progressive": 1.18},
    "민마나": {"Conservative": 0.88, "Progressive": 1.12},
    "모에바": {"Conservative": 0.77, "Progressive": 1.23},
    "아바나": {"Conservative": 0.84, "Progressive": 1.16},
    "솔바": {"Conservative": 0.87, "Progressive": 1.13},
    "미바나": {"Conservative": 0.85, "Progressive": 1.15},
    "에디아다": {"Conservative": 1.00, "Progressive": 1.00},
    "리에다": {"Conservative": 0.98, "Progressive": 1.02},

    # 미치바 주
    "메고이오": {"Conservative": 1.02, "Progressive": 0.98},
    "우프레나": {"Conservative": 0.91, "Progressive": 1.09},
    "미츠비": {"Conservative": 0.88, "Progressive": 1.12},
    "알고": {"Conservative": 1.12, "Progressive": 0.88},
    "산시아고": {"Conservative": 0.96, "Progressive": 1.04},
    "나릴로": {"Conservative":  0.90, "Progressive": 1.10},
    "유프란": {"Conservative": 1.04, "Progressive": 0.96},
    "미치바": {"Conservative": 0.95, "Progressive": 1.05},

    # 바니카-메고차 주
    "바니아": {"Conservative": 1.21, "Progressive": 0.79},
    "미에고": {"Conservative": 1.13, "Progressive": 0.87},
    "메고리": {"Conservative": 1.22, "Progressive": 0.78},
    "민고": {"Conservative": 1.14, "Progressive": 0.86},
    "이벤토": {"Conservative": 1.20, "Progressive": 0.80},
    "마링고": {"Conservative": 1.11, "Progressive": 0.89},

    # 베고차 주
    "모베이": {"Conservative": 1.02, "Progressive": 0.98},
    "트롱페이": {"Conservative": 1.11, "Progressive": 0.89},
    "바티아": {"Conservative": 0.91, "Progressive": 1.09},
    "이베이": {"Conservative": 1.03, "Progressive": 0.97},
    "페린": {"Conservative": 1.12, "Progressive": 0.88},
    "리안토": {"Conservative": 0.99, "Progressive": 1.01},
    "오고소": {"Conservative": 0.94, "Progressive": 1.06},
    "민마": {"Conservative": 0.89, "Progressive": 1.11},
    "테안타": {"Conservative": 0.92, "Progressive": 1.08},
    "모반토": {"Conservative": 0.94, "Progressive": 1.06},
    "레링가": {"Conservative": 1.09, "Progressive": 0.91},

    # 세그레차 주
    "하롱골": {"Conservative": 1.22, "Progressive": 0.78},
    "미골": {"Conservative": 1.02, "Progressive": 0.98},    
    "메링골": {"Conservative": 1.21, "Progressive": 0.79},
    "세골": {"Conservative": 0.97, "Progressive": 1.03},
    "키골": {"Conservative": 1.01, "Progressive": 0.99},
    "리에골": {"Conservative": 1.11, "Progressive": 0.89},
    "페아골": {"Conservative": 1.23, "Progressive": 0.77},
    "베아골": {"Conservative": 1.14, "Progressive": 0.86},

    # 안텐시 주
    "모호보드": {"Conservative": 1.02, "Progressive": 0.98},
    "아핀고": {"Conservative":  1.11, "Progressive": 0.89},
    "비에노": {"Conservative": 0.93, "Progressive": 1.07},
    "시세디": {"Conservative": 0.84, "Progressive": 1.16},
    "메즈노": {"Conservative": 0.89, "Progressive": 1.11},
    "아신가": {"Conservative": 0.93, "Progressive": 1.07},
    "키르가": {"Conservative": 0.92, "Progressive": 1.08},

    # 카리아-로 주
    "노베라니나": {"Conservative": 0.89, "Progressive": 1.11},
    "아르모텐타": {"Conservative": 0.96, "Progressive": 1.04},
    "피고모싱고메고차바데다": {"Conservative": 1.11, "Progressive": 0.89},
    "미베이토메고차피덴타": {"Conservative": 1.04, "Progressive": 0.96},
    "안트로아싱가": {"Conservative": 0.79, "Progressive": 1.21},

    # 테트라 주
    "아젠타": {"Conservative": 0.92, "Progressive": 1.08},
    "아칸타": {"Conservative": 1.03, "Progressive": 0.97},
    "파르티엔타": {"Conservative": 0.94, "Progressive": 1.06},
    "유칸타": {"Conservative": 1.02, "Progressive": 0.98},
    "테트리다모스": {"Conservative": 0.91, "Progressive": 1.09},
    "테트리비제모스": {"Conservative": 1.04, "Progressive": 0.96},
    "테타": {"Conservative": 0.93, "Progressive": 1.07},

    # 포어 주
    "메네트리포어": {"Conservative": 1.22, "Progressive": 0.78},
    "안트리포어": {"Conservative": 1.13, "Progressive": 0.87},
    "라간": {"Conservative": 0.94, "Progressive": 1.06},
    "안파": {"Conservative": 1.02, "Progressive": 0.98},
    "테사": {"Conservative": 0.91, "Progressive": 1.09},
    "아르테": {"Conservative": 1.04, "Progressive": 0.96},
    "세가": {"Conservative": 0.93, "Progressive": 1.07},
    "오르도기": {"Conservative": 1.01, "Progressive": 0.99},

    # 하파차 주
    "파시벤토": {"Conservative": 0.95, "Progressive": 1.05},
    "오고이모": {"Conservative": 1.03, "Progressive": 0.97},
    "미느리오": {"Conservative": 0.92, "Progressive": 1.08},
    "산세오": {"Conservative": 1.11, "Progressive": 0.89},
    "아스타나": {"Conservative": 1.02, "Progressive": 0.98},
    "티레니오": {"Conservative": 0.94, "Progressive": 1.06},
    "비엥고": {"Conservative": 1.12, "Progressive": 0.88},
    "아린키고": {"Conservative": 1.21, "Progressive": 0.79},
    "하싱고": {"Conservative":  0.91, "Progressive": 1.09},
    "모잉고": {"Conservative": 1.04, "Progressive": 0.96},
    "하르고": {"Conservative": 0.92, "Progressive": 1.08},
}

def define_party_preference(conservative, progressive):
    """
    보수주의와 진보주의 점수에 따라 정당 선호도를 정의하고 점수를 부여합니다.
    
    Args:
    conservative (float): 보수주의 점수
    progressive (float): 진보주의 점수
    
    Returns:
    dict: 정당 선호도와 점수
    """
    score = progressive - conservative
    preference_scores = {
        'Far-left': 0,
        'Left': 0,
        'Center-left': 0,
        'Centrist': 0,
        'Center-right': 0,
        'Right': 0,
        'Far-right': 0
    }
    
    if score >= 0.6:
        preference_scores['Far-left'] = 1 - abs(score - 0.6)
    elif score >= 0.3:
        preference_scores['Left'] = 1 - abs(score - 0.3)
    elif score >= 0.1:
        preference_scores['Center-left'] = 1 - abs(score - 0.1)
    elif score >= -0.1:
        preference_scores['Centrist'] = 1 - abs(score)
    elif score >= -0.3:
        preference_scores['Center-right'] = 1 - abs(score + 0.1)
    elif score >= -0.6:
        preference_scores['Right'] = 1 - abs(score + 0.3)
    else:
        preference_scores['Far-right'] = 1 - abs(score + 0.6)
        
    # 가장 높은 점수를 가진 성향을 찾습니다.
    max_preference = max(preference_scores, key=preference_scores.get)
    
    # 확률 분포를 생성합니다.
    distribution = {
        'Far-left': 0,
        'Left': 0,
        'Center-left': 0,
        'Centrist': 0,
        'Center-right': 0,
        'Right': 0,
        'Far-right': 0
    }
    
    # 중심 성향을 기준으로 확률 분포를 만듭니다.
    center_index = list(preference_scores.keys()).index(max_preference)
    for i, key in enumerate(preference_scores.keys()):
        distance = abs(center_index - i)
        distribution[key] = max(0.1, 1 - 0.18 * distance)  # 거리마다 0.18씩 감소
    
    return distribution