import cv2
import numpy as np
import re
import pandas as pd
import json
import os

import data.make as make
import data.election as elect

def add_data(row):
    parties = {col: (None if pd.isna(row[col]) else row[col]) for col in row.index if col not in [
        "province_state", "area", "population", "density", "area_rank", "population_rank", "density_rank", 
        "무효표", "총합", "province", "original_index", "사건", "도시지수", "경제지수"
    ]}
    
    return {
        "state": re.sub(r' 주$', '', row['province_state']).strip(),
        "area": row['area'],
        "population": row['population'],
        "density": row['density'],
        "rank-area": row['area_rank'],
        "rank-population": row['population_rank'],
        "rank-density": row['density_rank'],
        "city-index": row['도시지수'],
        "economy-index": row['경제지수'],
        "events": row['사건'],
        "parties": json.dumps(parties), # 파티 정보를 JSON 형식으로 변환
        "invalid-votes": row['무효표'],
        "total-votes": row['총합']
    }

def main():
    # 파일 경로 정의
    image_path = r'map\TRAYAVIYA_o.png'
    style_path = r'data\style.css'
    template_path = r'data\template.txt'
    province_info_path = r'data\xlsx\province_info_all.xlsx'
    output_path = "vector_map.html"

    # 이미지 로드 및 확인
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"이미지를 불러오지 못했습니다: {image_path}")

    # 색상 정의 및 범위 설정
    inside_color = np.array([152, 152, 152])
    tolerance = 2
    lower_bound = np.clip(inside_color - tolerance, 0, 255)
    upper_bound = np.clip(inside_color + tolerance, 0, 255)
    inside_mask = cv2.inRange(image, lower_bound, upper_bound)

    # 컨투어 추출 및 단순화
    contours_inside, _ = cv2.findContours(inside_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    epsilon = 0.001 * cv2.arcLength(contours_inside[0], True)
    contours_inside = [cv2.approxPolyDP(contour, epsilon, True) for contour in contours_inside]

    # province_info_all.xlsx 파일에서 데이터 읽기
    df = pd.read_excel(province_info_path)
    province_data = {row['province']: add_data(row) for _, row in df.iterrows()}
    province_cnt = len(province_data)

    # 컨투어와 데이터의 길이 확인
    if len(contours_inside) < province_cnt:
        raise ValueError("컨투어의 수가 행정구역의 수보다 적습니다. 이미지와 데이터가 일치하는지 확인하세요.")

    # SVG 생성 준비
    svg_elements = []
    subdivision_id = 0

    # inside 영역을 SVG로 변환 및 데이터 추가
    for province_name, info in province_data.items():
        if subdivision_id < len(contours_inside):
            contour = contours_inside[subdivision_id]
            path_data = "M " + " ".join(f"{x},{y}" for x, y in contour[:, 0, :])
            svg_elements.append(f'<path d="{path_data} Z" fill="gray" stroke="none" '
                                f'class="subdivision" id="subdivision{subdivision_id}" '
                                f'data-name="{province_name}" data-area="{info["area"]}" '
                                f'data-population="{info["population"]}" '
                                f'data-state="{info["state"]}" data-density="{info["density"]}" '
                                f'data-rank-area="{info["rank-area"]}" data-rank-population="{info["rank-population"]}" '
                                f'data-rank-density="{info["rank-density"]}" data-all-province="{province_cnt}" data-events="{info["events"]}" '
                                f'data-invalid-votes="{info["invalid-votes"]}" data-total-votes="{info["total-votes"]}" '
                                f'data-parties=\'{info["parties"]}\'/>')

            subdivision_id += 1

    # SVG 컨텐츠 생성
    svg_content = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {image.shape[1]} {image.shape[0]}" id="map">
        {''.join(svg_elements)}
        <text id="info" x="10" y="30" font-size="20" fill="black"></text>
    </svg>
    """

    # CSS 파일 불러오기
    with open(style_path, "r", encoding='utf-8') as css_file:
        css_content = css_file.read()

    # HTML 템플릿 불러오기
    with open(template_path, "r", encoding='utf-8') as template_file:
        html_content = template_file.read()

    # SVG 및 CSS 컨텐츠 추가
    html_content = html_content.replace("<!-- SVG_CONTENT -->", svg_content)
    html_content = html_content.replace("/* CSS_CONTENT */", css_content)

    # 파일 저장
    with open(output_path, "w", encoding='utf-8') as output_file:
        output_file.write(html_content)
        print(f"{output_path} | SVG 맵이 생성되었습니다. Live Server를 사용하여 확인하세요.")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    elect.main()
    make.main()
    main()