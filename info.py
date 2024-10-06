# data/province_info.txt에서 데이터를 읽는다.
# 각 행은 이름, 면적, 인구로 구성되어 있다.
# 인구의 총 합을 계산하고, 각 행정구역의 인구 비율을 계산하고 출력

# 숫자를 출력할 때 억, 만 단위로 표시하는 함수 (예: 1234567 -> 123만 4567)
def format_number(number):
    if number >= 100000000:
        return f"{number // 100000000}억 {number % 100000000 // 10000}만 {number % 10000}"
    elif number >= 10000:
        return f"{number // 10000}만 {number % 10000}"
    else:
        return str(number)

# 주 할당 튜플
province = {
    "그라나데": ["안파키", "아파그라나다", "페카그라나다", "그라나다", "보피노", "메르노"],
    "그미즈리": ["오크모", "미톤노", "페아그", "그미즈리", "아센시", "메깅고", "호오토", "키에오"],
    "도마니": ["오브니", "바스바드", "케릴티", "메고기", "에링고", "커피", "즈조이", "가안", "브고홀", "모옹홀", "메옹"],
    "림덴시": ["파미즈", "스피가", "아르고", "모리고", "펜보드", "메바치", "모호카", "린토카", "낙소", "보빈", "라토카", "세오고", "시안", "보어"],
    "메세기": ["크라나", "나다이", "옹피오", "메세기", "포크란", "크레이", "안파기"],
    "미네바": ["아리나", "만토", "메가", "코에가", "민마나", "모에바", "아바나", "솔바", "미바나", "에디아다", "리에다"],
    "미치바": ["메고이오", "우프레나", "미츠비", "알고", "산시아고", "나릴로", "유프란", "미치바"],
    "바니카-메고차": ["바니아", "미에고", "메고리", "민고", "이벤토", "마링고"],
    "베고차": ["모베이", "트롱페이", "바티아", "이베이", "페린", "리안토", "오고소", "민마", "테안타", "모반토", "레링가"],
    "세그레차": ["하롱골", "미골", "메링골", "세골", "키골", "리에골", "페아골", "베아골"],
    "아이리카": ["메초오비카", "아브레", "피에트라", "아이리카", "메르네", "츠비키", "하르바트"],
    "안텐시": ["모호보드", "아핀고", "비에노", "시세디", "메즈노", "아신가", "키르가"],
    "카리아-로": ["노베라니나", "아르모텐타", "피고모싱고메고차바데다", "미베이토메고차피덴타", "안트로아싱가"],
    "테트라": ["아젠타", "아칸타", "파르티엔타", "유칸타", "테트리다모스", "테트리비제모스", "테타"],
    "포어": ["메네트리포어", "안트리포어", "라간", "안파", "테사", "아르테", "세가", "오르도기"],
    "하파차": ["파시벤토", "오고이모", "미느리오", "산세오", "아스타나", "티레니오", "비엥고", "아린키고", "하싱고", "모잉고", "하르고"]
}

# 데이터를 읽어서 처리
province_data = {}
total_population = 0

# 데이터 읽기
with open("data/province_info.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        # 각 줄을 읽어서 이름, 면적, 인구로 나누기
        name, area, population = line.strip().split(",")
        province_data[name] = {"area": area.strip(), "population": population.strip()}
        total_population += int(population)

    # 인구 비율 계산
    # cnt = 0
    max_name_length = max(len(province_name) for province_name in province_data.keys())
    
    for province_name, info in province_data.items():
        population = int(info["population"])
        population_ratio = population / total_population
        tabs = "\t" * ((max_name_length - len(province_name)) // 4 + 1)
        # print(f"{province_name}:{tabs}{population_ratio:.2%}", end="\t" if cnt % 4 != 3 else "\n")
    #     cnt += 1
    
    # if cnt % 4 != 0:
    #     print()  # 마지막 줄 개행

for i in range(128): # 구분선 출력
    print("-", end="")
print()

# 각 주에 대해 반복하며 데이터 출력
for pro in province:
    print(f"{pro} 주의 행정구역 수: {len(province[pro])}개")
    print(f"{pro} 주의 면적: " + format_number(sum([int(province_data[p]['area']) for p in province[pro]])) + "A")
    print(f"{pro} 주의 인구: " + format_number(sum([int(province_data[p]['population']) for p in province[pro]])) + "명")
    print(f"{pro} 주의 인구 밀도: {sum([int(province_data[p]['population']) for p in province[pro]]) / sum([int(province_data[p]['area']) for p in province[pro]]):.2f}명/A")
    print(f"{pro} 주의 전체 대비 인구 비율: {sum([int(province_data[p]['population']) for p in province[pro]]) / total_population:.2%}")
    print()

for i in range(128): # 구분선 출력
    print("-", end="")
print()

# 총 인구 출력
print("국가명 : 트라야비아")
print(f"주 수: {len(province)}개")
print(f"행정구역 수: {len(province_data)}개")
print(f"총 인구: {format_number(total_population)}명")
print(f"총 인구 밀도: {total_population / sum([int(province_data[p]['area']) for p in province_data]):.2f}명/A\n")

# 주 정보 (인구가 가장 많은 주, 가장 적은 주, 인구 밀도가 가장 높은 주, 낮은 주)
max_population = max(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]))
max_population_num = sum([int(province_data[p]['population']) for p in province[max_population]])
min_population = min(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]))
min_population_num = sum([int(province_data[p]['population']) for p in province[min_population]])
max_density = max(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]) / sum([int(province_data[p]['area']) for p in province[x]]))
max_density_ratio = sum([int(province_data[p]['population']) for p in province[max_density]]) / sum([int(province_data[p]['area']) for p in province[max_density]])
min_density = min(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]) / sum([int(province_data[p]['area']) for p in province[x]]))
min_density_ratio = sum([int(province_data[p]['population']) for p in province[min_density]]) / sum([int(province_data[p]['area']) for p in province[min_density]])

