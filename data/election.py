import pandas as pd
import numpy as np
import random
import province as pro

# 정당 설정
main_parties = {
    '혁신당': (20, 35),
    '중앙당': (25, 40),
    '통합당': (15, 30),
    '녹색당': (5, 15),
    '자유개혁당': (10, 20),
    '사회민주당': (5, 10),
    '노동당': (5, 15),
    '국민당': (10, 25)
}

# 지역당 설정
regional_parties = {
    '그미즈리 민주당': '그미즈리',
    '하파차 인민당': '하파차',
    '도마니 연합': '도마니'
}

# 행정구역 리스트 생성
province = pro.province

# 진보, 보수 성향 설정
progressive_factor = 1.2
conservative_factor = 0.8

# 추가적인 factor 설정
urban_factor = 1.1
rural_factor = 0.9

# 데이터프레임 생성
data = []
for state, cities in province.items():
    for city in cities:
        row = {'주': state + ' 주', '행정구역': city}
        
        # 기본 정당 득표율 할당
        total = 0
        for party, range_tuple in main_parties.items():
            vote = round(random.uniform(range_tuple[0], range_tuple[1]), 3)
            row[party] = vote
            total += vote
            
        # 지역당이 있는 경우 추가
        if state in regional_parties.values():
            party_name = [k for k, v in regional_parties.items() if v == state][0]
            vote = round(random.uniform(10, 25), 3)
            row[party_name] = vote
            total += vote
            
        # 성향에 따른 득표율 조정
        if state in ['그라나데', '도마니', '미네바', '미치바', '세그레차']:
            row['혁신당'] *= progressive_factor
            row['통합당'] *= conservative_factor
        elif state in ['그미즈리', '림덴시', '메세기', '바니카-메고차', '베고차']:
            row['혁신당'] *= conservative_factor
            row['통합당'] *= progressive_factor
        
        # 도시/농촌 factor 적용
        if city in ["그라나다", "미톤노", "메고기", "파미즈", "크라나", "아리나", "메고이오", "바니아", "모베이", "하롱골", "메초오비카", "모호보드", "노베라니나", "아젠타", "메네트리포어", "파시벤토"]:
            row['혁신당'] *= urban_factor
            row['통합당'] *= rural_factor
        else:
            row['혁신당'] *= rural_factor
            row['통합당'] *= urban_factor

        # 총합 계산 (무효표 제외)
        total_valid = sum([v for k, v in row.items() if k not in ['주', '행정구역', '무효표', '총합']])

        # 총합이 98% 이상이면 95%로 조정
        while total_valid > 98.0:
            for k, v in row.items():
                if k not in ['주', '행정구역', '무효표', '총합']: 
                    row[k] *= 0.95
                    total_valid = sum([v for k, v in row.items() if k not in ['주', '행정구역', '무효표', '총합']])

        # 무효표 처리
        row['무효표'] = round(100.0 - total_valid, 3)
        
        # 총합 추가
        row['총합'] = round(total_valid + row['무효표'], 3)
        
        data.append(row)

# DataFrame 생성 및 저장
df = pd.DataFrame(data)

# 열 순서 재정렬
columns_order = ['주', '행정구역'] + list(main_parties.keys()) + list(regional_parties.keys()) + ['무효표', '총합']
df = df[columns_order]

df.to_excel('data/election_result.xlsx', index=False)

print("선거 결과 데이터가 생성되었습니다.")
