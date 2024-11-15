# data/province_info.txt에서 데이터를 읽는다.
# 각 행은 세부행정구역, 행정구역, 주, 면적, 인구로 구성되어 있다.
# 인구의 총 합을 계산하고, 각 행정구역의 인구 비율을 계산하고 출력

# 숫자를 출력할 때 억, 만 단위로 표시하는 함수 (예: 1234567 -> 123만 4567)
def format_number(number):
    if number >= 100000000:
        return f"{number // 100000000}억 {number % 100000000 // 10000}만 {number % 10000}"
    elif number >= 10000:
        return f"{number // 10000}만 {number % 10000}"
    else:
        return str(number)

def read_data(file_path):
    province_data = {}
    total_population = 0

    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            sub_region, name, state, area, population = line.strip().split(", ")
            province_data[sub_region] = {
                "name": name.strip(),
                "state": state.strip(),
                "area": int(area.strip()),
                "population": int(population.strip())
            }
            total_population += int(population)
    
    return province_data, total_population

def write_output(province_data, total_population, output_path):
    with open(output_path, "w", encoding='utf-8') as output_file:
        # 주
        provinces = {}
        for info in province_data.values():
            state = info["state"]
            if state not in provinces: provinces[state] = {"total_area": 0, "total_population": 0, "regions": []}
            provinces[state]["total_area"] += info["area"]
            provinces[state]["total_population"] += info["population"]
            provinces[state]["regions"].append(info)

        # 총 인구 출력
        output_file.write("국가명 : 트라야비아\n")
        output_file.write(f"주 수: {len(provinces)}개\n")
        output_file.write(f"행정구역 수: {len(province_data)}개\n")
        output_file.write(f"총 인구: {format_number(total_population)}명\n")
        output_file.write(f"총 인구 밀도: {total_population / sum(info['area'] for info in province_data.values()):.2f}명/A\n\n")
        output_file.write("-" * 128 + "\n")

        # 주별 정보 출력
        for state, data in provinces.items():
            output_file.write(f"{state} 주의 행정구역 수: {len(data['regions'])}개\n")
            output_file.write(f"{state} 주의 면적: {format_number(data['total_area'])}A\n")
            output_file.write(f"{state} 주의 인구: {format_number(data['total_population'])}명\n")
            
            if data['total_area'] > 0: output_file.write(f"{state} 주의 인구 밀도: {data['total_population'] / data['total_area']:.2f}명/A\n")
            else: output_file.write(f"{state} 주의 인구 밀도: 계산 불가 (면적이 0)\n")
            output_file.write(f"{state} 주의 전체 대비 인구 비율: {data['total_population'] / total_population:.2%}\n\n")
        output_file.write("-" * 128 + "\n")

        # 주 정보 (인구가 가장 많은 주, 가장 적은 주, 인구 밀도가 가장 높은 주, 낮은 주)
        max_population_state = max(provinces, key=lambda x: provinces[x]['total_population'])
        min_population_state = min(provinces, key=lambda x: provinces[x]['total_population'])
        max_density_state = max(provinces, key=lambda x: provinces[x]['total_population'] / provinces[x]['total_area'])
        min_density_state = min(provinces, key=lambda x: provinces[x]['total_population'] / provinces[x]['total_area'])

        output_file.write(f"인구가 가장 많은 주: {max_population_state} ({format_number(provinces[max_population_state]['total_population'])}명)\n")
        output_file.write(f"인구가 가장 적은 주: {min_population_state} ({format_number(provinces[min_population_state]['total_population'])}명)\n")
        output_file.write(f"인구 밀도가 가장 높은 주: {max_density_state} ({provinces[max_density_state]['total_population'] / provinces[max_density_state]['total_area']:.2f}명/A)\n")
        output_file.write(f"인구 밀도가 가장 낮은 주: {min_density_state} ({provinces[min_density_state]['total_population'] / provinces[min_density_state]['total_area']:.2f}명/A)\n\n")

        # 행정구역 정보 (인구가 가장 많은 행정구역, 가장 적은 행정구역, 인구 밀도가 가장 높은 행정구역, 낮은 행정구역)
        max_population_region = max(province_data, key=lambda x: province_data[x]["population"])
        min_population_region = min(province_data, key=lambda x: province_data[x]["population"])
        max_density_region = max(province_data, key=lambda x: province_data[x]["population"] / province_data[x]["area"])
        min_density_region = min(province_data, key=lambda x: province_data[x]["population"] / province_data[x]["area"])

        output_file.write(f"인구가 가장 많은 행정구역: {max_population_region} ({format_number(province_data[max_population_region]['population'])}명)\n")
        output_file.write(f"인구가 가장 적은 행정구역: {min_population_region} ({format_number(province_data[min_population_region]['population'])}명)\n")
        output_file.write(f"인구 밀도가 가장 높은 행정구역: {max_density_region} ({province_data[max_density_region]['population'] / province_data[max_density_region]['area']:.2f}명/A)\n")
        output_file.write(f"인구 밀도가 가장 낮은 행정구역: {min_density_region} ({province_data[min_density_region]['population'] / province_data[min_density_region]['area']:.2f}명/A)\n\n")
        output_file.write("-" * 128 + "\n")

        # 주별 인구 순위
        population_rank = sorted(provinces, key=lambda x: provinces[x]['total_population'], reverse=True)
        output_file.write("\n주별 인구 순위\n")
        for rank, state in enumerate(population_rank): output_file.write(f"{rank + 1}위: {state} ({format_number(provinces[state]['total_population'])}명)\n")
        output_file.write("\n")

        # 주별 인구 밀도 순위
        density_rank = sorted(provinces, key=lambda x: provinces[x]['total_population'] / provinces[x]['total_area'], reverse=True)
        output_file.write("주별 인구 밀도 순위\n")
        for rank, state in enumerate(density_rank): output_file.write(f"{rank + 1}위: {state} ({provinces[state]['total_population'] / provinces[state]['total_area']:.2f}명/A)\n")
        output_file.write("\n")

        # 행정구역별 인구 순위
        population_rank = sorted(province_data, key=lambda x: province_data[x]["population"], reverse=True)
        output_file.write("행정구역별 인구 순위\n")
        for rank, region in enumerate(population_rank): output_file.write(f"{rank + 1}위: {region} ({format_number(province_data[region]['population'])}명) (주 : {province_data[region]['state']})\n")
        output_file.write("\n")

        # 행정구역별 인구 밀도 순위
        density_rank = sorted(province_data, key=lambda x: province_data[x]["population"] / province_data[x]["area"], reverse=True)
        output_file.write("행정구역별 인구 밀도 순위\n")
        for rank, region in enumerate(density_rank): output_file.write(f"{rank + 1}위: {region} ({province_data[region]['population'] / province_data[region]['area']:.2f}명/A) (주 : {province_data[region]['state']})\n")
        output_file.write("\n")

        # 주별 면적 순위
        area_rank = sorted(provinces, key=lambda x: provinces[x]['total_area'], reverse=True)
        output_file.write("주별 면적 순위\n")
        for rank, state in enumerate(area_rank): output_file.write(f"{rank + 1}위: {state} ({format_number(provinces[state]['total_area'])}A)\n")   
        output_file.write("\n")

        # 행정구역별 면적 순위
        area_rank = sorted(province_data, key=lambda x: province_data[x]["area"], reverse=True)
        output_file.write("행정구역별 면적 순위\n")
        for rank, region in enumerate(area_rank): output_file.write(f"{rank + 1}위: {region} ({format_number(province_data[region]['area'])}A) (주 : {province_data[region]['state']})\n")
        output_file.write("\n")

