import os
import pandas as pd
from data.mashup.province import province  # province 딕셔너리 가져오기

def calculate_density(data): # 인구 밀도 계산 함수
    return data['population'] / data['area']

def rank_province_data(province_data, key, rank_key): # 지역 데이터를 정렬하는 함수
    province_data.sort(key=lambda x: x[key], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data[rank_key] = rank

def calculate_rankings(province_data): # 지역 데이터의 순위 계산 함수
    for data in province_data:
        data['density'] = calculate_density(data)

    rank_province_data(province_data, 'area', 'area_rank') # 지역 데이터를 정렬
    rank_province_data(province_data, 'population', 'population_rank') # 지역 데이터를 정렬
    rank_province_data(province_data, 'density', 'density_rank') # 지역 데이터를 정렬

    province_data.sort(key=lambda x: x['original_index']) # 원래 순서로 정렬
    return province_data

def read_province_data(input_file): # 지역 데이터를 읽는 함수
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines() # 파일을 줄 단위로 읽기
        return [
            {
                'province': parts[0],
                'province_state': parts[1].strip(),
                'area': int(parts[2]),
                'population': int(parts[3]),
                'original_index': index
            }
            for index, line in enumerate(lines)
            for parts in [line.strip().split(',')]
        ]

def update_province_info(relations, input_file, election_file, output_file): # 지역 정보를 업데이트하는 함수
    print(f"지역 정보를 읽고 선거 데이터를 추가합니다: {input_file}, {election_file}")
    province_data = read_province_data(input_file) # 지역 데이터를 읽기

    election_data = pd.read_excel(election_file) # 선거 데이터를 읽기
    election_data['주'] = election_data['행정구역'].apply(lambda x: x.split()[0]) # 주 정보 추가
    election_data = election_data.drop(columns=['면적', '인구', '인구밀도'], errors='ignore') # 불필요한 열 삭제
    election_data = election_data.set_index('행정구역').T.to_dict() # 행정구역을 인덱스로 설정하고 딕셔너리로 변환

    for data in province_data:
        province_name = data['province'] # 지역 이름 가져오기
        if province_name in election_data: # 선거 데이터가 있는 경우
            election_info = {k: v for k, v in election_data[province_name].items() if k != '주'} # 선거 정보 가져오기 ('주' 제외)
            data.update(election_info) # 선거 정보 업데이트

    province_data = calculate_rankings(province_data) # 지역 데이터의 순위 계산
    df = pd.DataFrame(province_data) # 데이터프레임 생성

    election_columns = list(election_data[next(iter(election_data))].keys()) # 선거 데이터의 열 이름 가져오기
    election_columns.remove('주') # '주' 열 제외
    other_columns = [col for col in df.columns if col not in election_columns] # 선거 데이터가 아닌 열 이름 가져오기
    df = df[other_columns + election_columns] # 열 순서 변경

    df.to_excel(output_file, index=False) # 엑셀 파일로 저장
    print(f"지역 정보를 업데이트하고 {output_file}에 저장했습니다.")

def main():
    province_info_file = 'data/mashup/province_info.txt' # 지역 정보 파일
    election_file = 'data/xlsx/election_result.xlsx' # 선거 결과 파일
    output_file = 'data/xlsx/province_info_all.xlsx' # 업데이트된 지역 정보 파일

    if not os.path.exists(province_info_file): # 파일이 없는 경우 예외 발생
        raise FileNotFoundError(f"{province_info_file} 파일을 찾을 수 없습니다.")
    if not os.path.exists(election_file): # 파일이 없는 경우 예외 발생
        raise FileNotFoundError(f"{election_file} 파일을 찾을 수 없습니다.")
    
    update_province_info(province, province_info_file, election_file, output_file) # 지역 정보 업데이트

if __name__ == "__main__":
    main()