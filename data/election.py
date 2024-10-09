import pandas as pd
import numpy as np
import random

# 정치 성향
alignments = [
    'Centrist', 'Center-left', 'Center-right', 'Far-left', 'Far-right',
    'Left', 'Right', 'Nationalism', 'Populism', 'Environmentalism',
    'Single-issue', 'Religious', 'Progressive', 'Conservative', 
    'Social Democracy', 'Social Justice', 'Liberal', 'Libertarian',
    'Technocratic', 'Agrarian', 'Federalist', 'Separatist',
    'Traditionalist', 'Militarist', 'Pacifist', 'Secular', 'Theocratic',
    'Socialist', 'Capitalist', 'Regionalist', 'Industrialist',
    'Protectionist', 'Free-market', 'Labor-rights', 'Individual-rights',
    'Unification', 'Innovation', 'Authoritarian', 'Anti-corruption', 
    'Transparency', 'Modernist', 'Autonomist', 'Economic-development'
]

# 사건
events = {
    '자연재해': {
        'priority': 9,
        'weight': 0.05,
        'subtypes': ['대지진', '태풍', '홍수', '가뭄', '화산폭발']
    },
    '경제위기': {
        'priority': 8,
        'weight': 0.08,
        'subtypes': ['금융위기', '무역전쟁', '인플레이션', '실업률급증', '산업붕괴']
    },
    '안보위기': {
        'priority': 10,
        'weight': 0.03,
        'subtypes': ['전쟁위협', '테러', '사이버공격', '국경분쟁', '내전']
    },
    '사회문제': {
        'priority': 6,
        'weight': 0.15,
        'subtypes': ['불평등심화', '교육위기', '고령화', '저출산', '주거난']
    },
    '환경위기': {
        'priority': 7,
        'weight': 0.1,
        'subtypes': ['기후변화', '대기오염', '수질오염', '생태계파괴', '자원고갈']
    },
    '정치스캔들': {
        'priority': 5,
        'weight': 0.12,
        'subtypes': ['부패', '권력남용', '선거조작', '정보유출', '정치자금비리']
    },
    '기술혁신': {
        'priority': 4,
        'weight': 0.15,
        'subtypes': ['AI혁명', '우주개발', '신재생에너지', '바이오기술', '양자컴퓨팅']
    },
    '외교관계': {
        'priority': 6,
        'weight': 0.12,
        'subtypes': ['동맹강화', '국제고립', '통상마찰', '문화충돌', '국제협력']
    },
    '정상상태': {
        'priority': 1,
        'weight': 0.2,
        'subtypes': ['안정기', '성장기', '조정기', '전환기', '회복기']
    }
}

# 사건 영향 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
events = {
    '자연재해': {
        'priority': 9,
        'weight': 0.05,
        'subtypes': ['대지진', '태풍', '홍수', '가뭄', '화산폭발']
    },
    '경제위기': {
        'priority': 8,
        'weight': 0.08,
        'subtypes': ['금융위기', '무역전쟁', '인플레이션', '실업률급증', '산업붕괴']
    },
    '안보위기': {
        'priority': 10,
        'weight': 0.03,
        'subtypes': ['전쟁위협', '테러', '사이버공격', '국경분쟁', '내전']
    },
    '사회문제': {
        'priority': 6,
        'weight': 0.15,
        'subtypes': ['불평등심화', '교육위기', '고령화', '저출산', '주거난']
    },
    '환경위기': {
        'priority': 7,
        'weight': 0.1,
        'subtypes': ['기후변화', '대기오염', '수질오염', '생태계파괴', '자원고갈']
    },
    '정치스캔들': {
        'priority': 5,
        'weight': 0.12,
        'subtypes': ['부패', '권력남용', '선거조작', '정보유출', '정치자금비리']
    },
    '기술혁신': {
        'priority': 4,
        'weight': 0.15,
        'subtypes': ['AI혁명', '우주개발', '신재생에너지', '바이오기술', '양자컴퓨팅']
    },
    '외교관계': {
        'priority': 6,
        'weight': 0.12,
        'subtypes': ['동맹강화', '국제고립', '통상마찰', '문화충돌', '국제협력']
    },
    '정상상태': {
        'priority': 1,
        'weight': 0.2,
        'subtypes': ['안정기', '성장기', '조정기', '전환기', '회복기']
    }
}

