# Description: 정당과 정치 이념을 정의합니다.

# 기본 이념 스펙트럼
ideological_spectrum = ['Far-left', 'Left', 'Center-left', 'Centrist', 'Center-right', 'Right','Far-right']

# 정치 이념 스펙트럼
main_alignments = [
    # 주요 정치 이념
    'Liberalism',  # 자유주의
    'Conservatism',  # 보수주의
    'Republicanism',  # 공화주의
    'Socialism',  # 사회주의
    'Communism',  # 공산주의
    'Anarchism',  # 무정부주의
    'Fascism',  # 파시즘
    'Social Democracy',  # 사회민주주의
    'Green Politics',  # 녹색정치
    'Libertarianism',  # 자유지상주의
    
    # 경제/사회 체제
    'Capitalist',  # 자본주의
    'Socialist',  # 사회주의
    'Mixed Economy',  # 혼합 경제
    'Welfare State',  # 복지 국가
    'Command Economy',  # 계획 경제
    'Market Economy',  # 시장 경제
    'State Capitalism',  # 국가 자본주의
    'Cooperative Economy',  # 협동 경제
    'Sharing Economy',  # 공유 경제
    'Circular Economy',  # 순환 경제
    'Progressive',  # 진보주의
    'Neo-liberalism',  # 신자유주의
    
    # 거버넌스/정치 방식
    'Nationalism',  # 민족주의
    'Populism',  # 대중주의
    'Technocratic',  # 기술관료주의
    'Anti-corruption',  # 반부패
    'Regionalist',  # 지역주의
    'Authoritarianism',  # 권위주의
    'Totalitarianism',  # 전체주의
    'Decentralization',  # 분권화
    'Direct Democracy',  # 직접 민주주의
    'Federalism',  # 연방주의
    
    # 주요 가치/이슈
    'Environmentalism',  # 환경주의
    'Social Justice',  # 사회 정의
    'Labor-rights',  # 노동권
    'Individual-rights',  # 개인의 권리
    'Religious',  # 종교적
    'Secularism',  # 세속주의
    'Feminism',  # 여성주의
    'Gender Equality',  # 성평등
    'LGBT Rights',  # 성소수자 권리
    'Privacy Rights',  # 개인정보 보호
    'Civil Liberties',  # 시민 자유
    'Anti-racism',  # 반인종차별
    'Mental Health Advocacy',  # 정신 건강 옹호
    'Digital Rights',  # 디지털 권리
    'Animal Rights',  # 동물 권리
    'Indigenous Rights',  # 원주민 권리
    'Disability Rights',  # 장애인 권리
    'Youth Politics',  # 청년 정치
    'Elderly Rights',  # 노인 권리
    
    # 경제 정책
    'Free-market',  # 자유시장
    'Protectionist',  # 보호무역주의
    'Innovation',  # 혁신
    'Universal Basic Income',  # 기본소득
    'Cooperative Economics',  # 협동 경제
    'Keynesianism',  # 케인스주의
    'Monetarism',  # 통화주의
    
    # 특수 관심사
    'Pacifism',  # 평화주의
    'Militarism',  # 군국주의
    'Traditionalism',  # 전통주의
    'Modernism',  # 현대주의
    'Anti-globalization',  # 반세계화
    'Globalism',  # 세계주의
    'Sustainability',  # 지속가능성
    'Climate Justice',  # 기후 정의
    'Public Health',  # 공공 보건
    'Social Entrepreneurship',  # 사회적 기업가 정신
    'Interfaith Dialogue',  # 종교간 대화
    'Civic Engagement',  # 시민 참여
    'Urban Development',  # 도시 개발
    'Rural Development',  # 농촌 개발
    
    # 현대적 성향
    'Transhumanism',  # 트랜스휴머니즘
    'Post-scarcity Economics',  # 포스트 희소성 경제학
    'Space Exploration Advocacy',  # 우주 탐사 옹호
    'Artificial Intelligence Ethics',  # 인공지능 윤리
    'Blockchain Governance',  # 블록체인 거버넌스
    'Techno-progressivism',  # 기술진보주의
    'Posthumanism',  # 포스트휴머니즘
]

# 초대형 정당
super_major_parties = {
    '사회민주당': ['Center-left', 'Left', 'Social Democracy', 'Progressive', 'Social Justice', 'Welfare State', 'Civil Liberties'],
    '자유민주연합': ['Center-right', 'Right', 'Conservatism', 'Republicanism', 'Market Economy', 'Nationalism'],
    '중앙당': ['Centrist', 'Social Democracy', 'Progressive', 'Republicanism', 'Mixed Economy', 'Civil Liberties'],
}

