import cv2
import numpy as np
import re
import pandas as pd
import json
import os
import sys

import data.make as make
import data.election as elect
import data.mashup.province_color as pcolor

# 주별 색상 정보
province_colors = {key: [int(value[i:i+2], 16) for i in (5, 3, 1)] for key, value in pcolor.province_colors.items()}

def hex_to_bgr(hex_color):
    return [int(hex_color[i:i+2], 16) for i in (5, 3, 1)]

def add_data(row):
    parties = {col: (None if pd.isna(row[col]) else row[col]) for col in row.index if col not in [
        "province_state", "area", "population", "density", "area_rank", "population_rank", "density_rank", 
        "무효표", "총합", "province", "subprovince", "original_index", "사건", "도시지수", "경제지수"
    ]}
    
    state = re.sub(r' 주$', '', row['province_state']).strip()
    return {
        "subprovince": row['subprovince'],
        "province": row['province'],
        "state": state,
        "area": row['area'],
        "population": row['population'],
        "density": row['density'],
        "rank-area": row['area_rank'],
        "rank-population": row['population_rank'],
        "rank-density": row['density_rank'],
        "city-index": row['도시지수'],
        "economy-index": row['경제지수'],
        "events": row['사건'],
        "parties": json.dumps(parties),
        "invalid-votes": row['무효표'],
        "total-votes": row['총합'],
    }

def main():
    # 파일 경로 정의
    image_path = r'map\TRAYAVIYA_o3.png'
    style_path = r'data\style.css'
    template_path = r'data\template.txt'
    province_info_path = r'data\xlsx\province_info_all.xlsx'
    output_path = "vector_map.html"

    # 이미지 로드 및 확인
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"이미지가 없는데요? {image_path} 🖼️🚫 어딨니, 내 사랑스러운 이미지야? 😢")
    else:
        sys.stdout.write(f"이미지를 불러왔어요: {image_path} 🖼️👍 이미지를 분석하고 있어요! 🔍\n")
        sys.stdout.flush()

    # province_info_all.xlsx 파일에서 데이터 읽기
    df = pd.read_excel(province_info_path)

    # 진행 상황 표시 바 초기화
    total_rows = len(df)
    bar_length = 40

    # province_data 생성
    province_data = {}
    for i, (index, row) in enumerate(df.iterrows()):
        province_data[row['subprovince']] = add_data(row)
        
        # 진행 상황 표시 바 업데이트
        if (i + 1) % 10 == 0 or (i + 1) == total_rows:
            progress = (i + 1) / total_rows
            bar = '█' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
            sys.stdout.write(f"\r데이터를 처리중: [{bar}] {i + 1}/{total_rows} - 거북이가 빨리 달려가고 있어요! 🐢💨")
            sys.stdout.flush()

    sys.stdout.write("\r" + " " * (bar_length + 70) + "\r")
    sys.stdout.write("이제 SVG 요소를 생성하고 있어요! 🧙✨")
    sys.stdout.flush()
    
    # SVG 요소 초기화
    svg_elements = []

    # 색상 정의 및 범위 설정
    for key, bgr_color in province_colors.items():
        tolerance = 0
        lower_bound = [max(c - tolerance, 0) for c in bgr_color]
        upper_bound = [min(c + tolerance, 255) for c in bgr_color]
        inside_mask = cv2.inRange(image, np.array(lower_bound, dtype=np.uint8), np.array(upper_bound, dtype=np.uint8))

        # 컨투어 추출 및 단순화
        contours_inside, _ = cv2.findContours(inside_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours_inside:
            raise ValueError(f"컨투어가 어디 갔죠? {key} 주가 숨바꼭질 중인가 봐요! 🙈")
        
        # 주별 SVG 요소 생성
        province_svg_elements = []
        subdivision_id = 0
        for province_name, info in province_data.items():
            if subdivision_id < len(contours_inside):
                if info["province"] == key:
                    contour = contours_inside[subdivision_id]
                    path_data = "M " + " ".join(f"{x},{y}" for x, y in contour[:, 0, :])
                    province_svg_elements.append(f'<path d="{path_data}" stroke="none" '
                                                f'class="subdivision" id="subdivision{subdivision_id}" '
                                                f'data-subname="{info["subprovince"]}" '
                                                f'data-name="{info["province"]}" data-area="{info["area"]}" '
                                                f'data-population="{info["population"]}" '
                                                f'data-state="{info["state"]}" data-density="{info["density"]}" '
                                                f'data-rank-area="{info["rank-area"]}" data-rank-population="{info["rank-population"]}" '
                                                f'data-rank-density="{info["rank-density"]}" data-all-province="{len(province_data)}" '
                                                f'data-events="{info["events"]}" data-invalid-votes="{info["invalid-votes"]}" '
                                                f'data-total-votes="{info["total-votes"]}" '
                                                f'data-parties=\'{info["parties"]}\'/>')
                    subdivision_id += 1

        province_svg_content = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {image.shape[1]} {image.shape[0]}" id="{key}">
            {''.join(province_svg_elements)}
        </svg>
        """
        svg_elements.append(province_svg_content)

    sys.stdout.write("\r" + " " * 100 + "\r")
    sys.stdout.write("이제 HTML 파일을 생성하고 있어요! 🧙✨\n")

    # 전체 SVG 컨텐츠 생성
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
        print(f"{output_path} 맵이 생성되었어요. 이제 지도를 탐험할 시간입니다! 🗺️🔍")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    elect.main()
    make.main()
    main()