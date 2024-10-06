import cv2
import numpy as np

# 이미지 경로
image_path = 'map\TRAYAVIYA_o.png'

# 이미지 로드 및 확인
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"이미지를 불러오지 못했습니다: {image_path}")

# 색상 정의 (BGR 포맷)
inside_color = np.array([152, 152, 152])  # #989898 국가 내 영역

# 색상 범위 정의
color_value = inside_color
tolerance = 2  # 색상 허용 범위
lower_bound = np.array([color_value - tolerance])
upper_bound = np.array([color_value + tolerance])
inside_mask = cv2.inRange(image, lower_bound, upper_bound)

# 컨투어 추출
contours_inside, _ = cv2.findContours(inside_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# province_info.txt 파일에서 데이터 읽기
province_data = {}
with open("data\province_info.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        # 각 줄을 읽어서 이름, 면적, 인구로 나누기
        name, area, population = line.strip().split(",")
        province_data[name] = {"area": area.strip(), "population": population.strip()}

# SVG 생성 준비
svg_paths = []
subdivision_id = 0
text_elements = []  # 텍스트 요소를 저장할 리스트

# 인구에 따른 색상 계산
def get_population_color(population):
    min_pop = 1000  # 최소 인구
    max_pop = 10000000  # 최대 인구 (백만으로 줄임)
    normalized = (int(population) - min_pop) / (max_pop - min_pop)
    red_intensity = int(255 * normalized)  # 빨간색 강도
    return f"rgb({red_intensity}, {255 - red_intensity}, {255 - red_intensity})"

# inside 영역을 SVG로 변환 및 데이터 추가
for province_name, info in province_data.items():
    # 컨투어 추출
    contour = contours_inside[subdivision_id % len(contours_inside)]  # 반복 사용
    path_data = "M " + " ".join(f"{x},{y}" for x, y in contour[:, 0, :])
    color = get_population_color(info["population"])  # 인구에 따른 색상 적용
    svg_paths.append(f'<path d="{path_data} Z" fill="{color}" stroke="none" '
                     f'class="subdivision" id="subdivision{subdivision_id}" '
                     f'data-name="{province_name}" data-area="{info["area"]}" '
                     f'data-population="{info["population"]}" '
                     f'data-province="{province_name}"/>')
    
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


# HTML 파일 생성
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Vector Map</title>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}
        #map-container {{
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        #map {{
            width: 100%;
            height: 100%;
        }}
        .subdivision {{
            fill: #989898;
            transition: fill 0.3s;
        }}
        .subdivision:hover {{
            fill: #f00;
        }}
        #tooltip {{
            position: absolute;
            background-color: white;
            border: 1px solid black;
            padding: 5px;
            z-index: 1000;
            display: none;
        }}
        #toggle-buttons {{
            position: fixed;
            bottom: 10px;
            left: 10px;
            z-index: 1000;
        }}
        #toggle-buttons button {{
            font-size: 16px;
            padding: 10px 20px;
        }}
    </style>
</head>
<body>
    <!-- SVG Content -->
    <div id="map-container">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" id="map">
            {svg_content}
        </svg>

        <!-- Tooltip Element -->
        <div id="tooltip"></div>

        <!-- Toggle Buttons Container -->
        <div id="toggle-buttons">
            <!-- Population Color Toggle Button -->
            <button id="population-toggle">Toggle Population Color</button>
        
            <!-- Population Density Toggle Button -->
            <button id="density-toggle">Toggle Population Density Color</button>
        </div>
    </div>

    <!-- JavaScript to control interaction -->
    <script src="map_interaction.js"></script>
</body>
</html>
"""

# 파일 저장
with open("vector_map.html", "w", encoding='utf-8') as file:
    file.write(html_content)

print("SVG 맵이 생성되어 'vector_map.html' 파일로 저장되었습니다.")