event_impact = {
    '자연재해': {
        'Centrist': 0.9, 'Center-left': 1.1, 'Center-right': 0.9, 'Far-left': 1.2, 'Far-right': 0.8, 'Left': 1.2, 'Right': 0.9,
        'Nationalism': 0.8, 'Populism': 1.0, 'Environmentalism': 1.4, 'Single-issue': 0.9, 'Religious': 0.9, 'Progressive': 1.2,
        'Conservative': 0.8, 'Social Democracy': 1.2, 'Social Justice': 1.1, 'Liberal': 1.0, 'Libertarian': 0.9, 'Technocratic': 1.3,
        'Agrarian': 0.8, 'Federalist': 0.9, 'Separatist': 0.8, 'Traditionalist': 0.9, 'Militarist': 0.7, 'Pacifist': 1.0, 'Secular': 1.1,
        'Theocratic': 0.8, 'Socialist': 1.3, 'Capitalist': 0.9, 'Regionalist': 0.9, 'Industrialist': 0.8, 'Protectionist': 0.9,
        'Free-market': 0.9, 'Labor-rights': 1.2, 'Individual-rights': 1.0, 'Unification': 1.0, 'Innovation': 1.1, 'Authoritarian': 0.9,
        'Anti-corruption': 1.1, 'Transparency': 1.2, 'Modernist': 1.1, 'Autonomist': 1.0, 'Economic-development': 0.9
    },
    '경제위기': {
        'Centrist': 0.9, 'Center-left': 1.1, 'Center-right': 1.2, 'Far-left': 1.4, 'Far-right': 1.2, 'Left': 1.3, 'Right': 1.2,
        'Nationalism': 1.1, 'Populism': 1.5, 'Environmentalism': 0.7, 'Single-issue': 0.8, 'Religious': 1.1, 'Progressive': 1.0,
        'Conservative': 1.1, 'Social Democracy': 1.4, 'Social Justice': 1.3, 'Liberal': 0.9, 'Libertarian': 1.2, 'Technocratic': 1.5,
        'Agrarian': 1.0, 'Federalist': 1.2, 'Separatist': 0.9, 'Traditionalist': 1.1, 'Militarist': 1.0, 'Pacifist': 0.9, 'Secular': 1.0,
        'Theocratic': 0.9, 'Socialist': 1.5, 'Capitalist': 0.7, 'Regionalist': 0.9, 'Industrialist': 1.3, 'Protectionist': 1.2,
        'Free-market': 0.8, 'Labor-rights': 1.3, 'Individual-rights': 0.9, 'Unification': 1.0, 'Innovation': 1.4, 'Authoritarian': 1.2,
        'Anti-corruption': 1.3, 'Transparency': 1.2, 'Modernist': 1.4, 'Autonomist': 1.0, 'Economic-development': 1.5
    },
    '안보위기': {
        'Centrist': 0.8, 'Center-left': 0.7, 'Center-right': 1.2, 'Far-left': 0.6, 'Far-right': 1.5, 'Left': 0.8, 'Right': 1.4,
        'Nationalism': 1.6, 'Populism': 1.5, 'Environmentalism': 0.5, 'Single-issue': 0.7, 'Religious': 1.2, 'Progressive': 0.6,
        'Conservative': 1.3, 'Social Democracy': 0.7, 'Social Justice': 0.7, 'Liberal': 0.8, 'Libertarian': 0.7, 'Technocratic': 1.1,
        'Agrarian': 1.1, 'Federalist': 1.3, 'Separatist': 1.2, 'Traditionalist': 1.4, 'Militarist': 1.7, 'Pacifist': 0.3, 'Secular': 1.0,
        'Theocratic': 1.1, 'Socialist': 0.8, 'Capitalist': 1.2, 'Regionalist': 1.1, 'Industrialist': 1.3, 'Protectionist': 1.4,
        'Free-market': 1.0, 'Labor-rights': 0.8, 'Individual-rights': 0.9, 'Unification': 1.1, 'Innovation': 1.1, 'Authoritarian': 1.5,
        'Anti-corruption': 1.0, 'Transparency': 0.8, 'Modernist': 1.0, 'Autonomist': 1.1, 'Economic-development': 1.3
    },
    '사회문제': {
        'Centrist': 1.2, 'Center-left': 1.1, 'Center-right': 1.0, 'Far-left': 0.9, 'Far-right': 0.8, 'Left': 1.1, 'Right': 1.0,
        'Nationalism': 0.9, 'Populism': 0.8, 'Environmentalism': 1.3, 'Single-issue': 1.1, 'Religious': 0.9, 'Progressive': 1.3,
        'Conservative': 0.8, 'Social Democracy': 1.2, 'Social Justice': 1.4, 'Liberal': 1.1, 'Libertarian': 0.9, 'Technocratic': 1.0,
        'Agrarian': 1.0, 'Federalist': 1.1, 'Separatist': 0.9, 'Traditionalist': 0.8, 'Militarist': 0.8, 'Pacifist': 1.1, 'Secular': 1.3,
        'Theocratic': 0.9, 'Socialist': 1.4, 'Capitalist': 0.7, 'Regionalist': 1.0, 'Industrialist': 0.8, 'Protectionist': 0.8,
        'Free-market': 0.9, 'Labor-rights': 1.4, 'Individual-rights': 1.2, 'Unification': 1.0, 'Innovation': 1.1, 'Authoritarian': 0.6,
        'Anti-corruption': 1.3, 'Transparency': 1.3, 'Modernist': 1.1, 'Autonomist': 1.0, 'Economic-development': 1.2
    },
    '환경위기': {
        'Centrist': 0.9, 'Center-left': 1.2, 'Center-right': 0.8, 'Far-left': 1.3, 'Far-right': 0.7, 'Left': 1.1, 'Right': 0.7,
        'Nationalism': 0.9, 'Populism': 1.0, 'Environmentalism': 1.6, 'Single-issue': 1.4, 'Religious': 0.8, 'Progressive': 1.2,
        'Conservative': 0.7, 'Social Democracy': 1.4, 'Social Justice': 1.2, 'Liberal': 0.9, 'Libertarian': 0.8, 'Technocratic': 1.1,
        'Agrarian': 1.1, 'Federalist': 0.9, 'Separatist': 0.8, 'Traditionalist': 0.7, 'Militarist': 0.6, 'Pacifist': 1.2, 'Secular': 1.1,
        'Theocratic': 0.8, 'Socialist': 1.4, 'Capitalist': 0.7, 'Regionalist': 1.0, 'Industrialist': 0.8, 'Protectionist': 0.9,
        'Free-market': 0.7, 'Labor-rights': 1.2, 'Individual-rights': 1.0, 'Unification': 1.0, 'Innovation': 1.3, 'Authoritarian': 0.7,
        'Anti-corruption': 1.1, 'Transparency': 1.0, 'Modernist': 1.1, 'Autonomist': 1.0, 'Economic-development': 1.2
    },
    '정치스캔들': {
        'Centrist': 1.1, 'Center-left': 1.2, 'Center-right': 0.8, 'Far-left': 1.3, 'Far-right': 1.5, 'Left': 1.4, 'Right': 1.0,
        'Nationalism': 0.8, 'Populism': 1.6, 'Environmentalism': 0.9, 'Single-issue': 1.0, 'Religious': 0.9, 'Progressive': 1.2,
        'Conservative': 0.7, 'Social Democracy': 1.4, 'Social Justice': 1.3, 'Liberal': 1.2, 'Libertarian': 1.1, 'Technocratic': 1.2,
        'Agrarian': 0.9, 'Federalist': 1.0, 'Separatist': 1.0, 'Traditionalist': 0.8, 'Militarist': 0.8, 'Pacifist': 0.7, 'Secular': 1.0,
        'Theocratic': 0.8, 'Socialist': 1.2, 'Capitalist': 1.0, 'Regionalist': 1.0, 'Industrialist': 0.9, 'Protectionist': 1.0,
        'Free-market': 1.0, 'Labor-rights': 1.2, 'Individual-rights': 1.1, 'Unification': 0.9, 'Innovation': 1.2, 'Authoritarian': 1.5,
        'Anti-corruption': 1.6, 'Transparency': 1.4, 'Modernist': 1.0, 'Autonomist': 1.1, 'Economic-development': 1.1
    },
    '기술혁신': {
        'Centrist': 1.2, 'Center-left': 1.1, 'Center-right': 1.3, 'Far-left': 1.4, 'Far-right': 0.9, 'Left': 1.3, 'Right': 1.1,
        'Nationalism': 1.0, 'Populism': 1.2, 'Environmentalism': 1.3, 'Single-issue': 1.0, 'Religious': 1.1, 'Progressive': 1.4,
        'Conservative': 1.0, 'Social Democracy': 1.3, 'Social Justice': 1.1, 'Liberal': 1.2, 'Libertarian': 1.3, 'Technocratic': 1.5,
        'Agrarian': 1.0, 'Federalist': 1.1, 'Separatist': 0.9, 'Traditionalist': 0.8, 'Militarist': 1.0, 'Pacifist': 1.1, 'Secular': 1.0,
        'Theocratic': 0.9, 'Socialist': 1.0, 'Capitalist': 1.4, 'Regionalist': 1.1, 'Industrialist': 1.4, 'Protectionist': 0.9,
        'Free-market': 1.5, 'Labor-rights': 1.1, 'Individual-rights': 1.1, 'Unification': 1.1, 'Innovation': 1.5, 'Authoritarian': 0.9,
        'Anti-corruption': 1.2, 'Transparency': 1.1, 'Modernist': 1.4, 'Autonomist': 1.1, 'Economic-development': 1.4
    },
    '외교관계': {
        'Centrist': 1.0, 'Center-left': 1.1, 'Center-right': 1.2, 'Far-left': 1.0, 'Far-right': 1.2, 'Left': 1.1, 'Right': 1.3,
        'Nationalism': 1.5, 'Populism': 1.2, 'Environmentalism': 0.8, 'Single-issue': 0.9, 'Religious': 1.0, 'Progressive': 1.1,
        'Conservative': 1.0, 'Social Democracy': 1.2, 'Social Justice': 1.0, 'Liberal': 1.1, 'Libertarian': 0.8, 'Technocratic': 1.2,
        'Agrarian': 1.0, 'Federalist': 1.1, 'Separatist': 1.0, 'Traditionalist': 1.0, 'Militarist': 1.2, 'Pacifist': 1.1, 'Secular': 1.0,
        'Theocratic': 0.9, 'Socialist': 1.0, 'Capitalist': 1.2, 'Regionalist': 1.0, 'Industrialist': 1.1, 'Protectionist': 1.1,
        'Free-market': 1.0, 'Labor-rights': 1.0, 'Individual-rights': 1.1, 'Unification': 1.1, 'Innovation': 1.1, 'Authoritarian': 1.0,
        'Anti-corruption': 1.1, 'Transparency': 1.2, 'Modernist': 1.1, 'Autonomist': 1.0, 'Economic-development': 1.1
    },
    '정상상태': {
        'Centrist': 1.0, 'Center-left': 1.1, 'Center-right': 0.9, 'Far-left': 0.8, 'Far-right': 0.9, 'Left': 1.0, 'Right': 1.0,
        'Nationalism': 1.0, 'Populism': 1.1, 'Environmentalism': 0.9, 'Single-issue': 0.8, 'Religious': 1.0, 'Progressive': 1.0,
        'Conservative': 1.0, 'Social Democracy': 1.0, 'Social Justice': 1.0, 'Liberal': 1.0, 'Libertarian': 1.0, 'Technocratic': 1.0,
        'Agrarian': 1.0, 'Federalist': 1.0, 'Separatist': 0.9, 'Traditionalist': 0.8, 'Militarist': 0.9, 'Pacifist': 1.0, 'Secular': 1.0,
        'Theocratic': 0.9, 'Socialist': 1.0, 'Capitalist': 1.0, 'Regionalist': 1.0, 'Industrialist': 1.0, 'Protectionist': 1.0,
        'Free-market': 1.0, 'Labor-rights': 1.0, 'Individual-rights': 1.0, 'Unification': 1.0, 'Innovation': 1.0, 'Authoritarian': 0.8,
        'Anti-corruption': 1.0, 'Transparency': 1.0, 'Modernist': 1.0, 'Autonomist': 1.0, 'Economic-development': 1.0
    }
}