def main():
    province_data, total_population = read_data("data/mashup/province_info.txt")
    provinces = {}
    for info in province_data.values():
        state = info["state"]
        if state not in provinces: provinces[state] = {"total_area": 0, "total_population": 0}
        provinces[state]["total_area"] += info["area"]
        provinces[state]["total_population"] += info["population"]

    while True:
        print("원하는 작업을 선택하세요.")
        print("0. 데이터 저장")
        print("1. 주별 인구 순위")
        print("2. 주별 인구 밀도 순위")
        print("3. 행정구역별 인구 순위")
        print("4. 행정구역별 인구 밀도 순위")
        print("5. 주별 면적 순위")
        print("6. 행정구역별 면적 순위")
        print("-1. 종료")

        choice = input("번호를 입력하세요: ")

        if choice == "-1": break
        elif choice == "0":
            write_output(province_data, total_population, "dummy/output.txt")
            print("데이터를 저장했습니다.")
        elif choice == "1":
            population_rank = sorted(provinces, key=lambda x: provinces[x]['total_population'], reverse=True)
            print("\n주별 인구 순위")
            for rank, state in enumerate(population_rank): print(f"{rank + 1}위: {state} ({format_number(provinces[state]['total_population'])}명)")
        elif choice == "2":
            density_rank = sorted(provinces, key=lambda x: provinces[x]['total_population'] / provinces[x]['total_area'], reverse=True)
            print("\n주별 인구 밀도 순위")
            for rank, state in enumerate(density_rank): print(f"{rank + 1}위: {state} ({provinces[state]['total_population'] / provinces[state]['total_area']:.2f}명/A)")
        elif choice == "3":
            population_rank = sorted(province_data, key=lambda x: province_data[x]["population"], reverse=True)
            print("\n행정구역별 인구 순위")
            for rank, region in enumerate(population_rank): print(f"{rank + 1}위: {region} ({format_number(province_data[region]['population'])}명) (주 : {province_data[region]['state']})")
        elif choice == "4":
            density_rank = sorted(province_data, key=lambda x: province_data[x]["population"] / province_data[x]["area"], reverse=True)
            print("\n행정구역별 인구 밀도 순위")
            for rank, region in enumerate(density_rank): print(f"{rank + 1}위: {region} ({province_data[region]['population'] / province_data[region]['area']:.2f}명/A) (주 : {province_data[region]['state']})")
        elif choice == "5":
            area_rank = sorted(provinces, key=lambda x: provinces[x]['total_area'], reverse=True)
            print("\n주별 면적 순위")
            for rank, state in enumerate(area_rank): print(f"{rank + 1}위: {state} ({format_number(provinces[state]['total_area'])}A)")
        elif choice == "6":
            area_rank = sorted(province_data, key=lambda x: province_data[x]["area"], reverse=True)
            print("\n행정구역별 면적 순위")
            for rank, region in enumerate(area_rank): print(f"{rank + 1}위: {region} ({format_number(province_data[region]['area'])}A) (주 : {province_data[region]['state']})")
        else: print("잘못된 입력입니다. 다시 시도하세요.")
        print("=" * 128, end="\n\n")

if __name__ == "__main__":
    main()