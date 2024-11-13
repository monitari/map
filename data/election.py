import sys
import os
import pandas as pd
import numpy as np
import random
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

# 파일 경로 설정
province_info_path = 'data/mashup/province_info.txt'
election_result_path = 'data/xlsx/election_result.xlsx'

# 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'mashup'))

# 데이터 및 모듈 임포트
import data.mashup.party as party
import data.mashup.province_preference as pp
import data.mashup.alignments_events as alevent

# 경고 무시 설정
warnings.filterwarnings('ignore')

# 이벤트 및 영향도 데이터 로드
events = alevent.events
event_impact = alevent.event_impact

# 정당 데이터 로드
super_major_parties = party.super_major_parties
major_parties = party.major_parties
medium_parties = party.medium_parties
minor_parties = party.minor_parties
regional_parties = party.regional_parties

# 이념 스펙트럼 및 지역 선호도 데이터 로드
ideological_spectrum = pp.ideological_spectrum
province_preference = pp.province_preference

# 우선 이벤트 선택 함수
def get_priority_event():
    events_list = list(events.keys())
    pr = [events[event]['frequency'] for event in events_list]
    return random.choices(events_list, weights=pr)[0]

# 인구 밀도 계산 함수
def calculate_population_density(province_info):
    return province_info['인구'] / province_info['면적']

# 정당 선호도 지수 계산 함수
def calculate_party_preference_index(province_info_row):
    district = province_info_row['행정구역'].strip()
    preference_index = {'Conservative': 1.0, 'Progressive': 1.0}

    if district in province_preference:
        for party, impact in province_preference[district].items():
            preference_index[party] *= impact

    return pp.define_party_preference(preference_index['Conservative'], preference_index['Progressive'])

# 지수 계산 함수
def calculate_indexes(province_info):
    province_info['도시지수'] = province_info['인구밀도'] / province_info['인구밀도'].max() * 100
    economic_indexes = province_info.groupby('주').apply(
        lambda x: (x['인구'].sum() / x['면적'].sum()) / (province_info['인구'].sum() / province_info['면적'].sum()) * 100
    ).reset_index(name='경제지수')
    
    province_info = province_info.merge(economic_indexes, on='주')
    province_info['주지수'] = province_info.groupby('주')['인구밀도'].transform('mean')
    province_info['행정구역지수'] = province_info.groupby('행정구역')['인구밀도'].transform('mean')
    
    return province_info

# 로지스틱 함수
def logistic_function(x, L=2, k=0.05, x0=50):
    exponent = -k * (x - x0)
    exponent = min(max(exponent, -100), 100)
    returning = (L / (1 + np.exp(exponent))) / 10 + 1
    
    factor = np.random.normal(1.05, 0.1) 
    factor = min(max(factor, 0.85), 1.25)
    if returning > 1.0: returning *= factor
    else: returning /= factor
    return returning

