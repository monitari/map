import pandas as pd
import numpy as np
import random
import math
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 기본 이념 스펙트럼
ideological_spectrum = ['Far-left', 'Left', 'Center-left', 'Centrist', 'Center-right', 'Right','Far-right']

# 주요 정치적 성향
main_alignments = [
    # 경제/사회 체제
    'Conservative', 'Liberal', 'Progressive', 'Socialist', 'Capitalist',
    # 거버넌스/정치 방식
    'Nationalism', 'Populism', 'Technocratic', 'Anti-corruption', 'Regionalist',
    # 주요 가치/이슈
    'Environmentalism', 'Social Justice', 'Labor-rights', 'Individual-rights', 'Religious',
    # 경제 정책
    'Free-market', 'Protectionist', 'Innovation',
    # 특수 관심사
    'Pacifist', 'Traditionalist', 'Rural', 'Modernist'
]

# 사건 영향 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
events = {
    '자연재해': { 'impact': 9.5, 'frequency': 0.05, 'importance': 8.0, 'subtypes': ['대지진', '태풍', '홍수', '가뭄', '화산폭발'] },
    '경제위기': { 'impact': 8.3, 'frequency': 0.08, 'importance': 9.0, 'subtypes': ['금융위기', '무역전쟁', '인플레이션', '실업률급증', '산업붕괴'] },
    '안보위기': { 'impact': 10.0, 'frequency': 0.03, 'importance': 9.5, 'subtypes': ['전쟁위협', '테러', '사이버공격', '국경분쟁', '내전'] },
    '사회문제': { 'impact': 6.7, 'frequency': 0.15, 'importance': 7.5, 'subtypes': ['불평등심화', '교육위기', '고령화', '저출산', '주거난'] },
    '환경위기': { 'impact': 7.8, 'frequency': 0.10, 'importance': 8.2, 'subtypes': ['기후변화', '대기오염', '수질오염', '생태계파괴', '자원고갈'] },
    '정치스캔들': { 'impact': 5.4, 'frequency': 0.12, 'importance': 6.8, 'subtypes': ['부패', '권력남용', '선거조작', '정보유출', '정치자금비리'] },
    '기술혁신': { 'impact': 4.9, 'frequency': 0.15, 'importance': 7.0, 'subtypes': ['AI혁명', '우주개발', '신재생에너지', '바이오기술', '양자컴퓨팅'] },
    '외교관계': { 'impact': 6.3, 'frequency': 0.12, 'importance': 7.2, 'subtypes': ['동맹강화', '국제고립', '통상마찰', '문화충돌', '국제협력'] },
    '정상상태': { 'impact': 1.0, 'frequency': 0.20, 'importance': 5.0, 'subtypes': ['안정기', '성장기', '조정기', '전환기', '회복기'] }
}

