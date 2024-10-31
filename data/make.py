import os
import pandas as pd
import sys

province_info_file = 'data/mashup/province_info.txt'
election_file = 'data/xlsx/election_result.xlsx'
output_file = 'data/xlsx/province_info_all.xlsx'

def calculate_density(data):
    return data['population'] / data['area']

def rank_province_data(province_data, key, rank_key):
    province_data.sort(key=lambda x: x[key], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data[rank_key] = rank

def calculate_rankings(province_data):
    for data in province_data:
        data['density'] = calculate_density(data)

    rank_province_data(province_data, 'area', 'area_rank')
    rank_province_data(province_data, 'population', 'population_rank')
    rank_province_data(province_data, 'density', 'density_rank')

    province_data.sort(key=lambda x: x['original_index'])
    return province_data

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

def update_province_info(input_file, election_file, output_file):
    print(f"지역 정보를 읽고 선거 데이터를 추가합니다: {input_file}, {election_file}")
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
            print(f"{data['province']} 지역의 선거 데이터를 찾을 수 없습니다.")
            continue

        province_election_data = province_election_data.iloc[0]
        for column in province_election_data.index:
            if column not in ['주', '행정구역', '세부행정구역', '면적', '인구', '인구밀도']:
                data[column] = province_election_data[column]

        progress = processed_rows / total_rows
        bar = '█' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
        sys.stdout.write(f"\r진행 상황: [{bar}] {processed_rows}/{total_rows}")
        sys.stdout.flush()

    sys.stdout.write("\r" + " " * (bar_length + 21) + "\r")
    sys.stdout.write(f"지역 정보 업데이트 완료! {output_file}에 저장합니다.\n")
    sys.stdout.flush()

    province_data = calculate_rankings(province_data)
    pd.DataFrame(province_data).to_excel(output_file, index=False)

def main():
    if not os.path.exists(province_info_file):
        raise FileNotFoundError(f"{province_info_file} 파일을 찾을 수 없습니다.")
    if not os.path.exists(election_file):
        raise FileNotFoundError(f"{election_file} 파일을 찾을 수 없습니다.")
    
    update_province_info(province_info_file, election_file, output_file)

if __name__ == "__main__":
    main()