# 정당 성향에 따른 투표율 조정 함수
def adjust_alignment_with_indexes(vote_shares, province_info_row):
    city_index = province_info_row['도시지수']
    economic_index = province_info_row['경제지수']
    party_preference_index = calculate_party_preference_index(province_info_row)

    alignment_impact = {
        'Far-left': logistic_function(city_index, L=3.7, k=0.10, x0=43) * logistic_function(economic_index, L=2.0, k=-0.03, x0=52),
        'Left': logistic_function(city_index, L=3.5, k=0.09, x0=47) * logistic_function(economic_index, L=2.5, k=0.05, x0=52),
        'Center-left': logistic_function(city_index, L=3.2, k=0.08, x0=45) * logistic_function(economic_index, L=2.8, k=0.07, x0=52),
        'Centrist': logistic_function(city_index, L=3.5, k=0.10, x0=50) * logistic_function(economic_index, L=3.5, k=0.10, x0=50),
        'Center-right': logistic_function(city_index, L=3.2, k=0.09, x0=50) * logistic_function(economic_index, L=3.2, k=0.09, x0=50),
        'Right': logistic_function(city_index, L=2.0, k=-0.03, x0=52) * logistic_function(economic_index, L=2.5, k=0.05, x0=48),
        'Far-right': logistic_function(city_index, L=1.3, k=-0.02, x0=55) * logistic_function(economic_index, L=1.5, k=0.03, x0=45),
        'Nationalism': logistic_function(city_index, L=1.8, k=-0.03, x0=52) * logistic_function(economic_index, L=2.0, k=0.04, x0=48),
        'Populism': logistic_function(city_index, L=2.5, k=0.06, x0=50) * logistic_function(economic_index, L=2.8, k=0.08, x0=48),
        'Social Democracy': logistic_function(city_index, L=3.2, k=0.09, x0=47) * logistic_function(economic_index, L=2.5, k=0.05, x0=50),
        'Liberalism': logistic_function(city_index, L=3.0, k=0.08, x0=48) * logistic_function(economic_index, L=3.0, k=0.08, x0=48),
        'Progressive': logistic_function(city_index, L=3.5, k=0.10, x0=45) * logistic_function(economic_index, L=2.8, k=0.07, x0=50),
        'Socialist': logistic_function(city_index, L=3.5, k=0.10, x0=45) * logistic_function(economic_index, L=2.5, k=-0.04, x0=50),
        'Conservatism': logistic_function(city_index, L=2.2, k=-0.03, x0=52) * logistic_function(economic_index, L=2.5, k=0.06, x0=48),
        'Technocratic': logistic_function(city_index, L=2.8, k=0.07, x0=48) * logistic_function(economic_index, L=2.8, k=0.07, x0=48),
        'Environmentalism': logistic_function(city_index, L=2.0, k=0.06, x0=50) * logistic_function(economic_index, L=1.8, k=-0.03, x0=52),
        'Traditionalist': logistic_function(city_index, L=1.6, k=-0.03, x0=52) * logistic_function(economic_index, L=2.2, k=0.05, x0=48),
    }

    all_parties = {**super_major_parties, **major_parties, **medium_parties, **minor_parties, **regional_parties}
    for party in vote_shares.keys():
        if party in all_parties:
            if party in regional_parties: vote_shares[party] *= 3.0
            for alignment in all_parties[party]:
                if alignment in alignment_impact: vote_shares[party] *= alignment_impact[alignment]
                if alignment in party_preference_index: vote_shares[party] *= party_preference_index[alignment]
        else: raise ValueError(f"정당 {party}에 대한 정치 성향이 없습니다. 이 정당은 외계에서 온 건가요? 👽🚀")
    return vote_shares

# 투표율 계산 함수
def calculate_vote_shares(event, state, row):
    regional_party_found = False
    relevant_regional_parties = {}

    formatted_state = state.strip().lower()
    for party, party_state in regional_parties.items():
        regions = party_state['region'].split(', ')
        if formatted_state in regions:
            regional_party_found = True
            relevant_regional_parties[party] = party_state

    state_vote_ranges = {
        "그미즈리": {
            "그미즈리 국민당": (1500.0, 2500.0), "그미즈리 민주당": (500.0, 1500.0),
            "그미즈리 녹색당": (0.0, 300.0), "그미즈리 통합당": (0.0, 200.0), "그미즈리 노동당": (0.0, 100.0), "default": (0.0, 50.0)
        },
        "하파차": {"하파차 민주연합": (150.0, 450.0), "default": (5.0, 50.0)},
        "테트라": (2000.0, 3000.0), "그라나데": (200.0, 500.0), "포어": (100.0, 300.0), "도마니": (100.0, 300.0),
        "안텐시": (25.0, 100.0), "림덴시": (25.0, 100.0), "default": (5.0, 50.0),
    }

    if regional_party_found:
        smajor_votes = np.random.uniform(20.0, 200.0, len(super_major_parties))
        major_votes = np.random.uniform(15.0, 100.0, len(major_parties))
        medium_votes = np.random.uniform(1.0, 20.0, len(medium_parties))
        minor_votes = np.random.uniform(0, 5.0, len(minor_parties))
        if state in state_vote_ranges:
            if state == "그미즈리" or state == "하파차":
                reg_votes = np.array([
                    np.random.uniform(*state_vote_ranges[state].get(party, state_vote_ranges[state]["default"]))
                    for party in relevant_regional_parties
                ])
            else: reg_votes = np.random.uniform(*state_vote_ranges[state], len(relevant_regional_parties))
        else: reg_votes = np.random.uniform(*state_vote_ranges["default"], len(relevant_regional_parties))
    else:
        smajor_votes = np.random.uniform(20.0, 200.0, len(super_major_parties))
        major_votes = np.random.uniform(15.0, 100.0, len(major_parties))
        medium_votes = np.random.uniform(1.0, 20.0, len(medium_parties))
        minor_votes = np.random.uniform(0, 5.0, len(minor_parties))
        reg_votes = np.zeros(len(relevant_regional_parties))

    vote_shares = {}
    all_parties = [
        (super_major_parties, smajor_votes),
        (major_parties, major_votes),
        (medium_parties, medium_votes),
        (minor_parties, minor_votes),
        (relevant_regional_parties, reg_votes)
    ]

    for parties, votes in all_parties:
        for i, party in enumerate(parties.keys()):
            total_impact = np.prod([event_impact.get(event, {}).get(ideology, 1.0) for ideology in parties[party]])
            if party in relevant_regional_parties: total_impact *= 1.5
            total_impact = min(max(total_impact, 0.1), 2.0)
            vote_shares[party] = round(votes[i] * total_impact, 3)
    
    vote_shares = adjust_alignment_with_indexes(vote_shares, row)

    total_votes = sum(vote_shares.values())
    target_votes = np.random.uniform(96, 98)
    adjustment_factor = target_votes / total_votes

    for party in vote_shares.keys(): vote_shares[party] *= adjustment_factor

    return vote_shares

