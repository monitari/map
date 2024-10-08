import cv2
import numpy as np
import re
import pandas as pd

# 이미지 경로
image_path = r'map\TRAYAVIYA_o.png'

# 이미지 로드 및 확인
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"이미지를 불러오지 못했습니다: {image_path}")

# 색상 정의 (BGR 포맷)
inside_color = np.array([152, 152, 152])  # #989898 국가 내 영역

# 색상 범위 정의
color_value = inside_color
tolerance = 2  # 색상 허용 범위
lower_bound = np.clip(color_value - tolerance, 0, 255)
upper_bound = np.clip(color_value + tolerance, 0, 255)
inside_mask = cv2.inRange(image, lower_bound, upper_bound)

# 컨투어 추출
contours_inside, _ = cv2.findContours(inside_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# province_info_all.xlsx 파일에서 데이터 읽기
province_data = {}
province_cnt = 0
df = pd.read_excel(r"data\province_info_all.xlsx")

# 데이터 처리
for _, row in df.iterrows():
    name = row['province']
    state = re.sub(r' 주$', '', row['province_state']) # 주 이름에서 ' 주' 제거
    province_data[name] = {
        "state": state.strip(),
        "area": row['area'],
        "population": row['population'],
        "density": row['density'],
        "rank-area": row['area_rank'],
        "rank-population": row['population_rank'],
        "rank-density": row['density_rank'],
    }
    province_cnt += 1

# SVG 생성 준비
svg_paths = []
subdivision_id = 0
text_elements = []  # 텍스트 요소를 저장할 리스트

# inside 영역을 SVG로 변환 및 데이터 추가
for province_name, info in province_data.items():
    # 컨투어 추출
    contour = contours_inside[subdivision_id % len(contours_inside)]  # 반복 사용
    path_data = "M " + " ".join(f"{x},{y}" for x, y in contour[:, 0, :])
    svg_paths.append(f'<path d="{path_data} Z" fill="gray" stroke="none" '
                     f'class="subdivision" id="subdivision{subdivision_id}" '
                     f'data-name="{province_name}" data-area="{info["area"]}" '
                     f'data-population="{info["population"]}" '
                     f'data-state="{info["state"]}" data-density="{info["density"]}" '
                     f'data-rank-area="{info["rank-area"]}" data-rank-population="{info["rank-population"]}" '
                     f'data-rank-density="{info["rank-density"]}" data-all-province="{province_cnt}"/>')

    # 행정구역 이름 추가
    text_x = contour[:, 0, 0].mean()  # 중심 X 좌표
    text_y = contour[:, 0, 1].mean()  # 중심 Y 좌표
    text_elements.append(f'<text x="{text_x}" y="{text_y}" font-size="20" fill="black" '
                        f'text-anchor="middle" alignment-baseline="middle" '
                        f'style="pointer-events: none;">{province_name}</text>')

    subdivision_id += 1

# SVG 컨텐츠 생성
svg_content = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {image.shape[1]} {image.shape[0]}" id="map">
    {''.join(svg_paths)}
    {''.join(text_elements)}
    <text id="info" x="10" y="30" font-size="20" fill="black"></text>
</svg>
"""
#css 파일 불러오기
css_content = open("data/style.css", "r", encoding='utf-8').read()

# HTML 템플릿 불러오기
html_content = open("dummy/template.txt", "r", encoding='utf-8').read()

# SVG 컨텐츠 추가
html_content = html_content.replace("<!-- SVG_CONTENT -->", svg_content)

# CSS 컨텐츠 추가
html_content = html_content.replace("/* CSS_CONTENT */", css_content)

# 파일 저장
with open("vector_map.html", "w", encoding='utf-8') as file:
    file.write(html_content)

print("SVG 맵이 생성되어 'vector_map.html' 파일로 저장되었습니다.")