# 주요 대형 정당
major_parties = {
    '자유혁신당': ['Center-left', 'Left', 'Progressive', 'Reformist'],
    '중앙당': ['Centrist', 'Right', 'Big Tent'],
    '통합 트라야비야': ['Center-right', 'Right', 'Conservative', 'Nationalism'],
    '사회민주당': ['Social Democracy', 'Left', 'Labor-rights'],
    '진보를 외치다': ['Left', 'Progressive', 'Social Justice', 'Environmentalism'],
    '보수당': ['Right', 'Conservative', 'Traditionalist', 'Religious'],
}

minor_parties = {
    '개혁당': ['Liberal', 'Right', 'Reformist'],
    '민주통합당': ['Center-left', 'Progressive'],
    '특이점이 온다': ['Technocratic', 'Modernist', 'Innovation'],
    '평화': ['Pacifist', 'Environmentalism', 'Social Justice'],
    '시민이 모였다!': ['Centrist', 'Anti-corruption', 'Transparency'],
    '녹색환경보호당': ['Environmentalism', 'Progressive'],
    '노동당': ['Socialist', 'Left', 'Labor-rights'],
    '국민행동당': ['Populism', 'Right'],
    '정의': ['Social Justice', 'Left'],
    '미래당': ['Technocratic', 'Innovation'],
    '자유민주연합': ['Liberal', 'Right', 'Free-market'],
    '청년당': ['Youth-focused', 'Progressive', 'Digital'],
    '농민당': ['Agrarian', 'Right', 'Protectionist'],
    '평화통일당': ['Pacifist', 'Unification'],
    '과학기술당': ['Technocratic', 'Innovation']
}