# 주요 대형 정당
major_parties = {
    '개혁당': ['Liberalism', 'Progressive', 'Innovation', 'Technocratic', 'Social Justice', 'Digital Rights'],
    '국가를 위한 보수당': ['Nationalism', 'Far-right', 'Conservatism', 'Traditionalism', 'Protectionist', 'Authoritarianism'],
    '노동자당': ['Left', 'Far-left', 'Labor-rights', 'Social Justice', 'Progressive', 'Welfare State', 'Socialism'],
    '좌파연합': ['Left', 'Socialism', 'Progressive', 'Labor-rights', 'Social Justice', 'Environmentalism', 'Anti-corruption'],
    '통합 트라야비야': ['Right', 'Nationalism', 'Conservatism', 'Traditionalism', 'Protectionist'],
}

for party, ideologies in major_parties.items():
    for ideology in ideologies:
        # if ideology not in ae.main_alignments and ideology not in ae.ideological_spectrum:
        #     raise ValueError(f"주요 대형 정당 '{party}'의 정치 이념 '{ideology}'이 alignments_events.py에 없습니다.")
        pass

# 중형 규모 정당
medium_parties = {
    '기본소득당': ['Progressive', 'Social Justice', 'Welfare State', 'Universal Basic Income', 'Labor-rights'],
    '녹색당': ['Environmentalism', 'Progressive', 'Social Justice', 'Left', 'Sustainability', 'Animal Rights', 'Climate Justice'],
    '시민이 모였다!': ['Centrist', 'Anti-corruption', 'Progressive', 'Social Justice', 'Direct Democracy', 'Civic Engagement'],
    '연방공화당': ['Republicanism', 'Conservatism', 'Right', 'Nationalism', 'Protectionist', 'Authoritarianism'],
    '자유혁신당': ['Center-left', 'Progressive', 'Innovation', 'Technocratic', 'Social Justice', 'Digital Rights'],
    '진보를 외치다': ['Left', 'Progressive', 'Social Justice', 'Environmentalism', 'Anti-corruption', 'Globalism'],
    '청년당': ['Progressive', 'Innovation', 'Social Justice', 'Center-left', 'Civic Engagement', 'Youth Politics'],
    '특이점이 온다': ['Technocratic', 'Innovation', 'Progressive', 'Artificial Intelligence Ethics', 'Transhumanism', 'Techno-progressivism'],
}

for party, ideologies in medium_parties.items():
    for ideology in ideologies:
        # if ideology not in ae.main_alignments and ideology not in ae.ideological_spectrum:
        #     raise ValueError(f"중형 규모 정당 '{party}'의 정치 이념 '{ideology}'이 alignments_events.py에 없습니다.")
        pass

# 소수 정당
minor_parties = {
    'LGBT 평등당': ['LGBT Rights', 'Social Justice', 'Progressive', 'Civil Liberties', 'Feminism'],
    '공산당': ['Socialism', 'Far-left', 'Labor-rights', 'Social Justice', 'Progressive', 'Communism'],
    '공정무역당': ['Progressive', 'Social Justice', 'Environmentalism', 'Anti-corruption', 'Globalism'],
    '국가신성당': ['Religious', 'Right', 'Traditionalism', 'Nationalism', 'Authoritarianism'],
    '국민자유전선': ['Far-right', 'Facism', 'Nationalism', 'Conservatism', 'Traditionalism', 'Authoritarianism'],
    '국민행동당': ['Populism', 'Right', 'Nationalism', 'Anti-corruption', 'Conservatism'],
    '균형잡힌 미래': ['Centrist', 'Center-right', 'Progressive', 'Social Justice', 'Mixed Economy'],
    '노인당': ['Conservatism', 'Traditionalism', 'Right', 'Protectionist', 'Rural Development', 'Elderly Rights'],
    '농민당': ['Rural Development', 'Right', 'Protectionist', 'Conservatism', 'Nationalism'],
    '단결하는 신앙당': ['Religious', 'Traditionalism', 'Nationalism', 'Far-right', 'Conservatism', 'Authoritarianism'],
    '디지털 권리당': ['Digital Rights', 'Privacy Rights', 'Technocratic', 'Progressive', 'Civil Liberties'],
    '자연보호당': ['Environmentalism', 'Progressive', 'Social Justice', 'Left', 'Sustainability'],
    '미래당': ['Technocratic', 'Innovation', 'Progressive', 'Environmentalism', 'Globalism'],
    '민주시민모임': ['Center-left', 'Progressive', 'Social Justice', 'Environmentalism', 'Direct Democracy', 'Civic Engagement'],
    '보호하라!': ['Far-right', 'Nationalism', 'Conservatism', 'Traditionalism', 'Authoritarianism'],
    '복지추구당': ['Welfare State', 'Social Justice', 'Progressive', 'Labor-rights', 'Universal Basic Income'],
    '새희망당': ['Center-right', 'Conservatism', 'Traditionalism', 'Capitalist', 'Social Justice', 'Republicanism'],
    '생명당': ['Environmentalism', 'Progressive', 'Social Justice', 'Centrist', 'Civil Liberties'],
    '전사회당': ['Far-left', 'Socialism', 'Progressive', 'Labor-rights', 'Anti-globalization'],
    '정의': ['Social Justice', 'Left', 'Progressive', 'Environmentalism', 'Anti-corruption'],
    '통일당': ['Pacifism', 'Centrist', 'Nationalism', 'Progressive', 'Social Justice'],
    '평화': ['Pacifism', 'Environmentalism', 'Social Justice', 'Progressive', 'Civic Engagement'],
    '우리는 안정을 추구한다': ['Conservatism', 'Traditionalism', 'Right', 'Protectionist', 'Nationalism'],
    '우리는 페미니스트': ['Feminism', 'Left', 'Far-left', 'Feminism', 'Social Justice', 'Gender Equality', 'Progressive'],
    '인권정의당': ['Individual-rights', 'Social Justice', 'Progressive', 'Centrist', 'Feminism'],
}