# 사건 영향 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
event_impact = {
    '자연재해': {'Centrist': 1.2, 'Center-left': 1.5, 'Center-right': 1.2, 'Far-left': 1.8, 'Far-right': 1.0, 'Left': 1.8, 'Right': 1.2, 'Conservative': 0.9, 'Liberal': 1.3, 'Progressive': 1.6, 'Socialist': 1.7, 'Capitalist': 0.8, 'Nationalism': 1.0, 'Populism': 1.4, 'Technocratic': 1.3, 'Environmentalism': 2.0, 'Social Justice': 1.6, 'Labor-rights': 1.4, 'Individual-rights': 1.1, 'Religious': 1.2, 'Free-market': 0.7, 'Protectionist': 1.3, 'Innovation': 1.4, 'Pacifist': 1.3, 'Traditionalist': 0.9, 'Rural': 1.5, 'Modernist': 1.3, 'Regionalist': 1.4, 'Anti-corruption': 1.1},
    '경제위기': {'Centrist': 0.8, 'Center-left': 1.4, 'Center-right': 0.7, 'Far-left': 1.9, 'Far-right': 1.3, 'Left': 1.6, 'Right': 0.6, 'Conservative': 0.7, 'Liberal': 0.8, 'Progressive': 1.3, 'Socialist': 1.8, 'Capitalist': 0.5, 'Nationalism': 1.4, 'Populism': 1.6, 'Technocratic': 1.2, 'Environmentalism': 1.1, 'Social Justice': 1.5, 'Labor-rights': 1.7, 'Individual-rights': 0.8, 'Religious': 1.0, 'Free-market': 0.4, 'Protectionist': 1.6, 'Innovation': 1.1, 'Pacifist': 0.9, 'Traditionalist': 0.8, 'Rural': 1.3, 'Modernist': 1.0, 'Regionalist': 1.2, 'Anti-corruption': 1.4},
    '안보위기': {'Centrist': 0.9, 'Center-left': 0.8, 'Center-right': 1.3, 'Far-left': 0.6, 'Far-right': 1.8, 'Left': 0.7, 'Right': 1.5, 'Conservative': 1.4, 'Liberal': 0.8, 'Progressive': 0.7, 'Socialist': 0.6, 'Capitalist': 1.2, 'Nationalism': 1.9, 'Populism': 1.5, 'Technocratic': 1.1, 'Environmentalism': 0.7, 'Social Justice': 0.8, 'Labor-rights': 0.9, 'Individual-rights': 0.7, 'Religious': 1.3, 'Free-market': 0.8, 'Protectionist': 1.6, 'Innovation': 1.2, 'Pacifist': 0.4, 'Traditionalist': 1.5, 'Rural': 1.1, 'Modernist': 0.9, 'Regionalist': 1.3, 'Anti-corruption': 0.9},
    '사회문제': {'Centrist': 1.0, 'Center-left': 1.6, 'Center-right': 0.8, 'Far-left': 1.8, 'Far-right': 1.1, 'Left': 1.7, 'Right': 0.7, 'Conservative': 0.8, 'Liberal': 1.4, 'Progressive': 1.6, 'Socialist': 1.7, 'Capitalist': 0.6, 'Nationalism': 1.2, 'Populism': 1.5, 'Technocratic': 1.1, 'Environmentalism': 1.3, 'Social Justice': 1.8, 'Labor-rights': 1.6, 'Individual-rights': 1.3, 'Religious': 1.2, 'Free-market': 0.7, 'Protectionist': 1.2, 'Innovation': 1.2, 'Pacifist': 1.3, 'Traditionalist': 0.9, 'Rural': 1.4, 'Modernist': 1.3, 'Regionalist': 1.3, 'Anti-corruption': 1.4 },
    '환경위기': {'Centrist': 1.2, 'Center-left': 1.7, 'Center-right': 0.9, 'Far-left': 1.8, 'Far-right': 0.6, 'Left': 1.7, 'Right': 0.7, 'Conservative': 0.7, 'Liberal': 1.3, 'Progressive': 1.7, 'Socialist': 1.6, 'Capitalist': 0.6, 'Nationalism': 0.8, 'Populism': 1.2, 'Technocratic': 1.5, 'Environmentalism': 2.0, 'Social Justice': 1.6, 'Labor-rights': 1.3, 'Individual-rights': 1.0, 'Religious': 1.1, 'Free-market': 0.6, 'Protectionist': 1.2, 'Innovation': 1.6, 'Pacifist': 1.4, 'Traditionalist': 0.8, 'Rural': 1.3, 'Modernist': 1.5, 'Regionalist': 1.2, 'Anti-corruption': 1.3},
    '정치스캔들': {'Centrist': 1.1, 'Center-left': 1.4, 'Center-right': 0.8, 'Far-left': 1.6, 'Far-right': 1.3, 'Left': 1.5, 'Right': 0.7, 'Conservative': 0.7, 'Liberal': 1.3, 'Progressive': 1.5, 'Socialist': 1.4, 'Capitalist': 0.8, 'Nationalism': 1.2, 'Populism': 1.7, 'Technocratic': 1.1, 'Environmentalism': 1.2, 'Social Justice': 1.6, 'Labor-rights': 1.4, 'Individual-rights': 1.3, 'Religious': 1.1, 'Free-market': 0.9, 'Protectionist': 1.2, 'Innovation': 1.1, 'Pacifist': 1.2, 'Traditionalist': 0.8, 'Rural': 1.2, 'Modernist': 1.3, 'Regionalist': 1.3, 'Anti-corruption': 1.9},
    '기술혁신': {'Centrist': 1.2, 'Center-left': 1.3, 'Center-right': 1.4, 'Far-left': 1.0, 'Far-right': 0.9, 'Left': 1.2, 'Right': 1.3, 'Conservative': 0.8, 'Liberal': 1.5, 'Progressive': 1.6, 'Socialist': 1.1, 'Capitalist': 1.6, 'Nationalism': 1.1, 'Populism': 0.9, 'Technocratic': 1.9, 'Environmentalism': 1.4, 'Social Justice': 1.2, 'Labor-rights': 0.8, 'Individual-rights': 1.4, 'Religious': 0.7, 'Free-market': 1.6, 'Protectionist': 0.7, 'Innovation': 2.0, 'Pacifist': 1.1, 'Traditionalist': 0.6, 'Rural': 0.8, 'Modernist': 1.9, 'Regionalist': 0.9, 'Anti-corruption': 1.2},
    '외교관계': {'Centrist': 1.3, 'Center-left': 1.2, 'Center-right': 1.1, 'Far-left': 0.8, 'Far-right': 0.7, 'Left': 1.1, 'Right': 1.0, 'Conservative': 1.0, 'Liberal': 1.3, 'Progressive': 1.2, 'Socialist': 0.9, 'Capitalist': 1.4, 'Nationalism': 0.7, 'Populism': 0.8, 'Technocratic': 1.3, 'Environmentalism': 1.2, 'Social Justice': 1.1, 'Labor-rights': 1.0, 'Individual-rights': 1.2, 'Religious': 0.9, 'Free-market': 1.5, 'Protectionist': 0.7, 'Innovation': 1.4, 'Pacifist': 1.6, 'Traditionalist': 0.8, 'Rural': 0.9, 'Modernist': 1.4, 'Regionalist': 0.8, 'Anti-corruption': 1.3},
    '정상상태': {'Centrist': 1.3, 'Center-left': 1.0, 'Center-right': 1.2, 'Far-left': 0.8, 'Far-right': 0.8, 'Left': 0.9, 'Right': 1.1, 'Conservative': 1.2, 'Liberal': 1.1, 'Progressive': 1.0, 'Socialist': 0.9, 'Capitalist': 1.2, 'Nationalism': 1.0, 'Populism': 0.9, 'Technocratic': 1.2, 'Environmentalism': 1.1, 'Social Justice': 1.0, 'Labor-rights': 1.0, 'Individual-rights': 1.1, 'Religious': 1.1, 'Free-market': 1.2, 'Protectionist': 1.0, 'Innovation': 1.1, 'Pacifist': 1.2, 'Traditionalist': 1.1, 'Rural': 1.0, 'Modernist': 1.1, 'Regionalist': 1.0, 'Anti-corruption': 1.0}
}