# 지역 정당
regional_parties = {
    '그미즈리 민주당': {'region': '그미즈리', 'ideology': ['Regionalist', 'Left', 'Autonomist']},
    '하파차의 후예': {'region': '하파차', 'ideology': ['Conservative', 'Right', 'Traditionalist']},
    '도마니 연합': {'region': '도마니', 'ideology': ['Centrist', 'Right', 'Economic-development']},
    '테트라 인민당': {'region': '테트라', 'ideology': ['Socialist', 'Left', 'Industrialist']},
    '세오어 보호당': {'region': '그라나데, 포어', 'ideology': ['Nationalism', 'Right']},
    '살기좋은 안텐시' : {'region': '안텐시', 'ideology': ['Environmentalism', 'Social Justice']},
    '림덴시에 어서오세요': {'region': '림덴시', 'ideology': ['Centrist', 'Big Tent']},
}


def get_weighted_event():
    events_list = list(events.keys())
    weights = [events[event]['weight'] for event in events_list]
    return random.choices(events_list, weights=weights)[0]

def calculate_vote_shares(event, state):
    # 기본 투표율 계산
    regional_party_found = False  # 지역 정당 존재 여부 확인
    relevant_regional_parties = {}  # 해당 주의 지역 정당만 포함

    for party, party_state in regional_parties.items():
        if party_state['region'].find(',') != -1:  # 여러 지역에 걸쳐 있는 경우 (예: 그라나데, 포어 주)
            regions = party_state['region'].split(', ')
            formatted_state = state.strip().lower()
            if any((region.strip() + " 주").lower() == formatted_state for region in regions):
                regional_party_found = True
                relevant_regional_parties[party] = party_state
        else:
            formatted_party_state = (party_state['region'] + " 주").strip().lower()
            formatted_state = state.strip().lower()
            if formatted_party_state == formatted_state:  # 지역 정당이 해당 주에 존재하는 경우
                regional_party_found = True
                relevant_regional_parties[party] = party_state

    if regional_party_found:  # 지역 정당이 있는 경우
        while True:
            ma, mi, reg = random.uniform(20.0, 40.0), random.uniform(0.0, 20.0), random.uniform(40.0, 60.0) # 대형 정당, 소수 정당, 지역 정당
            if 90 <= ma + mi + reg <= 100: continue
            if ma + mi + reg <= 100: break
        major_votes = [random.uniform(10, ma) for _ in range(len(major_parties))] # 대형 정당 투표율
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))] # 소수 정당 투표율
        reg_votes = [random.uniform(15, reg) for _ in range(len(relevant_regional_parties))] # 지역 정당 투표율
    else:  # 지역 정당이 없는 경우
        while True:
            ma, mi, reg = random.uniform(40, 60), random.uniform(20.0, 40.0), 0.0 # 대형 정당, 소수 정당, 지역 정당
            if 90 <= ma + mi + reg <= 100: continue 
            if ma + mi + reg <= 100: break
        major_votes = [random.uniform(10, ma) for _ in range(len(major_parties))] # 대형 정당 투표율
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))] # 소수 정당 투표율
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))] # 지역 정당 투표율 (0)

    # 정당별 투표율 할당
    vote_shares = {}

    # 대형 정당 투표율
    for i, party in enumerate(major_parties.keys()):
        party_impact = sum(event_impact.get(event, {}).get(ideology, 1.0) for ideology in major_parties[party]) / len(major_parties[party])
        vote_shares[party] = round(major_votes[i] * party_impact, 3)

    # 소수 정당 투표율
    for i, party in enumerate(minor_parties.keys()):
        party_impact = sum(event_impact.get(event, {}).get(ideology, 1.0) for ideology in minor_parties[party]) / len(minor_parties[party])
        vote_shares[party] = round(minor_votes[i] * party_impact, 3)

    # 지역 정당 투표율 (해당 주에서만)
    for i, party in enumerate(relevant_regional_parties.keys()):
        party_impact = sum(event_impact.get(event, {}).get(ideology, 1.0) for ideology in relevant_regional_parties[party]['ideology']) / len(relevant_regional_parties[party]['ideology'])
        vote_shares[party] = round(reg_votes[i] * party_impact, 3)

    # 투표율이 100%가 넘는 경우 조정
    total_votes = sum(vote_shares.values())
    while total_votes > random.uniform(95, 98):
        for party in vote_shares.keys():
            vote_shares[party] /= 1.001
        total_votes = sum(vote_shares.values())

    return vote_shares