for party, ideologies in minor_parties.items():
    for ideology in ideologies:
        # if ideology not in ae.main_alignments and ideology not in ae.ideological_spectrum:
        #     raise ValueError(f"소수 정당 '{party}'의 정치 이념 '{ideology}'이 alignments_events.py에 없습니다.")
        pass

# 지역 정당
regional_parties = {
    '그미즈리 국민당': {'region': '그미즈리', 'ideology': ['Conservatism', 'Traditionalism', 'Right', 'Protectionist', 'Regionalist']},
    '그미즈리 노동당': {'region': '그미즈리', 'ideology': ['Left', 'Far-left', 'Socialism', 'Progressive', 'Labor-rights', 'Regionalist']},
    '그미즈리 녹색당': {'region': '그미즈리', 'ideology': ['Environmentalism', 'Progressive', 'Social Justice', 'Left', 'Sustainability', 'Regionalist']},
    '그미즈리 민주당': {'region': '그미즈리', 'ideology': ['Centrist', 'Center-left', 'Progressive', 'Social Justice', 'Regionalist']},
    '그미즈리 보수당': {'region': '그미즈리', 'ideology': ['Far-right', 'Nationalism', 'Conservatism', 'Traditionalism', 'Protectionist', 'Regionalist']},
    '그미즈리 사회당': {'region': '그미즈리', 'ideology': ['Socialism', 'Left', 'Progressive', 'Labor-rights', 'Regionalist']},
    '그미즈리 자유당': {'region': '그미즈리', 'ideology': ['Liberalism', 'Center-right', 'Progressive', 'Market Economy', 'Regionalist']},
    '그미즈리 통합당': {'region': '그미즈리', 'ideology': ['Centrist', 'Center-right', 'Progressive', 'Social Justice', 'Regionalist']},
    '그미즈리 혁신당': {'region': '그미즈리', 'ideology': ['Progressive', 'Innovation', 'Technocratic', 'Social Justice', 'Regionalist']},
    '림덴시를 위하여': {'region': '림덴시', 'ideology': ['Rural Development', 'Conservatism', 'Traditionalism', 'Protectionist', 'Regionalist']},
    '세오어 보호당': {'region': '그라나데, 포어', 'ideology': ['Far-right', 'Nationalism', 'Conservatism', 'Traditionalism', 'Protectionist', 'Regionalist']},
    '테트라 인민당': {'region': '테트라', 'ideology': ['Far-left', 'Socialism', 'Progressive', 'Labor-rights', 'Anti-globalization', 'Regionalist']},
    '하파차의 후예': {'region': '하파차', 'ideology': ['Conservatism', 'Traditionalism', 'Right', 'Protectionist', 'Regionalist']},
    '하파차 민주연합': {'region': '하파차', 'ideology': ['Center-left', 'Left', 'Progressive', 'Social Justice', 'Environmentalism', 'Regionalist']},
}

for party, data in regional_parties.items():
    for ideology in data['ideology']:
        # if ideology not in ae.main_alignments and ideology not in ae.ideological_spectrum:
        #     raise ValueError(f"지역 정당 '{party}'의 정치 이념 '{ideology}'이 alignments_events.py에 없습니다.")
        pass