# 주요 대형 정당
major_parties = {
    '중앙당': ['Centrist', 'Center-right', 'Center-left', 'Conservative', 'Liberal', 'Progressive'],
    '통합 트라야비야': ['Center-right', 'Right', 'Conservative', 'Nationalism', 'Populism'],
    '사회민주당': ['Center-left', 'Progressive', 'Social Justice', 'Left', 'Labor-rights', 'Centrist'],
    '자유민주연합': ['Liberal', 'Right', 'Free-market', 'Individual-rights', 'Conservative', 'Center-right', 'Technocratic'],
}

# 중형 규모 정당
medium_parties = {
    '개혁당': ['Liberal', 'Right', 'Innovation', 'Progressive', 'Center-right', 'Technocratic'],
    '국가를 위한 보수당': ['Nationalism', 'Right', 'Conservative', 'Religious', 'Free-market'],
    '국민자유전선': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist'],
    '민주시민모임': ['Center-left', 'Progressive', 'Social Justice', 'Environmentalism', 'Labor-rights'],
    '녹색당': ['Environmentalism', 'Progressive', 'Social Justice', 'Centrist', 'Left'],
    '새희망당': ['Right', 'Conservative', 'Traditionalist', 'Nationalism', 'Protectionist'],
    '시민이 모였다!': ['Centrist', 'Anti-corruption', 'Progressive', 'Center-left', 'Left'],
    '자유혁신당': ['Center-left', 'Left', 'Progressive', 'Innovation', 'Environmentalism', 'Technocratic'],
    '진보를 외치다': ['Left', 'Progressive', 'Social Justice', 'Environmentalism', 'Anti-corruption'],
    '청년당': ['Progressive', 'Innovation', 'Social Justice', 'Center-left', 'Centrist'],
}

# 소수 정당
minor_parties = {
    '공산당': ['Far-left', 'Socialist', 'Social Justice', 'Progressive'],
    '과학기술당': ['Technocratic', 'Innovation', 'Progressive', 'Environmentalism'],
    '국민행동당': ['Populism', 'Right', 'Nationalism', 'Anti-corruption', 'Conservative'],
    '노동자당': ['Left', 'Labor-rights', 'Social Justice', 'Progressive', 'Socialist'],
    '보호하자 자연!': ['Environmentalism', 'Progressive', 'Social Justice', 'Left'],
    '농민당': ['Rural', 'Right', 'Protectionist', 'Conservative'],
    '미래당': ['Technocratic', 'Innovation', 'Progressive', 'Environmentalism'],
    '보호하라!': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist'],
    '생명당': ['Environmentalism', 'Progressive', 'Social Justice', 'Centrist'],
    '전사회당': ['Far-left', 'Socialist', 'Social Justice', 'Progressive'],
    '정의': ['Social Justice', 'Left', 'Progressive', 'Environmentalism', 'Anti-corruption'],
    '통일당': ['Pacifist', 'Conservative', 'Centrist', 'Right', 'Nationalism'],
    '특이점이 온다': ['Technocratic', 'Modernist', 'Innovation', 'Progressive'],
    '평화': ['Pacifist', 'Environmentalism', 'Social Justice', 'Progressive'],
}

