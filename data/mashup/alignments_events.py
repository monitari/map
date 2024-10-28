# Description: 정치 이념과 사건의 영향 관계를 정의한 파일

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

# 사건 목록
events = {
    '자연재해': { 'impact': 0.15, 'frequency': 0.06, 'importance': 8.0, 'subtypes': ['지진', '태풍', '홍수', '가뭄', '화산폭발'] },
    '이민': { 'impact': 0.25, 'frequency': 0.08, 'importance': 7.5, 'subtypes': ['난민', '이주 노동자', '불법 이민'] },
    '반이민': { 'impact': 0.3, 'frequency': 0.08, 'importance': 8.0, 'subtypes': ['이주자 규제', '난민 반대', '국경 통제'] },
    '경제 불황': { 'impact': 0.4, 'frequency': 0.12, 'importance': 9.0, 'subtypes': ['실업률 증가', '물가 상승', '소득 불평등'] },
    '사회 운동': { 'impact': 0.3, 'frequency': 0.10, 'importance': 8.5, 'subtypes': ['시위', '파업', '청년 운동'] },
    '노동 문제': { 'impact': 0.35, 'frequency': 0.07, 'importance': 8.0, 'subtypes': ['최저임금', '근로시간', '노동 환경'] },
    '안보 위협': { 'impact': 0.5, 'frequency': 0.05, 'importance': 9.5, 'subtypes': ['테러', '국제 갈등', '군사 공격'] },
    '빈부격차 감소': { 'impact': 0.3, 'frequency': 0.05, 'importance': 8.2, 'subtypes': ['복지 정책 강화', '진보적 세금 정책'] },
    '기업 성장': { 'impact': 0.4, 'frequency': 0.07, 'importance': 8.5, 'subtypes': ['혁신', '산업 성장', '투자 증가'] },
    '국가 안보 강화': { 'impact': 0.35, 'frequency': 0.04, 'importance': 9.0, 'subtypes': ['국경 통제 강화', '군사 훈련', '방위 산업 발전'] },
    '환경 보호': { 'impact': 0.25, 'frequency': 0.06, 'importance': 9.3, 'subtypes': ['온실가스 감축', '재생 에너지', '지속 가능성'] },
    '사회 복지 확대': { 'impact': 0.35, 'frequency': 0.08, 'importance': 8.8, 'subtypes': ['공공 의료', '주거 지원', '교육 기회 제공'] },
    '전통적 가치 강조': { 'impact': 0.2, 'frequency': 0.05, 'importance': 7.8, 'subtypes': ['가족 중심 정책', '종교 교육', '보수적 규범'] },
    '소수자 권리 강화': { 'impact': 0.3, 'frequency': 0.08, 'importance': 8.7, 'subtypes': ['성소수자 권리', '인종 평등', '장애인 권리'] },
    '경제 자유화': { 'impact': 0.4, 'frequency': 0.07, 'importance': 8.5, 'subtypes': ['자유무역 협정', '시장 규제 완화', '세금 인하'] },
    '반세계화 운동': { 'impact': 0.3, 'frequency': 0.05, 'importance': 7.6, 'subtypes': ['무역 제한', '국가 자립성 강화', '다국적 기업 규제'] },
    '청년 참여 증진': { 'impact': 0.25, 'frequency': 0.06, 'importance': 8.4, 'subtypes': ['정치 교육', '청년 투표율 증가', '청년 정책'] },
    '정상': {'impact': 0.0, 'frequency': 0.20, 'importance': 10.0, 'subtypes': ['정치적 안정', '사회적 안정', '경제적 안정']},
}