# 데이터 처리 함수
def process_state_data(state, cities, global_event, global_sub_event):
    data = []
    for _, row in cities.iterrows():
        result_row = {
            '주': state,
            '행정구역': row['행정구역'].strip(),
            '세부행정구역': row['세부행정구역'],
            '면적': row['면적'],
            '인구': row['인구'],
            '인구밀도': row['인구밀도'],
            '사건': f"{global_event} - {global_sub_event}",
            '도시지수': row['도시지수'],
            '경제지수': row['경제지수']
        }

        vote_shares = calculate_vote_shares(global_event, state, row)
        result_row.update(vote_shares)
        result_row['무효표'] = 100 - sum(vote_shares.values())
        result_row['총합'] = round(sum(vote_shares.values()) + result_row['무효표'], 3)
        
        data.append(result_row)
    return data

# 데이터 처리 함수
def process_data_with_indexes(province_info):
    province_info = calculate_indexes(province_info)
    data = []
    global_event = get_priority_event()
    global_sub_event = random.choice(events[global_event]['subtypes'])
    print(f"전국적 사건 발생! 🌍 {global_event} - {global_sub_event}, 과연 민심은 어떠할까요? 🤔")

    total_rows = len(province_info)
    bar_length = 40

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_state_data, state, cities, global_event, global_sub_event): state for state, cities in province_info.groupby('주')}
        processed_rows = 0
        for future in as_completed(futures):
            state_data = future.result()
            data.extend(state_data)
            processed_rows += len(state_data)
            if processed_rows % 10 == 0 or processed_rows == total_rows:
                progress = processed_rows / total_rows
                block = int(bar_length * progress)
                bar = '█' * block + '-' * (bar_length - block)
                sys.stdout.write(f"\r선거 집계 중: [{bar}] {processed_rows}/{total_rows} - 아직도 계산 중인데, 커피 한 잔 하실래요? ☕️")
                sys.stdout.flush()

    sys.stdout.write("\r" + " " * (bar_length + 80) + "\r")
    sys.stdout.write(f"선거 결과 데이터📊 생성 완료! {election_result_path}에 저장했어요. 커피 다 마셨나요? ☕️\n")
    sys.stdout.flush()
    return data

# 지역 정보 파일 읽기 함수
def read_province_info(file_path):
    try:
        province_info = pd.read_csv(file_path, sep=',', names=['세부행정구역', '행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        return province_info
    except Exception as e: raise ValueError(f"파일을 읽는 중 오류 {e}. 설마 파일이 외계어로 작성된 건 아니겠죠? 👽📄")

# 메인 함수
def main():
    province_info = read_province_info(province_info_path)
    province_info['주'] = province_info['주'].str.strip()

    if province_info is not None:
        data = process_data_with_indexes(province_info)
        df = pd.DataFrame(data)

        columns_order = ['주', '행정구역', '세부행정구역', '면적', '인구', '인구밀도', '도시지수', '경제지수', '사건'] + \
                        list(super_major_parties.keys()) + list(major_parties.keys()) + list(medium_parties.keys()) + \
                       list(minor_parties.keys()) + list(regional_parties.keys()) + ['무효표', '총합']

        df = df[columns_order]
        df.to_excel(election_result_path, index=False)

if __name__ == "__main__":
    main()