print(f"인구가 가장 많은 주: {max_population} ({format_number(max_population_num)}명)")
print(f"인구가 가장 적은 주: {min_population} ({format_number(min_population_num)}명)")
print(f"인구 밀도가 가장 높은 주: {max_density} ({max_density_ratio:.2f}명/A)")
print(f"인구 밀도가 가장 낮은 주: {min_density} ({min_density_ratio:.2f}명/A)\n")

# 행정구역 정보 (인구가 가장 많은 행정구역, 가장 적은 행정구역, 인구 밀도가 가장 높은 행정구역, 낮은 행정구역)
max_population = max(province_data, key=lambda x: int(province_data[x]["population"]))
max_population_num = int(province_data[max_population]["population"])
min_population = min(province_data, key=lambda x: int(province_data[x]["population"]))
min_population_num = int(province_data[min_population]["population"])
max_density = max(province_data, key=lambda x: int(province_data[x]["population"]) / int(province_data[x]["area"]))
max_density_ratio = int(province_data[max_density]["population"]) / int(province_data[max_density]["area"])
min_density = min(province_data, key=lambda x: int(province_data[x]["population"]) / int(province_data[x]["area"]))
min_density_ratio = int(province_data[min_density]["population"]) / int(province_data[min_density]["area"])

print(f"인구가 가장 많은 행정구역: {max_population} ({format_number(max_population_num)}명)")
print(f"인구가 가장 적은 행정구역: {min_population} ({format_number(min_population_num)}명)")
print(f"인구 밀도가 가장 높은 행정구역: {max_density} ({max_density_ratio:.2f}명/A)")
print(f"인구 밀도가 가장 낮은 행정구역: {min_density} ({min_density_ratio:.2f}명/A)\n")

for i in range(128): # 구분선 출력
    print("-", end="")

# 주별 인구 순위
population_rank = sorted(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]), reverse=True)
print("\n주별 인구 순위")
for rank, pro in enumerate(population_rank):
    print(f"{rank + 1}위: {pro} ({format_number(sum([int(province_data[p]['population']) for p in province[pro]]))}명)")

print()

# 주별 인구 밀도 순위
density_rank = sorted(province, key=lambda x: sum([int(province_data[p]['population']) for p in province[x]]) / sum([int(province_data[p]['area']) for p in province[x]]), reverse=True)
print("주별 인구 밀도 순위")
for rank, pro in enumerate(density_rank):
    print(f"{rank + 1}위: {pro} ({sum([int(province_data[p]['population']) for p in province[pro]]) / sum([int(province_data[p]['area']) for p in province[pro]]):>6.2f}명/A)")

print()

# 행정구역별 인구 순위
population_rank = sorted(province_data, key=lambda x: int(province_data[x]["population"]), reverse=True)
print("행정구역별 인구 순위 상위 16개")
for rank, pro in enumerate(population_rank):
    for p in province:
        if pro in province[p]:
            print(f"{rank + 1}위: {pro} ({format_number(int(province_data[pro]['population']))}명) (주 : {p})")
    if rank == 15:
        break

print()

# 행정구역별 인구 밀도 순위
density_rank = sorted(province_data, key=lambda x: int(province_data[x]["population"]) / int(province_data[x]["area"]), reverse=True)
print("행정구역별 인구 밀도 순위 상위 16개")
for rank, pro in enumerate(density_rank):
    for p in province:
        if pro in province[p]:
            print(f"{rank + 1}위: {pro} ({int(province_data[pro]['population']) / int(province_data[pro]['area']):>6.2f}명/A) (주 : {p})")
    if rank == 15:
        break

print()