# 지역 정당
regional_parties = {
    '그미즈리 민주당': {'region': '그미즈리', 'ideology': ['Centrist', 'Center-left', 'Progressive', 'Social Justice', 'Environmentalism', 'Labor-rights', 'Regionalist']},
    '도마니 연합': {'region': '도마니', 'ideology': ['Centrist', 'Center-right', 'Conservative', 'Technocratic', 'Innovation', 'Regionalist']},
    '림덴시를 위하여': {'region': '림덴시', 'ideology': ['Rural', 'Conservative', 'Traditionalist', 'Protectionist', 'Regionalist']},
    '살기좋은 안텐시': {'region': '안텐시', 'ideology': ['Environmentalism', 'Progressive', 'Social Justice', 'Centrist', 'Left', 'Regionalist']},
    '세오어 보호당': {'region': '그라나데, 포어', 'ideology': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist', 'Regionalist']},
    '테트라 인민당': {'region': '테트라', 'ideology': ['Socialist', 'Left', 'Progressive', 'Social Justice', 'Labor-rights', 'Regionalist']},
    '하파차의 후예': {'region': '하파차', 'ideology': ['Nationalism', 'Right', 'Conservative', 'Traditionalist', 'Regionalist', 'Protectionist']}
}

# 정당 선호도
party_preference_map = {
    # 아이리카 주
    "메초오비카": {"Conservative": 1.28, "Progressive": 0.72},
    "아브레": {"Conservative": 1.21, "Progressive": 0.79},
    "피에트라": {"Conservative": 0.83, "Progressive": 1.17},
    "아이리카": {"Conservative": 0.96, "Progressive": 1.04},
    "메르네": {"Conservative": 0.75, "Progressive": 1.25},
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
    "오크모": {"Conservative": 1.18, "Progressive": 0.82},
    "미톤노": {"Conservative": 0.97, "Progressive": 1.03},
    "페아그": {"Conservative": 0.91, "Progressive": 1.09},
    "그미즈리": {"Conservative": 0.85, "Progressive": 1.15},
    "아센시": {"Conservative": 1.02, "Progressive": 0.98},
    "메깅고": {"Conservative": 0.94, "Progressive": 1.06},
    "호오토": {"Conservative": 1.11, "Progressive": 0.89},
    "키에오": {"Conservative": 0.93, "Progressive": 1.07},

    # 도마니 주
    "오브니": {"Conservative": 0.92, "Progressive": 1.08},
    "바스바드": {"Conservative": 1.07, "Progressive": 0.93},
    "케릴티": {"Conservative": 0.91, "Progressive": 1.09},
    "메고기": {"Conservative": 1.04, "Progressive": 0.96},
    "에링고": {"Conservative": 1.00, "Progressive": 1.00},
    "커피": {"Conservative": 1.02, "Progressive": 0.98},
    "즈조이": {"Conservative": 0.94, "Progressive": 1.06},
    "가안": {"Conservative": 1.01, "Progressive": 0.99},
    "브고홀": {"Conservative": 0.93, "Progressive": 1.07},
    "모옹홀": {"Conservative": 1.03, "Progressive": 0.97},
    "메옹": {"Conservative": 0.95, "Progressive": 1.05},

    # 림덴시 주
    "파미즈": {"Conservative": 0.82, "Progressive": 1.18},
    "스피가": {"Conservative": 0.91, "Progressive": 1.09},
    "아르고": {"Conservative": 0.84, "Progressive": 1.16},
    "모리고": {"Conservative": 0.93, "Progressive": 1.07},
    "펜보드": {"Conservative": 0.85, "Progressive": 1.15},
    "메바치": {"Conservative": 0.92, "Progressive": 1.08},
    "모호카": {"Conservative": 0.83, "Progressive": 1.17},
    "린토카": {"Conservative": 0.94, "Progressive": 1.06},
    "낙소": {"Conservative": 0.86, "Progressive": 1.14},
    "보빈": {"Conservative": 0.91, "Progressive": 1.09},
    "라토카": {"Conservative": 0.87, "Progressive": 1.13},
    "세오고": {"Conservative": 0.90, "Progressive": 1.10},
    "시안": {"Conservative": 0.84, "Progressive": 1.16},
    "보어": {"Conservative": 0.89, "Progressive": 1.11},

    # 메세기 주
    "크라나": {"Conservative": 1.01, "Progressive": 0.99},
    "나다이": {"Conservative": 1.12, "Progressive": 0.88},
    "옹피오": {"Conservative": 0.92, "Progressive": 1.08},
    "메세기": {"Conservative": 1.03, "Progressive": 0.97},
    "포크란": {"Conservative": 1.11, "Progressive": 0.89},
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
    "에디아다": {"Conservative": 0.86, "Progressive": 1.14},
    "리에다": {"Conservative": 0.83, "Progressive": 1.17},

    # 미치바 주
    "메고이오": {"Conservative": 0.81, "Progressive": 1.19},
    "우프레나": {"Conservative": 0.92, "Progressive": 1.08},
    "미츠비": {"Conservative": 0.80, "Progressive": 1.20},
    "알고": {"Conservative": 0.84, "Progressive": 1.16},
    "산시아고": {"Conservative": 0.91, "Progressive": 1.09},
    "나릴로": {"Conservative": 0.83, "Progressive": 1.17},
    "유프란": {"Conservative": 0.92, "Progressive": 1.08},
    "미치바": {"Conservative": 0.85, "Progressive": 1.15},

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
    "리안토": {"Conservative": 0.93, "Progressive": 1.07},
    "오고소": {"Conservative": 1.04, "Progressive": 0.96},
    "민마": {"Conservative": 1.10, "Progressive": 0.90},
    "테안타": {"Conservative": 0.92, "Progressive": 1.08},
    "모반토": {"Conservative": 1.05, "Progressive": 0.95},
    "레링가": {"Conservative": 1.09, "Progressive": 0.91},

    # 세그레차 주
    "하롱골": {"Conservative": 1.22, "Progressive": 0.78},
    "미골": {"Conservative": 1.13, "Progressive": 0.87},
    "메링골": {"Conservative": 1.21, "Progressive": 0.79},
    "세골": {"Conservative": 1.12, "Progressive": 0.88},
    "키골": {"Conservative": 1.20, "Progressive": 0.80},
    "리에골": {"Conservative": 1.11, "Progressive": 0.89},
    "페아골": {"Conservative": 1.23, "Progressive": 0.77},
    "베아골": {"Conservative": 1.14, "Progressive": 0.86},

    # 안텐시 주
    "모호보드": {"Conservative": 0.91, "Progressive": 1.09},
    "아핀고": {"Conservative": 0.82, "Progressive": 1.18},
    "비에노": {"Conservative": 0.93, "Progressive": 1.07},
    "시세디": {"Conservative": 0.84, "Progressive": 1.16},
    "메즈노": {"Conservative": 0.89, "Progressive": 1.11},
    "아신가": {"Conservative": 0.83, "Progressive": 1.17},
    "키르가": {"Conservative": 0.92, "Progressive": 1.08},

    # 카리아-로 주
    "노베라니나": {"Conservative": 1.01, "Progressive": 0.99},
    "아르모텐타": {"Conservative": 1.12, "Progressive": 0.88},
    "피고모싱고메고차바데다": {"Conservative": 0.93, "Progressive": 1.07},
    "미베이토메고차피덴타": {"Conservative": 1.04, "Progressive": 0.96},
    "안트로아싱가": {"Conservative": 0.92, "Progressive": 1.08},

    # 테트라 주
    "아젠타": {"Conservative": 0.92, "Progressive": 1.08},
    "아칸타": {"Conservative": 1.03, "Progressive": 0.97},
    "파르티엔타": {"Conservative": 0.94, "Progressive": 1.06},
    "유칸타": {"Conservative": 1.02, "Progressive": 0.98},
    "테트리다모스": {"Conservative": 0.91, "Progressive": 1.09},
    "테트리비제모스": {"Conservative": 1.04, "Progressive": 0.96},
    "테타": {"Conservative": 0.93, "Progressive": 1.07},

    # 포어 주
    "메네트리포어": {"Conservative": 0.92, "Progressive": 1.08},
    "안트리포어": {"Conservative": 1.03, "Progressive": 0.97},
    "라간": {"Conservative": 0.94, "Progressive": 1.06},
    "안파": {"Conservative": 1.02, "Progressive": 0.98},
    "테사": {"Conservative": 0.91, "Progressive": 1.09},
    "아르테": {"Conservative": 1.04, "Progressive": 0.96},
    "세가": {"Conservative": 0.93, "Progressive": 1.07},
    "오르도기": {"Conservative": 1.01, "Progressive": 0.99},

    # 하파차 주
    "파시벤토": {"Conservative": 0.92, "Progressive": 1.08},
    "오고이모": {"Conservative": 1.03, "Progressive": 0.97},
    "미느리오": {"Conservative": 0.92, "Progressive": 1.08},
    "산세오": {"Conservative": 1.11, "Progressive": 0.89},
    "아스타나": {"Conservative": 0.88, "Progressive": 1.12},
    "티레니오": {"Conservative": 0.94, "Progressive": 1.06},
    "비엥고": {"Conservative": 0.91, "Progressive": 1.09},
    "아린키고": {"Conservative": 1.02, "Progressive": 0.98},
    "하싱고": {"Conservative": 0.93, "Progressive": 1.07},
    "모잉고": {"Conservative": 1.01, "Progressive": 0.99},
    "하르고": {"Conservative": 0.92, "Progressive": 1.08},
}

def calculate_priority(event):
    # 각 요소에 대한 점수와 가중치
    impact_score = event['impact'] * 1.5  # 영향력
    frequency_score = event['frequency'] * 1.2  # 빈도
    importance_score = event['importance']
    
    # 총 점수 계산
    total_score = impact_score + frequency_score + importance_score
    return total_score

def get_priority_event():
    # 가중치에 따라 사건 선택
    events_list = list(events.keys())
    pr = [events[event]['frequency'] for event in events_list]
    return random.choices(events_list, weights=pr)[0]

def calculate_population_density(province_info):
    # 인구 밀도 계산
    density = province_info['인구'] / province_info['면적']
    return density

def calculate_party_preference_index(province_info_row):
    # 주 및 행정구역에 따른 개인 선호 정당 지수 계산
    state = province_info_row['주']
    district = province_info_row['행정구역']

    # 각 주와 행정구역에 대한 정치적 성향을 기반으로 선호 지수 설정
    preference_index = {'Conservative': 1.0, 'Progressive': 1.0}

    # 주에 대한 선호 지수 반영
    if state in party_preference_map:
        for party, impact in party_preference_map[state].items():
            preference_index[party] *= impact

    # 행정구역에 대한 선호 지수 반영
    if district in party_preference_map:
        for party, impact in party_preference_map[district].items():
            preference_index[party] *= impact

    return preference_index  # 각 정당에 대한 상대적 선호 지수


def calculate_indexes(province_info):
    # 도시지수 계산 (인구밀도가 높은 경우 도시지수가 높다고 가정)
    province_info['도시지수'] = province_info['인구밀도'] / province_info['인구밀도'].max() * 100

    # 주별로 경제지수를 계산 (주별 인구와 면적을 고려한 단순 경제지수 가정)
    economic_indexes = province_info.groupby('주').apply(
        lambda x: (x['인구'].sum() / x['면적'].sum()) / (province_info['인구'].sum() / province_info['면적'].sum()) * 100
    ).reset_index(name='경제지수')
    
    province_info = province_info.merge(economic_indexes, on='주')
        
    # 주 지수 계산 (예시: 주별 인구 밀도 평균)
    province_info['주지수'] = province_info.groupby('주')['인구밀도'].transform('mean')
    
    # 행정구역 지수 계산 (예시: 행정구역별 인구 밀도 평균)
    province_info['행정구역지수'] = province_info.groupby('행정구역')['인구밀도'].transform('mean')
    
    return province_info

def logistic_function(x, L=2, k=0.05, x0=50):
    # 로지스틱 함수: x가 증가할수록 0과 L 사이의 값을 반환 (k는 기울기 조절)
    exponent = -k * (x - x0)
    exponent = min(max(exponent, -100), 100)  # 지수 함수 오버플로 방지
    return (L / (1 + np.exp(exponent))) / 10 + 1 # 0.1 배수 + 1

def adjust_alignment_with_indexes(vote_shares, province_info_row, event):
    city_index = province_info_row['도시지수'] # 주별 도시 및 경제 지수를 기반으로 정당별 투표율 조정
    economic_index = province_info_row['경제지수'] # 경제 지수를 추가
    party_preference_index = calculate_party_preference_index(province_info_row)  # 개인 선호 정당 지수를 추가

    # 정치 성향에 따라 지수 영향을 반영 (로지스틱 함수로 조정)
    # L: 최대 투표율, k: 기울기, x0: 기준값, city_index: 도시지수, economic_index: 경제지수
    # 범진보 / 범보수 정당의 투표율 조정
    
    # 정렬에 따른 투표율 조정
    alignment_impact = {
        'Centrist': logistic_function(city_index, L=3.5, k=0.10, x0=50) * logistic_function(economic_index, L=3.5, k=0.10, x0=50),
        'Center-left': logistic_function(city_index, L=3.0, k=0.08, x0=50) * logistic_function(economic_index, L=3.0, k=0.08, x0=50),
        'Center-right': logistic_function(city_index, L=3.2, k=0.09, x0=50) * logistic_function(economic_index, L=3.2, k=0.09, x0=50),
        'Social Justice': logistic_function(city_index, L=3.2, k=0.09, x0=47) * logistic_function(economic_index, L=2.5, k=0.05, x0=50),
        'Liberal': logistic_function(city_index, L=3.0, k=0.08, x0=48) * logistic_function(economic_index, L=3.0, k=0.08, x0=48),
        'Progressive': logistic_function(city_index, L=3.5, k=0.10, x0=45) * logistic_function(economic_index, L=2.8, k=0.07, x0=50),
        'Socialist': logistic_function(city_index, L=3.5, k=0.10, x0=45) * logistic_function(economic_index, L=2.5, k=-0.04, x0=50),
        'Right': logistic_function(city_index, L=2.0, k=-0.03, x0=52) * logistic_function(economic_index, L=2.5, k=0.05, x0=48),
        'Far-right': logistic_function(city_index, L=1.3, k=-0.02, x0=55) * logistic_function(economic_index, L=1.5, k=0.03, x0=45),
        'Nationalism': logistic_function(city_index, L=1.8, k=-0.03, x0=52) * logistic_function(economic_index, L=2.0, k=0.04, x0=48),
        'Technocratic': logistic_function(city_index, L=2.8, k=0.07, x0=48) * logistic_function(economic_index, L=2.8, k=0.07, x0=48),
        'Conservative': logistic_function(city_index, L=2.2, k=-0.03, x0=52) * logistic_function(economic_index, L=2.5, k=0.06, x0=48),
        'Free-market': logistic_function(city_index, L=2.5, k=0.06, x0=50) * logistic_function(economic_index, L=2.8, k=0.08, x0=48),
        'Environmentalism': logistic_function(city_index, L=2.0, k=0.06, x0=50) * logistic_function(economic_index, L=1.8, k=-0.03, x0=52),
        'Traditionalist': logistic_function(city_index, L=1.6, k=-0.03, x0=52) * logistic_function(economic_index, L=2.2, k=0.05, x0=48),
    }

    # 정당별 투표율에 정렬 영향 반영
    for party in vote_shares.keys():
        all_parties = {**major_parties, **medium_parties, **minor_parties, **regional_parties}
        if party in all_parties:
            if party in regional_parties: vote_shares[party] *= 10.0  # 지역 정당의 투표율을 높게 설정
            for alignment in all_parties[party]:
                if alignment in alignment_impact:
                    alignment_score = alignment_impact.get(alignment, 1.0)
                    #print(f"{party} 정당의 정렬 {alignment}에 대한 영향: {alignment_score}")
                    vote_shares[party] *= alignment_score
                if alignment in party_preference_index:
                    preference_score = party_preference_index.get(alignment, 1.0)
                    #print(f"{party} 정당의 선호도 {alignment}에 대한 영향: {preference_score}")
                    vote_shares[party] *= preference_score
        else: raise ValueError(f"정당 {party}에 대한 정치 성향이 없습니다.")
    return vote_shares

def calculate_vote_shares(event, state, row):
    # 기본 투표율 계산
    regional_party_found = False  # 지역 정당 존재 여부 확인
    relevant_regional_parties = {}  # 해당 주의 지역 정당만 포함

    for party, party_state in regional_parties.items():
        if party_state['region'].find(',') != -1:  # 여러 지역에 걸쳐 있는 경우
            regions = party_state['region'].split(', ')
            formatted_state = state.strip().lower()
            if any((region.strip() + " 주").lower() == formatted_state for region in regions):
                regional_party_found = True
                relevant_regional_parties[party] = party_state
        else:
            formatted_party_state = (party_state['region'] + " 주").strip().lower()
            formatted_state = state.strip().lower()
            if formatted_party_state == formatted_state:
                regional_party_found = True
                relevant_regional_parties[party] = party_state

    if regional_party_found: # 지역 정당이 있는 경우
        while True:
            ma, me, mi, reg = random.uniform(40.0, 60.0), random.uniform(20.0, 30.0), random.uniform(10.0, 20.0), random.uniform(10.0, 20.0)
            if 90.0 < ma + me + mi + reg < 110.0: break
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(0, me) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))]
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))]
    else: # 지역 정당이 없는 경우
        while True:
            ma, me, mi, reg = random.uniform(40.0, 60.0), random.uniform(20.0, 30.0), random.uniform(10.0, 20.0), random.uniform(0.0, 0.0)
            if 90.0 < ma + me + mi + reg < 110.0: break
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(0, me) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))]
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))]

    # 정당별 투표율 할당
    vote_shares = {}

    # 대형 정당, 중형 정당, 소수 정당, 지역 정당 순으로 반복
    all_parties = [
        (major_parties, major_votes),
        (medium_parties, medium_votes),
        (minor_parties, minor_votes),
        (relevant_regional_parties, reg_votes)
    ]
    
    # 정당별 투표율 계산 (event_impact 반영)
    for parties, votes in all_parties:
        for i, party in enumerate(parties.keys()):
            total_impact = 0
            for ideology in parties[party]: 
                total_impact += event_impact.get(event, {}).get(ideology, 1.0)
            party_impact = total_impact / len(parties[party])
            vote_shares[party] = round(votes[i] * party_impact, 3)
            # 지역 정당 vote_shares 출력
            #if party in relevant_regional_parties:
                #print(f"{party} 지역 정당의 투표율: {vote_shares[party]}")

    # 투표율 계산 후 정당 성향 및 도시/경제 지수 반영
    vote_shares = adjust_alignment_with_indexes(vote_shares, row, event)

    #print("조정된 상위 4개 정당의 투표율:", sorted(vote_shares.items(), key=lambda x: x[1], reverse=True)[:4])

    # 투표율이 95% 미만인 경우 조정
    total_votes = sum(vote_shares.values())
    while total_votes < random.uniform(95, 98):
        for party in vote_shares.keys(): vote_shares[party] *= 1.001
        total_votes = sum(vote_shares.values())

    # 투표율이 100%가 넘는 경우 조정
    total_votes = sum(vote_shares.values())
    while total_votes > random.uniform(95, 98):
        for party in vote_shares.keys(): vote_shares[party] /= 1.001
        total_votes = sum(vote_shares.values())

    return vote_shares

