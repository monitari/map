import sys
import os
import pandas as pd
import numpy as np
import random
import warnings

province_info_path = 'data/mashup/province_info.txt' # 행정구역 정보 파일 경로
election_result_path = 'data/xlsx/election_result.xlsx' # 선거 결과 파일 경로

# 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'mashup'))

import data.mashup.party as party
import data.mashup.province_preference as pp
import data.mashup.alignments_events as alevent

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 사건
events = alevent.events
event_impact = alevent.event_impact

# 정당 추가
super_major_parties = party.super_major_parties
major_parties = party.major_parties
medium_parties = party.medium_parties
minor_parties = party.minor_parties
regional_parties = party.regional_parties

# 정당 선호도 및 이념 스펙트럼 추가
ideological_spectrum = pp.ideological_spectrum
province_preference = pp.province_preference

def get_priority_event(): # 우선순위 사건 선택
    events_list = list(events.keys())
    pr = [events[event]['frequency'] for event in events_list] # 사건 빈도수에 따라 가중치 부여
    return random.choices(events_list, weights=pr)[0] # 가중치에 따라 사건 선택

def calculate_population_density(province_info): # 인구밀도 계산
    return province_info['인구'] / province_info['면적'] 

def calculate_party_preference_index(province_info_row): # 정당 선호도 계산
    district = province_info_row['행정구역'] # 행정구역
    preference_index = {'Conservative': 1.0, 'Progressive': 1.0} # 보수주의, 진보주의 선호도 지수 초기화

    if district in province_preference: # 행정구역이 선호도 데이터에 있는 경우
        for party, impact in province_preference[district].items(): # 선호도 데이터에 따라 선호도 지수 조정
            preference_index[party] *= impact # 선호도 지수 조정

    return pp.define_party_preference(preference_index['Conservative'], preference_index['Progressive']) # 선호도 지수 반환

def calculate_indexes(province_info): # 지수 계산
    province_info['도시지수'] = province_info['인구밀도'] / province_info['인구밀도'].max() * 100 # 도시지수 계산
    economic_indexes = province_info.groupby('주').apply( # 경제지수 계산
        lambda x: (x['인구'].sum() / x['면적'].sum()) / (province_info['인구'].sum() / province_info['면적'].sum()) * 100
    ).reset_index(name='경제지수')
    
    province_info = province_info.merge(economic_indexes, on='주') # 경제지수 데이터 병합
    province_info['주지수'] = province_info.groupby('주')['인구밀도'].transform('mean') # 주별 인구밀도 평균 계산
    province_info['행정구역지수'] = province_info.groupby('행정구역')['인구밀도'].transform('mean') # 행정구역별 인구밀도 평균 계산
    
    return province_info

def logistic_function(x, L=2, k=0.05, x0=50): # 로지스틱 함수
    exponent = -k * (x - x0) # 지수 계산
    exponent = min(max(exponent, -100), 100) # 지수 범위 제한
    returning = (L / (1 + np.exp(exponent))) / 10 + 1 # 로지스틱 함수 계산
    
    factor = np.random.normal(1.1, 0.1) # 요인 (평균: 1.1, 표준편차: 0.1)
    factor = min(max(factor, 0.9), 1.3) # 요인 범위 제한 (0.9 ~ 1.3)
    if returning > 1.0: returning *= factor # 로지스틱 함수 값 조정
    else: returning /= factor # 로지스틱 함수 값 조정
    return returning

