import sys
import os

# 현재 파일의 디렉토리 경로를 가져와서 부모 디렉토리를 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
import numpy as np
import random
import warnings
import data.mashup.party as party
import data.mashup.party_preference as pp
import data.mashup.alignments_events as alevent

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 사건
events = alevent.events # 사건 목록
event_impact = alevent.event_impact # 사건 영향력

# 정당 추가
super_major_parties = party.super_major_parties
major_parties = party.major_parties
medium_parties = party.medium_parties
minor_parties = party.minor_parties
regional_parties = party.regional_parties

# 정당 선호도 및 이념 스펙트럼 추가
ideological_spectrum = pp.ideological_spectrum
party_preference_map = pp.party_preference

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
    #행정구역에 따른 개인 선호 정당 지수 계산
    district = province_info_row['행정구역']

    # 각 주와 행정구역에 대한 정치적 성향을 기반으로 선호 지수 설정
    preference_index = {'Conservative': 1.0, 'Progressive': 1.0}

    # 행정구역에 대한 선호 지수 반영
    if district in party_preference_map:
        for party, impact in party_preference_map[district].items():
            preference_index[party] *= impact

    # 최종 확률 분포 계산
    distribution = pp.define_party_preference(preference_index['Conservative'], preference_index['Progressive'])

    return distribution  # 각 정당에 대한 상대적 선호 지수

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
    returning = (L / (1 + np.exp(exponent))) / 10 + 1
    
    # factor: 정규 분포로 0.95 ~ 1.25 사이의 값을 랜덤하게 생성
    factor = np.random.normal(1.1, 0.05)
    factor = max(0.95, min(factor, 1.25))
    
    if returning > 1.0: returning *= factor  # 1.0을 초과하는 경우 추가 조정
    else: returning /= factor  # 1.0을 초과하지 않는 경우 추가 조정
    return returning

