import os
import pandas as pd
from province import province  # Import the province dictionary

def calculate_rankings(province_data):
    # Calculate population density
    for data in province_data:
        data['density'] = data['population'] / data['area']

    # Sort and rank by area
    province_data.sort(key=lambda x: x['area'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['area_rank'] = rank

    # Sort and rank by population
    province_data.sort(key=lambda x: x['population'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['population_rank'] = rank

    # Sort and rank by population density
    province_data.sort(key=lambda x: x['density'], reverse=True)
    for rank, data in enumerate(province_data, start=1):
        data['density_rank'] = rank

    # Restore original order
    province_data.sort(key=lambda x: x['original_index'])

    return province_data

def update_province_info(relations, input_file, election_file, output_file):
    province_data = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            parts = line.strip().split(',')
            province_data.append({
                'province': parts[0],
                'province_state': parts[1],  # state를 province_state로 변경
                'area': int(parts[2]),
                'population': int(parts[3]),
                'original_index': index
            })

    # Read election data
    election_data = pd.read_excel(election_file)
    
    # '주' 열을 추가하고 인덱스로 설정하지 않음
    election_data['주'] = election_data['행정구역'].apply(lambda x: x.split()[0])
    election_data = election_data.set_index('행정구역').T.to_dict()  # 행정구역을 인덱스로 설정

    # Update province data with election data
    for data in province_data:
        province_name = data['province']
        if province_name in election_data:
            election_info = {k: v for k, v in election_data[province_name].items() if k != '주'}
            data.update(election_info)

    province_data = calculate_rankings(province_data)

    # Convert to DataFrame
    df = pd.DataFrame(province_data)

    # Move election data columns to the end
    election_columns = list(election_data[next(iter(election_data))].keys())
    election_columns.remove('주')  # '주' 열을 제거
    other_columns = [col for col in df.columns if col not in election_columns]
    df = df[other_columns + election_columns]

    # Write to Excel file
    df.to_excel(output_file, index=False)

def main():
    base_dir = os.path.dirname(__file__)  # 현재 파일의 디렉토리
    province_info_file = os.path.join(base_dir, 'province_info.txt')
    election_file = os.path.join(base_dir, 'election_result.xlsx')
    output_file = os.path.join(base_dir, 'province_info_all.xlsx')

    if not os.path.exists(province_info_file):
        raise FileNotFoundError(f"File not found: {province_info_file}")

    if not os.path.exists(election_file):
        raise FileNotFoundError(f"File not found: {election_file}")

    update_province_info(province, province_info_file, election_file, output_file)

if __name__ == "__main__":
    main()
    print("Data processing is complete.")