def adjust_alignment_with_indexes(vote_shares, province_info_row): # 정렬 및 지수 조정
    city_index = province_info_row['도시지수'] # 도시지수
    economic_index = province_info_row['경제지수'] # 경제지수
    party_preference_index = calculate_party_preference_index(province_info_row) # 정당 선호도 지수

    alignment_impact = { # 정렬 영향도
        'Far-left': logistic_function(city_index, L=3.7, k=0.10, x0=43) * logistic_function(economic_index, L=2.0, k=-0.06, x0=55),
        'Left': logistic_function(city_index, L=3.5, k=0.09, x0=47) * logistic_function(economic_index, L=2.5, k=0.05, x0=52),
        'Center-left': logistic_function(city_index, L=3.0, k=0.08, x0=50) * logistic_function(economic_index, L=3.0, k=0.08, x0=50),
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

    all_parties = {**super_major_parties, **major_parties, **medium_parties, **minor_parties, **regional_parties} # 모든 정당
    for party in vote_shares.keys():
        if party in all_parties:
            if party in regional_parties: vote_shares[party] *= 5.0 # 지역 정당의 경우 투표율 증가
            for alignment in all_parties[party]: # 정렬에 따라 정당 선호도 지수 조정
                if alignment in alignment_impact: # 정렬이 정렬 영향도에 있는 경우
                    vote_shares[party] *= alignment_impact[alignment] # 정당 선호도 지수 조정
                if alignment in party_preference_index: # 정렬이 정당 선호도 지수에 있는 경우
                    vote_shares[party] *= party_preference_index[alignment] # 정당 선호도 지수 조정
        else: raise ValueError(f"정당 {party}에 대한 정치 성향이 없습니다.") # 정당 선호도가 없는 경우
    return vote_shares

def calculate_vote_shares(event, state, row): # 투표율 계산
    regional_party_found = False # 지역 정당 발견 여부
    relevant_regional_parties = {} # 관련 지역 정당

    formatted_state = state.strip().lower() # 주 이름 포맷팅
    for party, party_state in regional_parties.items():
        regions = party_state['region'].split(', ')
        if formatted_state in regions: # 주 이름이 지역 정당에 있는 경우
            regional_party_found = True
            relevant_regional_parties[party] = party_state

    state_vote_ranges = { # 주별 투표율 범위
        "그미즈리": {
            "그미즈리 국민당": (800.0, 2000.0), "그미즈리 민주당": (800.0, 2000.0),
            "그미즈리 녹색당": (0.0, 400.0), "그미즈리 혁신당": (0.0, 400.0), "그미즈리 통합당": (0.0, 400.0), "default": (0.0, 80.0)
        },
        "테트라": (1000.0, 1500.0), "그라나데": (200.0, 500.0), "포어": (100.0, 250.0), "도마니": (100.0, 250.0),
        "안텐시": (25.0, 100.0), "림덴시": (25.0, 100.0), "하파차": (25.0, 100.0), "default": (5.0, 50.0)
    }

    if regional_party_found:
        smajor_votes = np.random.uniform(20.0, 200.0, len(super_major_parties))
        major_votes = np.random.uniform(20.0, 100.0, len(major_parties))
        medium_votes = np.random.uniform(2.0, 25.0, len(medium_parties))
        minor_votes = np.random.uniform(0, 10.0, len(minor_parties))
        if state in state_vote_ranges: # 주 이름이 주별 투표율 범위에 있는 경우
            if state == "그미즈리": # 그미즈리의 경우
                reg_votes = np.array([
                    np.random.uniform(*state_vote_ranges[state].get(party, state_vote_ranges[state]["그미즈리 국민당"]) if party in state_vote_ranges[state] else state_vote_ranges[state]["default"])
                    for party in relevant_regional_parties
                ])
            else: reg_votes = np.random.uniform(*state_vote_ranges[state], len(relevant_regional_parties)) # 그 외의 경우
        else: reg_votes = np.random.uniform(*state_vote_ranges["default"], len(relevant_regional_parties)) # 기본 범위로 설정
    else: # 지역 정당이 없는 경우
        smajor_votes = np.random.uniform(20.0, 200.0, len(super_major_parties))
        major_votes = np.random.uniform(20.0, 100.0, len(major_parties))
        medium_votes = np.random.uniform(2.0, 25.0, len(medium_parties))
        minor_votes = np.random.uniform(0, 10.0, len(minor_parties))
        reg_votes = np.zeros(len(relevant_regional_parties))

    vote_shares = {} # 투표율
    all_parties = [ # 모든 정당
        (super_major_parties, smajor_votes),
        (major_parties, major_votes),
        (medium_parties, medium_votes),
        (minor_parties, minor_votes),
        (relevant_regional_parties, reg_votes)
    ]

    for parties, votes in all_parties:
        for i, party in enumerate(parties.keys()):
            total_impact = np.prod([event_impact.get(event, {}).get(ideology, 1.0) for ideology in parties[party]])
            total_impact = np.clip(total_impact, 0.5, 2.0) # 영향도 범위 제한
            vote_shares[party] = round(votes[i] * total_impact, 3)
    
    vote_shares = adjust_alignment_with_indexes(vote_shares, row) # 정렬 및 지수 조정

    total_votes = sum(vote_shares.values())
    target_votes = np.random.uniform(95, 98) # 목표 투표율
    adjustment_factor = target_votes / total_votes # 조정 계수

    for party in vote_shares.keys(): vote_shares[party] *= adjustment_factor # 투표율 조정

    return vote_shares

def process_data_with_indexes(province_info): # 지수를 이용한 데이터 처리
    province_info = calculate_indexes(province_info) # 지수 계산
    data = [] # 데이터 (투표 결과)
    global_event = get_priority_event() # 우선순위 사건 선택
    global_sub_event = random.choice(events[global_event]['subtypes']) # 사건 하위 유형 선택
    print(f"전국적 사건: {global_event} - {global_sub_event}") # 전국적 사건 출력

    total_rows = len(province_info) # 총 행 수
    processed_rows = 0 # 처리된 행 수
    bar_length = 50 # 진행 막대 길이

    for state, cities in province_info.groupby('주'):
        for _, row in cities.iterrows():
            result_row = { # 결과 행
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

            vote_shares = calculate_vote_shares(global_event, state, row) # 투표율 계산
            result_row.update(vote_shares) # 결과 행 업데이트
            result_row['무효표'] = 100 - sum(vote_shares.values()) # 무효표 계산 (100 - 투표율 총합)
            result_row['총합'] = round(sum(vote_shares.values()) + result_row['무효표'], 3) # 총합 계산 (투표율 총합 + 무효표)
            
            data.append(result_row) # 결과 행 추가
            
            processed_rows += 1 # 처리된 행 수 증가
            progress = processed_rows / total_rows
            block = int(bar_length * progress)
            bar = '█' * block + '-' * (bar_length - block) # 진행 막대
            sys.stdout.write(f"\r진행 상황: [{bar}] {processed_rows}/{total_rows}") # 진행 상황 출력
            sys.stdout.flush()

    sys.stdout.write("\r" + " " * (bar_length + 21) + "\r") # 진행 상황 초기화
    sys.stdout.write(f"선거 결과 데이터 생성 완료! {election_result_path}에 저장합니다.\n") # 선거 결과 데이터 생성 완료 메시지 출력
    sys.stdout.flush()
    return data

def read_province_info(file_path): # 행정구역 정보 읽기
    try: # 파일 읽기 시도
        province_info = pd.read_csv(file_path, sep=',', names=['세부행정구역', '행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        return province_info
    except Exception as e: raise ValueError(f"파일을 읽는 중 오류 발생: {e}") # 파일 불러오기 실패 시 오류 메시지 출력

def main(): # 메인 함수
    province_info = read_province_info(province_info_path) # 행정구역 정보 읽기
    province_info['주'] = province_info['주'].str.strip() # 주 정보 공백 제거

    if province_info is not None: # 행정구역 정보가 있는 경우
        data = process_data_with_indexes(province_info) # 지수를 이용한 데이터 처리
        df = pd.DataFrame(data) # 데이터프레임 생성

        columns_order = ['주', '행정구역', '세부행정구역', '면적', '인구', '인구밀도', '도시지수', '경제지수', '사건'] + \
                        list(super_major_parties.keys()) + list(major_parties.keys()) + list(medium_parties.keys()) + \
                       list(minor_parties.keys()) + list(regional_parties.keys()) + ['무효표', '총합']

        df = df[columns_order]
        df.to_excel(election_result_path, index=False) # 선거 결과 저장

if __name__ == "__main__":
    main()