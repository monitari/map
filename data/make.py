import os

def load_relations(relation_file):
    relations = {}
    with open(relation_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            state, provinces = line.strip().split(' = ')
            for province in provinces.split(', '):
                relations[province] = state
    return relations

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

def update_province_info(relations, input_file, output_file):
    province_data = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            parts = line.strip().split(',')
            province_data.append({
                'province': parts[0],
                'state': parts[1],
                'area': int(parts[2]),
                'population': int(parts[3]),
                'original_index': index
            })

    province_data = calculate_rankings(province_data)

    with open(output_file, 'w', encoding='utf-8') as file:
        for data in province_data:
            province = data['province']
            if province in relations:
                province_with_state = f"{province}, {relations[province]}"
            else:
                province_with_state = province
            file.write(f"{province_with_state}, {data['area']}, {data['population']}, {data['density']}, {data['area_rank']}, {data['population_rank']}, {data['density_rank']}\n")

def main():
    base_dir = os.path.dirname(__file__)  # 현재 파일의 디렉토리
    # relation 파일 경로 ../dummy/relation.txt
    relation_file = os.path.join(base_dir, '..', 'dummy', 'relation.txt')
    province_info_file = os.path.join(base_dir, 'province_info.txt')
    output_file = os.path.join(base_dir, 'province_info_all.txt')

    if not os.path.exists(relation_file):
        raise FileNotFoundError(f"File not found: {relation_file}")
    if not os.path.exists(province_info_file):
        raise FileNotFoundError(f"File not found: {province_info_file}")

    relations = load_relations(relation_file)
    update_province_info(relations, province_info_file, output_file)

if __name__ == "__main__":
    main()