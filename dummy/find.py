from PIL import Image
from collections import defaultdict
import sys
sys.path.append('f:/Code/MAP')
import data.mashup.province_color as pcolor

# 16진수 색상을 RGB 색상으로 변환하는 함수
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)

# 행정구역 색상 데이터를 RGB로 변환
province_colors = {k: hex_to_rgb(v) for k, v in pcolor.province_colors.items()}
# RGB 색상으로부터 행정구역 이름을 찾기 위한 역 매핑
reverse_province_colors = {v: k for k, v in province_colors.items()}

# 제외할 색상 목록
else_color = {(211, 242, 255, 255), (0, 0, 0, 255), (255, 255, 255, 255), (237, 237, 237, 255), (195, 195, 195, 255), (152, 152, 152, 255)}

# 중복되는 색상을 찾는 함수
def find_duplicate_colors(province_colors):
    reverse_dict = defaultdict(list)
    for key, value in province_colors.items():
        reverse_dict[value].append(key)
    
    duplicates = {k: v for k, v in reverse_dict.items() if len(v) > 1}
    return duplicates

# 이미지에서 모든 색상의 개수를 세는 함수
def count_all_colors(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    color_count = defaultdict(int)
    for x in range(width):
        for y in range(height):
            color = pixels[x, y]
            if isinstance(color, int): color = (color, color, color, 255)  # 단일 채널 값을 RGB 값으로 변환
            color_count[color] += 1
    return color_count

def main():
    mode = input("모드를 입력하세요 (1: province_colors 사용, 2: 사용하지 않음): ")
    image_path = "map/TRAYAVIYA_o0.png"
    color_count = count_all_colors(image_path)
    
    if mode == '1': # province_colors 사용
        province_cnt = len(province_colors)
        else_cnt = 0
        for color, count in color_count.items(): # 색상별로 개수 출력
            if color in province_colors.values(): # 행정구역 색상인 경우
                province_name = reverse_province_colors[color]
                print(province_name, color, count)
            else: else_cnt += 1 # 행정구역 색상이 아닌 경우
        print(f"총 {province_cnt}개의 행정구역과 {int(len(color_count)) - else_cnt}개 (+기타 {else_cnt}개)의 색상이 사용되었습니다.")
        
        duplicates = find_duplicate_colors(province_colors)
        if duplicates: # 중복되는 색이 있는 경우
            print("중복되는 색이 있습니다.")
            for color, provinces in duplicates.items(): print(f"색 {color}는 {provinces}에서 중복 사용되고 있습니다.")
        else: print("중복되는 색이 없습니다.")

    elif mode == '2': # province_colors 사용하지 않음
        for color, count in color_count.items():
            if color not in else_color:
                hex_color = '#{:02X}{:02X}{:02X}'.format(color[0], color[1], color[2])
                print(hex_color, count) # else_color 제외
        print(f"총 {len(color_count)}개의 색상이 사용되었습니다.")
    else: print("잘못된 모드입니다.")

if __name__ == "__main__":
    main()