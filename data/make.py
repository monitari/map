import os
import pandas as pd
import sys

# 파일 경로 설정
province_info_file = 'data/mashup/province_info.txt'
election_file = 'data/xlsx/election_result.xlsx'
output_file = 'data/xlsx/province_info_all.xlsx'

# 인구 밀도 계산 함수
def calculate_density(data):
    return data['population'] / data['area']

# 주어진 키를 기준으로 데이터 정렬 후 순위 부여 함수
def rank_province_data(province_data, key, rank_key):
    province_data.sort(key=lambda x: x[key], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data[rank_key] = rank

# 지역 데이터에 대한 순위 계산 함수
def calculate_rankings(province_data):
    for data in province_data:
        data['density'] = calculate_density(data)

    rank_province_data(province_data, 'area', 'area_rank')
    rank_province_data(province_data, 'population', 'population_rank')
    rank_province_data(province_data, 'density', 'density_rank')

    province_data.sort(key=lambda x: x['original_index'])
    return province_data

# 지역 데이터 파일 읽기 함수
def read_province_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return [
            {
                'subprovince': parts[0],
                'province': parts[1].strip(),
                'province_state': parts[2].strip(),
                'area': int(parts[3]),
                'population': int(parts[4]),
                'original_index': index
            }
            for index, line in enumerate(lines)
            for parts in [line.strip().split(',')]
        ]

# 지역 정보 업데이트 함수
def update_province_info(input_file, election_file, output_file):
    sys.stdout.write(f"지역 정보를 읽고 선거 데이터📊를 추가하는 중이에요: {input_file}, {election_file} - 데이터 요리사가 열심히 일하고 있어요. 🍳\n")
    sys.stdout.flush()
    province_data = read_province_data(input_file)
    election_data = pd.read_excel(election_file).fillna(0)

    total_rows = len(province_data)
    bar_length = 40

    for processed_rows, data in enumerate(province_data, start=1):
        province_election_data = election_data[
            (election_data['세부행정구역'] == data['subprovince']) &
            (election_data['행정구역'] == data['province']) &
            (election_data['주'] == data['province_state'])
        ]

        if province_election_data.empty:
            raise ValueError(f"{data['province']} 지역의 선거 데이터📊를 찾을 수 없어요! 아무래도 외계인이 납치해 간 것 같아요! 👽")

        province_election_data = province_election_data.iloc[0]
        for column in province_election_data.index:
            if column not in ['주', '행정구역', '세부행정구역', '면적', '인구', '인구밀도']:
                data[column] = province_election_data[column]
        if processed_rows % 10 == 0 or processed_rows == total_rows:
            progress = processed_rows / total_rows
            bar = '█' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
            sys.stdout.write(f"\r데이터 요리중: [{bar}] {processed_rows}/{total_rows} - 냄새가 끝내줘요. 😋")
            sys.stdout.flush()
            
    sys.stdout.write("\r" + " " * (bar_length + 100) + "\r")
    sys.stdout.write(f"데이터 업데이트 완료! {output_file}에 저장했어요. 요리가 완성되었어요. 맛있게 드세요! 🍽️\n")
    sys.stdout.flush()

    province_data = calculate_rankings(province_data)
    pd.DataFrame(province_data).to_excel(output_file, index=False)

# 메인 함수
def main():
    if not os.path.exists(province_info_file):
        raise FileNotFoundError(f"{province_info_file} 파일이 어디 갔죠? 찾을 수 없어요! 🕵️‍♂️")
    if not os.path.exists(election_file):
        raise FileNotFoundError(f"{election_file} 파일이 도망갔나요? 여기에 없어요! 🏃‍♂️💨")
    update_province_info(province_info_file, election_file, output_file)

if __name__ == "__main__":
    main()