def adjust_alignment_with_indexes(vote_shares, province_info_row, event):
    city_index = province_info_row['도시지수'] # 주별 도시 및 경제 지수를 기반으로 정당별 투표율 조정
    economic_index = province_info_row['경제지수'] # 경제 지수를 추가
    party_preference_index = calculate_party_preference_index(province_info_row)  # 개인 선호 정당 지수를 추가

    # 정치 성향에 따라 지수 영향을 반영 (로지스틱 함수로 조정)
    # L: 최대 투표율, k: 기울기, x0: 기준값, city_index: 도시지수, economic_index: 경제지수
    # 범진보 / 범보수 정당의 투표율 조정
    
    # 정렬에 따른 투표율 조정
    alignment_impact = {
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

    # 정당별 투표율에 정렬 영향 반영
    for party in vote_shares.keys():
        all_parties = {**super_major_parties, **major_parties, **medium_parties, **minor_parties, **regional_parties}
        if party in all_parties:
            if party in regional_parties: vote_shares[party] *= 15.0 # 지역 정당의 투표율 15배 증가
            for alignment in all_parties[party]:
                if alignment in alignment_impact:
                    alignment_score = alignment_impact.get(alignment, 1.0)
                    vote_shares[party] *= alignment_score
                if alignment in party_preference_index:
                    preference_score = party_preference_index.get(alignment, 1.0)
                    vote_shares[party] *= preference_score
        else: raise ValueError(f"정당 {party}에 대한 정치 성향이 없습니다.")
    return vote_shares

def calculate_vote_shares(event, state, row):
    # 기본 투표율 계산
    regional_party_found = False  # 지역 정당 존재 여부 확인
    relevant_regional_parties = {}  # 해당 주의 지역 정당만 포함

    for party, party_state in regional_parties.items(): # 해당 주의 지역 정당 찾기
        if party_state['region'].find(',') != -1:  # 여러 지역에 걸쳐 있는 경우
            regions = party_state['region'].split(', ')
            formatted_state = state.strip().lower()
            if any((region.strip() + " 주").lower() == formatted_state for region in regions):
                regional_party_found = True
                relevant_regional_parties[party] = party_state
        else: # 한 지역에 속하는 경우
            formatted_party_state = (party_state['region'] + " 주").strip().lower()
            formatted_state = state.strip().lower()
            if formatted_party_state == formatted_state:
                regional_party_found = True
                relevant_regional_parties[party] = party_state

    if regional_party_found: # 지역 정당이 있는 경우
        smajor_votes = [random.uniform(70.0, 250.0) for _ in range(len(super_major_parties))]
        major_votes = [random.uniform(20.0, 40.0) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(2.0, 15.0) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, 10.0) for _ in range(len(minor_parties))]
        if state == "그미즈리 주": # 그미즈리 주의 경우
            reg_votes = [random.uniform(800.0, 2000.0) if party == "그미즈리 국민당" or party == "그미즈리 민주당"
                else (random.uniform(0.0, 400.0) if party == "그미즈리 녹색당" or party == "그미즈리 혁신당" or party == "그미즈리 통합당"
                else random.uniform(0.0, 80.0)) for party in relevant_regional_parties]
        elif state == "테트라 주": # 테트라 주의 경우
            reg_votes = [random.uniform(300.0, 600.0) for _ in range(len(relevant_regional_parties))]
        else: reg_votes = [random.uniform(5.0, 25.0) for _ in range(len(relevant_regional_parties))]
            
    else: # 지역 정당이 없는 경우
        smajor_votes = [random.uniform(75.0, 150.0) for _ in range(len(super_major_parties))]
        major_votes = [random.uniform(20.0, 40.0) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(2.0, 15.0) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, 10.0) for _ in range(len(minor_parties))]
        reg_votes = [random.uniform(0.0, 0.0) for _ in range(len(relevant_regional_parties))]

    # 정당별 투표율 할당
    vote_shares = {}

    # 대형 정당, 중형 정당, 소수 정당, 지역 정당 순으로 반복
    all_parties = [
        (super_major_parties, smajor_votes),
        (major_parties, major_votes),
        (medium_parties, medium_votes),
        (minor_parties, minor_votes),
        (relevant_regional_parties, reg_votes)
    ]
    
    # 정당별 투표율 계산 (event_impact 반영)
    for parties, votes in all_parties:
        for i, party in enumerate(parties.keys()):
            total_impact = 1.0
            for ideology in parties[party]: 
                e = event_impact.get(event, {}).get(ideology, 1.0) # 사건 영향력
                total_impact *= e
            if total_impact > 1.5: total_impact = 1.5
            elif total_impact < 0.75: total_impact = 0.75
            adjusted_vote = votes[i] * total_impact
            vote_shares[party] = round(adjusted_vote, 3)  # 투표율 반영

    # 투표율 계산 후 정당 성향 및 도시/경제 지수 반영
    vote_shares = adjust_alignment_with_indexes(vote_shares, row, event)

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
    # 먼저 도시지수와 경제지수를 계산하여 추가
    province_info = calculate_indexes(province_info) # 도시지수, 경제지수, 주지수, 행정구역지수 추가
    data = [] # 결과 데이터를 저장할 리스트
    global_event = get_priority_event() # 전국적 사건 선택
    global_sub_event = random.choices(events[global_event]['subtypes']) # 전국적 사건의 세부 사건 선택
    print(f"전국적 사건: {global_event} - {global_sub_event[0]}")

    total_rows = len(province_info)
    processed_rows = 0 # 처리된 행 수 (진행 상황 출력에 사용)
    bar_length = 50  # 진행 상황 바의 길이

    for state, cities in province_info.groupby('주'):
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
            
            # 진행 상황 출력
            processed_rows += 1
            progress = processed_rows / total_rows
            block = int(bar_length * progress)
            bar = '█' * block + '-' * (bar_length - block)
            sys.stdout.write(f"\r진행 상황: [{bar}] {processed_rows}/{total_rows}")
            sys.stdout.flush()

    # 완료 메시지 출력
    sys.stdout.write("\r" + " " * (bar_length + 21) + "\r")  # 진행 바 지우기
    sys.stdout.write("선거 결과 데이터 생성 완료!\n")
    sys.stdout.flush()
    return data

def read_province_info(file_path):
    # 파일에서 주별 정보 읽기
    try:
        province_info = pd.read_csv(file_path, sep=',', names=['행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        print(f"{file_path} 파일을 성공적으로 불러왔습니다.")
        return province_info
    except Exception as e: raise ValueError(f"파일을 읽는 중 오류 발생: {e}")

def main():
    province_info_path = 'data/mashup/province_info.txt'
    election_result_path = 'data/xlsx/election_result.xlsx'

    province_info = read_province_info(province_info_path)
    province_info['주'] = province_info['주'].str.strip() # 주 이름 공백 제거

    if province_info is not None:
        data = process_data_with_indexes(province_info)
        df = pd.DataFrame(data)

        # 열 순서 정리
        columns_order = ['주', '행정구역', '면적', '인구', '인구밀도', '도시지수', '경제지수', '사건'] + \
                        list(super_major_parties.keys()) + list(major_parties.keys()) + list(medium_parties.keys()) + \
                       list(minor_parties.keys()) + list(regional_parties.keys()) + ['무효표', '총합']
        
        df = df[columns_order]
        df.to_excel(election_result_path, index=False)
        print(f"선거 결과를 {election_result_path}에 저장했습니다.")

if __name__ == "__main__":
    main()