def process_data(province_info):
    data = []
    # 주별로 하나의 사건 선택 (전국적 사건)
    global_event = get_weighted_event()
    global_sub_events = random.choices(events[global_event]['subtypes'])
    print(f"전국적 사건: {global_event} - {global_sub_events[0]}")

    for state, cities in province_info.groupby('주'):
        for _, row in cities.iterrows():
            local_event = get_weighted_event()
            local_sub_events = random.choices(events[local_event]['subtypes'])

            # 가중치에 따라 사건 선택
            if events[local_event]['priority'] > events[global_event]['priority']: # 지역 사건이 전국적 사건보다 중요한 경우
                local_event = global_event # 전국적 사건 선택 (혼자 동떨어진 지역 사건은 없음)
                local_sub_events = global_sub_events # 전국적 사건의 하위 사건 선택
            if events[local_event]['priority'] == events[global_event]['priority']: # 지역 사건과 전국적 사건이 동등한 경우
                local_sub_events = global_sub_events # 전국적 사건의 하위 사건 선택 (지역 사건은 무시)
            result_row = {
                '주': state + ' 주',
                '행정구역': row['행정구역'],
                '면적': row['면적'],
                '인구': row['인구'],
                '인구밀도': row['인구밀도'],
                '사건': local_event + ' - ' + local_sub_events[0]
            }

            # 투표율 계산 및 조정
            vote_shares = calculate_vote_shares(local_event, state)
            result_row.update(vote_shares)
            
            # 무효표
            result_row['무효표'] = 100 - sum(vote_shares.values())
            
            # 총합 계산
            total = sum(vote_shares.values()) + result_row['무효표']
            result_row['총합'] = round(total, 3)
            
            data.append(result_row)
    
    return data

def read_province_info(file_path):
    try:
        province_info = pd.read_csv(file_path, sep=',', names=['행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        return province_info
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    province_info = read_province_info('data/province_info.txt')
    if province_info is not None:
        data = process_data(province_info)
        df = pd.DataFrame(data)
        
        # 열 순서 정리
        columns_order = ['주', '행정구역', '면적', '인구', '인구밀도', '사건'] + \
                       list(major_parties.keys()) + list(minor_parties.keys()) + \
                       list(regional_parties.keys()) + ['무효표', '총합']
        
        df = df[columns_order]
        df.to_excel('data/election_result.xlsx', index=False)
        print("선거 결과 데이터가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()