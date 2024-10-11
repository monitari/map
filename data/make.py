import os
import pandas as pd
from data.province import province  # province 딕셔너리 가져오기

def calculate_rankings(province_data):
    # 인구 밀도 계산
    for data in province_data:
        data['density'] = data['population'] / data['area']

    # 면적 기준으로 정렬 및 순위 매기기
    province_data.sort(key=lambda x: x['area'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['area_rank'] = rank

    # 인구 기준으로 정렬 및 순위 매기기
    province_data.sort(key=lambda x: x['population'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['population_rank'] = rank

    # 인구 밀도 기준으로 정렬 및 순위 매기기
    province_data.sort(key=lambda x: x['density'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['density_rank'] = rank

    # 원래 순서로 복원
    province_data.sort(key=lambda x: x['original_index'])

    return province_data

def update_province_info(relations, input_file, election_file, output_file):
    print("파일을 업데이트 중 . . .")
    province_data = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            parts = line.strip().split(',')
            province_data.append({
                'province': parts[0],
                'province_state': parts[1].strip(),  # 주 이름 공백 제거
                'area': int(parts[2]),
                'population': int(parts[3]),
                'original_index': index
            })

    # 선거 데이터 읽기
    election_data = pd.read_excel(election_file)

    # '주' 열을 추가하고 인덱스로 설정하지 않음
    election_data['주'] = election_data['행정구역'].apply(lambda x: x.split()[0])

    # 면적, 인구, 인구밀도 열을 제거
    election_data = election_data.drop(columns=['면적', '인구', '인구밀도'], errors='ignore')

    # 행정구역을 인덱스로 설정하고 딕셔너리로 변환
    election_data = election_data.set_index('행정구역').T.to_dict()

    # 선거 데이터로 province 데이터 업데이트
    for data in province_data:
        province_name = data['province']
        if province_name in election_data:
            election_info = {k: v for k, v in election_data[province_name].items() if k != '주'}
            data.update(election_info)

    province_data = calculate_rankings(province_data)

    # DataFrame으로 변환
    df = pd.DataFrame(province_data)

    # 선거 데이터 열을 끝으로 이동
    election_columns = list(election_data[next(iter(election_data))].keys())
    election_columns.remove('주')  # '주' 열을 제거
    other_columns = [col for col in df.columns if col not in election_columns]
    df = df[other_columns + election_columns]

    # Excel 파일로 쓰기
    df.to_excel(output_file, index=False)

def main():
    base_dir = os.path.dirname(__file__)  # 현재 파일의 디렉토리
    province_info_file = os.path.join(base_dir, 'province_info.txt')
    election_file = os.path.join(base_dir, 'election_result.xlsx')
    output_file = os.path.join(base_dir, 'province_info_all.xlsx')

    if not os.path.exists(province_info_file):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {province_info_file}")

    if not os.path.exists(election_file):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {election_file}")

    update_province_info(province, province_info_file, election_file, output_file)
    print("성공적으로 파일을 저장했습니다.")

if __name__ == "__main__":
    main()