import pandas as pd
import numpy as np
import random

# 정치 성향 확장
alignments = [
    'Centrist', 'Center-left', 'Center-right', 'Far-left', 'Far-right',
    'Nationalism', 'Populism', 'Environmentalism', 'Third-position',
    'Single-issue', 'Hybrid', 'Religious', 'Progressive', 'Conservative',
    'Social Democracy', 'Social Justice', 'Liberal', 'Libertarian',
    'Anarchist', 'Monarchist', 'Technocratic', 'Agrarian', 'Federalist',
    'Unionist', 'Separatist', 'Reformist', 'Traditionalist', 'Militarist',
    'Pacifist', 'Globalist', 'Isolationist', 'Secular', 'Theocratic',
    'Socialist', 'Capitalist', 'Corporatist', 'Anti-establishment',
    'Regionalist', 'Urbanist', 'Rural-interest', 'Youth-focused',
    'Pensioners-interest', 'Direct-democratic', 'Authoritarian',
    'Anti-corruption', 'Transparent', 'Innovation', 'Industrialist',
    'Protectionist', 'Free-market', 'Labor-rights', 'Individual-rights',
    'Unification', 'Dialogue', 'Research', 'Digital', 'Modernist',
    'Autonomist', 'Economic-development', 'Big Tent', 'Anti-capitalist',
]

# 사건 확장
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

# 사건 영향 확장 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
event_impact = {
    '자연재해': {
        'Centrist': 0.9,
        'Progressive': 1.2,
        'Conservative': 0.8,
        'Environmentalism': 1.4,
        'Technocratic': 1.3,
        'Social Democracy': 1.2
    },
    '경제위기': {
        'Populism': 1.5,
        'Socialist': 1.3,
        'Capitalist': 0.7,
        'Conservative': 0.8,
        'Reformist': 1.2,
        'Anti-establishment': 1.4
    },
    '안보위기': {
        'Nationalism': 1.4,
        'Militarist': 1.5,
        'Pacifist': 0.6,
        'Conservative': 1.3,
        'Isolationist': 1.2,
        'Globalist': 0.8
    },
    '사회문제': {
        'Social Justice': 1.4,
        'Progressive': 1.3,
        'Conservative': 0.8,
        'Socialist': 1.3,
        'Reformist': 1.2,
        'Traditionalist': 0.7
    },
    '환경위기': {
        'Environmentalism': 1.6,
        'Progressive': 1.3,
        'Conservative': 0.8,
        'Technocratic': 1.2,
        'Green': 1.5,
        'Industrialist': 0.6
    },
    '정치스캔들': {
        'Anti-corruption': 1.5,
        'Progressive': 1.3,
        'Conservative': 0.8,
        'Reformist': 1.2,
        'Anti-establishment': 1.4,
        'Transparent': 1.2
    },
    '기술혁신': {
        'Technocratic': 1.5,
        'Progressive': 1.3,
        'Conservative': 0.8,
        'Innovation': 1.4,
        'Digital': 1.2,
        'Research': 1.1
    },
    '외교관계': {
        'Globalist': 1.5,
        'Nationalism': 0.8,
        'Conservative': 1.3,
        'Progressive': 1.2,
        'Diplomatic': 1.4,
        'Internationalist': 1.3
    },
    '정상상태': {
        'Centrist': 1.2,
        'Conservative': 1.1,
        'Progressive': 1.1,
        'Reformist': 1.2,
        'Traditionalist': 1.0,
        'Technocratic': 1.3
    }
}

# 정당 확장
major_parties = {
    '자유혁신당': ['Center-left', 'Progressive', 'Reformist'],
    '중앙당': ['Centrist', 'Big Tent', 'Moderate'],
    '통합당': ['Center-right', 'Conservative', 'Traditionalist'],
    '사회민주당': ['Social Democracy', 'Progressive', 'Labor'],
    '진보당': ['Progressive', 'Social Justice', 'Environmentalism', 'Labor'],
    '보수당': ['Conservative', 'Nationalist', 'Traditionalist', 'Religious'],
}

minor_parties = {
    '개혁당': ['Liberal', 'Reformist', 'Pro-business'],
    '민주통합당': ['Center-left', 'Big Tent', 'Progressive'],
    '미래연합': ['Technocratic', 'Modernist', 'Reform'],
    '평화당': ['Pacifist', 'Environmentalist', 'Social Justice'],
    '시민당': ['Direct-democratic', 'Anti-corruption', 'Transparent'],
    '녹색당': ['Environmentalism', 'Progressive', 'Social Justice'],
    '노동당': ['Socialist', 'Labor-rights', 'Anti-capitalist'],
    '국민당': ['Nationalist', 'Conservative', 'Traditional'],
    '정의당': ['Social Justice', 'Progressive', 'Labor'],
    '미래당': ['Technocratic', 'Innovation', 'Reform'],
    '자유민주연합': ['Liberal', 'Free-market', 'Individual-rights'],
    '청년당': ['Youth-focused', 'Progressive', 'Digital'],
    '농민당': ['Agrarian', 'Rural-interest', 'Protectionist'],
    '평화통일당': ['Pacifist', 'Unification', 'Dialogue'],
    '과학기술당': ['Technocratic', 'Innovation', 'Research']
}

# 지역 정당 확장
regional_parties = {
    '그미즈리 민주당': {'region': '그미즈리', 'ideology': ['Regionalist', 'Progressive', 'Autonomist']},
    '하파차 인민당': {'region': '하파차', 'ideology': ['Conservative', 'Traditional', 'Religious']},
    '도마니 연합': {'region': '도마니', 'ideology': ['Centrist', 'Economic-development', 'Modernist']},
    '테트라 인민당': {'region': '테트라', 'ideology': ['Socialist', 'Labor', 'Industrial']},
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
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))] # 대형 정당 투표율
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))] # 소수 정당 투표율
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))] # 지역 정당 투표율
    else:  # 지역 정당이 없는 경우
        while True:
            ma, mi, reg = random.uniform(40, 60), random.uniform(20.0, 40.0), 0.0 # 대형 정당, 소수 정당, 지역 정당
            if 90 <= ma + mi + reg <= 100: continue 
            if ma + mi + reg <= 100: break
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))] # 대형 정당 투표율
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
    print(f"전국적 사건: {global_event}")

    for state, cities in province_info.groupby('주'):
        for _, row in cities.iterrows():
            local_event = get_weighted_event()
            # 가중치에 따라 사건 선택
            if events[local_event]['priority'] < events[global_event]['priority']:
                local_event = global_event
            result_row = {
                '주': state + ' 주',
                '행정구역': row['행정구역'],
                '면적': row['면적'],
                '인구': row['인구'],
                '인구밀도': row['인구밀도'],
                '사건': local_event
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