# 사건 영향
event_impact = {
    '자연재해': {
        'Far-left': 1.5, 'Left': 1.4, 'Center-left': 1.3, 'Centrist': 1.1, 'Center-right': 1.0, 'Right': 0.9, 'Far-right': 0.5,
        'Liberalism': 1.1, 'Republicanism': 1.0, 'Socialism': 1.4, 'Communism': 1.5, 'Anarchism': 0.7, 'Fascism': 0.5,
        'Social Democracy': 1.3, 'Green Politics': 1.9, 'Libertarianism': 0.8, 'Capitalist': 0.9, 'Mixed Economy': 1.2,
        'Welfare State': 1.6, 'Market Economy': 0.8, 'Environmentalism': 1.8, 'Social Justice': 1.5, 'Labor-rights': 1.4,
        'Civil Liberties': 1.0, 'Anti-racism': 1.2, 'Public Health': 1.0, 'Urban Development': 1.2, 'Disability Rights': 1.3
    },
    '이민': {
        'Far-left': 1.2, 'Left': 1.3, 'Center-left': 1.1, 'Centrist': 1.0, 'Center-right': 0.8, 'Right': 0.6, 'Far-right': 0.5,
        'Liberalism': 1.2, 'Conservatism': 0.6, 'Republicanism': 0.7, 'Socialism': 1.4, 'Anarchism': 1.0, 'Nationalism': 0.5,
        'Social Justice': 1.3, 'Labor-rights': 1.1, 'Individual-rights': 1.2, 'Civil Liberties': 1.1, 'Anti-racism': 1.5
    },
    '반이민': {
        'Far-left': 0.8, 'Left': 0.9, 'Center-left': 1.0, 'Centrist': 1.1, 'Center-right': 1.3, 'Right': 1.5, 'Far-right': 1.8,
        'Nationalism': 1.7, 'Populism': 1.6, 'Authoritarianism': 1.5, 'Conservatism': 1.4, 'Republicanism': 1.3, 'Anti-globalization': 1.2,
    },
    '경제 불황': {
        'Far-left': 1.5, 'Left': 1.4, 'Center-left': 1.3, 'Centrist': 1.1, 'Center-right': 1.0, 'Right': 0.9, 'Far-right': 0.8,
        'Socialism': 1.6, 'Communism': 1.5, 'Libertarianism': 0.7, 'Capitalist': 1.0, 'Mixed Economy': 1.3, 'Welfare State': 1.4,
        'Public Health': 1.2, 'Labor-rights': 1.6, 'Universal Basic Income': 1.4, 'Free-market': 0.8, 'Keynesianism': 1.5
    },
    '사회 운동': {
        'Far-left': 1.7, 'Left': 1.5, 'Center-left': 1.3, 'Centrist': 1.0, 'Center-right': 0.8, 'Right': 0.7, 'Far-right': 0.6,
        'Social Justice': 1.8, 'Labor-rights': 1.5, 'Civil Liberties': 1.4, 'Environmentalism': 1.2, 'Anti-corruption': 1.3,
        'Feminism': 1.6, 'Youth Politics': 1.4, 'Elderly Rights': 1.1
    },
    '노동 문제': {
        'Far-left': 1.6, 'Left': 1.5, 'Center-left': 1.3, 'Centrist': 1.1, 'Center-right': 0.9, 'Right': 0.8, 'Far-right': 0.7,
        'Labor-rights': 1.9, 'Social Justice': 1.7, 'Welfare State': 1.4, 'Universal Basic Income': 1.2, 'Protectionist': 1.0,
        'Civil Liberties': 1.1, 'Free-market': 0.7, 'Innovation': 1.3
    },
    '안보 위협': {
        'Far-left': 0.7, 'Left': 0.8, 'Center-left': 1.0, 'Centrist': 1.2, 'Center-right': 1.4, 'Right': 1.5, 'Far-right': 1.8,
        'Nationalism': 1.7, 'Authoritarianism': 1.6, 'Republicanism': 1.4, 'Conservatism': 1.5, 'Militarism': 1.9,
        'Public Health': 1.1, 'Civil Liberties': 0.8, 'Individual-rights': 0.9, 'Federalism': 1.2, 'Populism': 1.3
    },
    '빈부격차 감소': {
        'Far-left': 1.7, 'Left': 1.5, 'Center-left': 1.4, 'Centrist': 1.2, 'Center-right': 0.9, 'Right': 0.7, 'Far-right': 0.5,
        'Socialism': 1.6, 'Social Democracy': 1.5, 'Welfare State': 1.7, 'Social Justice': 1.8, 'Anti-racism': 1.4,
        'Labor-rights': 1.6, 'Civil Liberties': 1.3
    },
    '기업 성장': {
        'Far-left': 0.6, 'Left': 0.8, 'Center-left': 1.0, 'Centrist': 1.3, 'Center-right': 1.4, 'Right': 1.5, 'Far-right': 1.6,
        'Capitalist': 1.8, 'Free-market': 1.6, 'Libertarianism': 1.3, 'Conservatism': 1.5, 'Republicanism': 1.4, 'Innovation': 1.7
    },
    '국가 안보 강화': {
        'Far-left': 0.5, 'Left': 0.7, 'Center-left': 0.9, 'Centrist': 1.1, 'Center-right': 1.3, 'Right': 1.5, 'Far-right': 1.8,
        'Nationalism': 1.8, 'Authoritarianism': 1.7, 'Militarism': 1.9, 'Republicanism': 1.4, 'Federalism': 1.2, 'Public Health': 1.1
    },
    '환경 보호': {
        'Far-left': 1.5, 'Left': 1.7, 'Center-left': 1.6, 'Centrist': 1.3, 'Center-right': 1.1, 'Right': 0.9, 'Far-right': 0.7,
        'Green Politics': 1.9, 'Social Justice': 1.8, 'Environmentalism': 1.8, 'Liberalism': 1.3, 'Welfare State': 1.2,
        'Anti-globalization': 1.1, 'Labor-rights': 1.2, 'Public Health': 1.4
    },
    '사회 복지 확대': {
        'Far-left': 1.6, 'Left': 1.5, 'Center-left': 1.4, 'Centrist': 1.1, 'Center-right': 1.0, 'Right': 0.9, 'Far-right': 0.5,
        'Socialism': 1.8, 'Welfare State': 1.7, 'Social Justice': 1.6, 'Environmentalism': 1.3, 'Public Health': 1.5,
        'Civil Liberties': 1.2, 'Labor-rights': 1.4, 'Youth Politics': 1.1
    },
    '전통적 가치 강조': {
        'Far-left': 0.4, 'Left': 0.6, 'Center-left': 0.7, 'Centrist': 0.9, 'Center-right': 1.1, 'Right': 1.5, 'Far-right': 1.7,
        'Conservatism': 1.7, 'Nationalism': 1.5, 'Fascism': 1.6, 'Authoritarianism': 1.5, 'Populism': 1.4, 'Religious_right': 1.7
    },
    '소수자 권리 강화': {
        'Far-left': 1.6, 'Left': 1.5, 'Center-left': 1.4, 'Centrist': 1.1, 'Center-right': 1.0, 'Right': 0.8, 'Far-right': 0.5,
        'Socialism': 1.5, 'Liberalism': 1.6, 'Green Politics': 1.5, 'Social Justice': 1.7, 'Civil Liberties': 1.6, 'Youth Politics': 1.4
    },
    '경제 자유화': {
        'Far-left': 0.5, 'Left': 0.6, 'Center-left': 0.8, 'Centrist': 1.0, 'Center-right': 1.3, 'Right': 1.5, 'Far-right': 1.8,
        'Capitalism': 1.8, 'Free-market': 1.7, 'Libertarianism': 1.5, 'Conservatism': 1.4, 'Republicanism': 1.2, 'Neoliberalism': 1.6
    },
    '반세계화 운동': {
        'Far-left': 1.3, 'Left': 1.2, 'Center-left': 1.1, 'Centrist': 1.0, 'Center-right': 0.8, 'Right': 0.7, 'Far-right': 1.5,
        'Nationalism': 1.6, 'Populism': 1.5, 'Protectionism': 1.4, 'Socialism': 1.3, 'Fascism': 1.5, 'Labor-rights': 1.1
    },
    '청년 참여 증진': {
        'Far-left': 1.4, 'Left': 1.3, 'Center-left': 1.2, 'Centrist': 1.1, 'Center-right': 0.9, 'Right': 0.7, 'Far-right': 0.6,
        'Youth Politics': 1.5, 'Social Justice': 1.3, 'Civil Liberties': 1.2, 'Labor-rights': 1.4, 'Public Health': 1.1,
        'Environmentalism': 1.3
    },
    '정상': {
        'Far-left': 1.0,  # 안정된 사회적 조건을 통한 평화로운 변화 가능성
        'Left': 1.1,  # 사회적 안정 속에서 정책 추진 가능성
        'Center-left': 1.2,  # 일상적 상황에서 변화의 필요성 인식
        'Centrist': 1.3,  # 사회적 안정 속에서 균형 잡힌 접근
        'Center-right': 1.2,  # 경제적 안정성 유지
        'Right': 1.1,  # 개인의 책임 강조, 안정적인 사회 환경
        'Far-right': 1.0,  # 전통적 가치 유지, 안정 중시
        'Liberalism': 1.3,  # 개인의 자유와 권리가 존중되는 사회
        'Capitalism': 1.2,  # 경제적 성장과 안정의 조화
        'Welfare State': 1.2,  # 복지 제도의 안정적 운영
        'Environmentalism': 1.1,  # 환경 문제의 점진적 개선
        'Social Justice': 1.2,  # 공정한 기회 제공을 위한 환경 조성
    },
}