def process_data_with_indexes(province_info):
    print("선거 결과 데이터 생성 중 . . .")
    # 먼저 도시지수와 경제지수를 계산하여 추가
    province_info = calculate_indexes(province_info) # 도시지수, 경제지수, 주지수, 행정구역지수 추가
    data = [] # 결과 데이터를 저장할 리스트
    global_event = get_priority_event() # 전국적 사건 선택
    global_sub_event = random.choices(events[global_event]['subtypes']) # 전국적 사건의 세부 사건 선택
    print(f"전국적 사건: {global_event} - {global_sub_event[0]}")

    for state, cities in province_info.groupby('주'):
        #local_event = get_priority_event() # 주 단위 사건 선택
        #local_sub_event = random.choices(events[local_event]['subtypes']) # 주 단위 사건의 세부 사건 선택
        # 우선 순위에 따라 사건 선택
        #if calculate_priority(events[local_event]) > calculate_priority(events[global_event]):
           #local_event, local_sub_event = global_event, global_sub_event
        #사건이 같고 세부 사건이 다른 경우
        #if local_event == global_event: local_sub_event = global_sub_event # 세부 사건을 동일하게 설정
        for _, row in cities.iterrows(): # 주별 행정구역별로 반복
            result_row = {
                '주': state,
                '행정구역': row['행정구역'],
                '면적': row['면적'],
                '인구': row['인구'],
                '인구밀도': row['인구밀도'],
                '사건': global_event + ' - ' + global_sub_event[0], # 전국적 사건 및 세부 사건 추가 #local_event + " - " + local_sub_event[0]
                '도시지수': row['도시지수'],  # 계산된 도시지수 추가
                '경제지수': row['경제지수']   # 계산된 경제지수 추가
            }

            # 투표율 계산 및 조정
            vote_shares = calculate_vote_shares(global_event, state, row)  # row 인자 추가 (원래 local_event)
            result_row.update(vote_shares)
            
            # 무효표
            result_row['무효표'] = 100 - sum(vote_shares.values())
            
            # 총합 계산
            total = sum(vote_shares.values()) + result_row['무효표']
            result_row['총합'] = round(total, 3)
            
            data.append(result_row)
    
    return data

def read_province_info(file_path):
    # 파일에서 주별 정보 읽기
    try:
        province_info = pd.read_csv(file_path, sep=',', names=['행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        return province_info
    except Exception as e: raise ValueError(f"파일을 읽는 중 오류 발생: {e}")

def main():
    province_info = read_province_info('data/province_info.txt')
    province_info['주'] = province_info['주'].str.strip() # 주 이름 공백 제거

    if province_info is not None:
        data = process_data_with_indexes(province_info)
        df = pd.DataFrame(data)
        print("선거 결과 데이터 생성 완료")
        
        # 열 순서 정리
        columns_order = ['주', '행정구역', '면적', '인구', '인구밀도', '도시지수', '경제지수', '사건'] + \
                       list(major_parties.keys()) + list(medium_parties.keys()) + list(minor_parties.keys()) + \
                       list(regional_parties.keys()) + ['무효표', '총합']
        
        df = df[columns_order]
        df.to_excel('data/election_result.xlsx', index=False)
        print("선거 데이터를 파일에 저장했습니다.")

if __name__ == "__main__":
    main()