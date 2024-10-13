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

events = {
    '자연재해': { 'impact': 0.15, 'frequency': 0.06, 'importance': 8.0, 'subtypes': ['대지진', '태풍', '홍수', '가뭄', '화산폭발'] },
    '경제위기': { 'impact': 0.45, 'frequency': 0.08, 'importance': 9.0, 'subtypes': ['금융위기', '무역전쟁', '인플레이션', '실업률급증', '산업붕괴'] },
    '안보위기': { 'impact': 0.30, 'frequency': 0.05, 'importance': 9.5, 'subtypes': ['전쟁위협', '테러', '사이버공격', '국경분쟁', '내전'] },
    '사회문제': { 'impact': 0.60, 'frequency': 0.18, 'importance': 8.5, 'subtypes': ['불평등심화', '교육위기', '고령화', '저출산', '주거난'] },
    '환경위기': { 'impact': 0.75, 'frequency': 0.14, 'importance': 8.2, 'subtypes': ['기후변화', '대기오염', '수질오염', '생태계파괴', '자원고갈'] },
    '정치스캔들': { 'impact': 1.05, 'frequency': 0.13, 'importance': 6.5, 'subtypes': ['부패', '권력남용', '선거조작', '정보유출', '정치자금비리'] },
    '기술혁신': { 'impact': 2.25, 'frequency': 0.18, 'importance': 7.0, 'subtypes': ['AI혁명', '우주개발', '신재생에너지', '바이오기술', '양자컴퓨팅'] },
    '외교마찰': { 'impact': 1.20, 'frequency': 0.10, 'importance': 7.8, 'subtypes': ['국경분쟁', '국제갈등', '동맹붕괴', '국제제재', '국제사법소송'] },
    '정상상태': { 'impact': 1.50, 'frequency': 0.24, 'importance': 5.0, 'subtypes': ['안정기', '성장기', '조정기', '전환기', '회복기'] },
    # 추가된 이벤트
    '의료혁신': { 'impact': 2.40, 'frequency': 0.072, 'importance': 8.5, 'subtypes': ['신약개발', '원격의료', '유전자치료', '맞춤형의학', '의료AI'] },
    '문화현상': { 'impact': 1.80, 'frequency': 0.216, 'importance': 6.5, 'subtypes': ['대중문화열풍', '문화다양성', '예술혁신', '전통부활', '문화교류'] },
    '교육혁신': { 'impact': 2.10, 'frequency': 0.120, 'importance': 7.8, 'subtypes': ['온라인학습', '평생교육', 'STEM교육', '국제교류', '교육평등'] },
    '사회운동': { 'impact': 1.95, 'frequency': 0.168, 'importance': 7.0, 'subtypes': ['인권운동', '환경운동', '노동운동', '여성운동', '시민운동'] },
    '경제호황': { 'impact': 2.55, 'frequency': 0.072, 'importance': 8.0, 'subtypes': ['경제성장', '일자리창출', '창업붐', '투자활성화', '소비증가'] },
    '기후변화': { 'impact': 0.90, 'frequency': 0.096, 'importance': 8.2, 'subtypes': ['온난화', '해빙', '해수면 상승', '극지반응', '기후재앙'] },
    '인구변화': { 'impact': 0.60, 'frequency': 0.072, 'importance': 8.0, 'subtypes': ['이민', '출산율 감소', '노령화', '도시화', '인구 이동'] },
    '팬데믹': { 'impact': 1.35, 'frequency': 0.06, 'importance': 9.5, 'subtypes': ['COVID-19', '전염병 대유행', '백신 개발', '공중 보건 위기', '사회적 거리 두기'] },
}

# 사건 영향 (1보다 큰 값은 영향력이 높음을 의미, 1보다 작은 값은 영향력이 낮음을 의미)
event_impact = {
    '자연재해': {
        'Liberalism': 1.1, 'Republicanism': 1.0, 'Socialism': 1.4, 'Communism': 1.5, 'Anarchism': 0.7, 'Fascism': 0.5,
        'Social Democracy': 1.3, 'Green Politics': 1.9, 'Libertarianism': 0.8, 'Capitalist': 0.9, 'Mixed Economy': 1.2, 
        'Welfare State': 1.6, 'Market Economy': 0.8, 'Environmentalism': 1.8, 'Social Justice': 1.5, 'Labor-rights': 1.4, 
        'Civil Liberties': 1.0, 'Anti-racism': 1.2, 'Public Health': 1.0, 'Urban Development': 1.2, 'Disability Rights': 1.3
    },
    '경제위기': {
        'Conservatism': 1.1, 'Republicanism': 1.0, 'Socialism': 1.6, 'Communism': 1.8, 'Fascism': 0.4, 'Social Democracy': 1.5,
        'Libertarianism': 0.6, 'Capitalist': 0.7, 'Mixed Economy': 1.1, 'Welfare State': 1.4, 'Keynesianism': 1.8, 'Innovation': 1.3,
        'Universal Basic Income': 1.4, 'Protectionist': 1.3, 'Free-market': 1.0, 'Cooperative Economics': 1.1, 'Monetarism': 0.8
    },
    '안보위기': {
        'Centrist': 0.8, 'Center-left': 0.7, 'Center-right': 1.3, 'Far-left': 0.6, 'Far-right': 1.4, 'Populism': 1.5,
        'Nationalism': 1.6, 'Authoritarianism': 1.5, 'Technocratic': 1.0, 'Civil Liberties': 0.5, 'Public Health': 1.1,
        'Globalism': 1.2, 'Regionalist': 1.1, 'Direct Democracy': 0.9, 'Federalism': 0.6, 'Decentralization': 0.7
    },
    '사회문제': {
        'Liberalism': 1.4, 'Socialism': 1.7, 'Communism': 1.6, 'Feminism': 1.8, 'LGBT Rights': 1.9, 'Anti-racism': 1.7, 
        'Civil Liberties': 1.5, 'Social Justice': 1.6, 'Mental Health Advocacy': 1.5, 'Environmentalism': 1.8, 'Labor-rights': 1.7, 
        'Individual-rights': 1.5, 'Religious': 1.4, 'Secularism': 1.4
    },
    '환경위기': {
        'Green Politics': 2.0, 'Environmentalism': 1.9, 'Social Democracy': 1.6, 'Socialism': 1.5, 'Liberalism': 1.4, 
        'Climate Justice': 1.8, 'Sustainability': 1.7,
    },
    '정치스캔들': {
        'Populism': 1.2, 'Anti-corruption': 1.3, 'Nationalism': 0.5, 'Authoritarianism': 0.3, 'Civil Liberties': 0.4, 
        'Social Justice': 1.1, 'Totalitarianism': 1.5, 'Decentralization': 1.2, 'Direct Democracy': 1.0, 'Federalism': 0.8, 
        'Globalism': 1.3, 'Regionalist': 1.2,
    },
    '기술혁신': {
        'Libertarianism': 1.5, 'Social Democracy': 1.3, 'Technocratic': 1.8, 'Progressive': 1.6, 'Innovation': 1.9, 
        'Artificial Intelligence Ethics': 1.4, 'Blockchain Governance': 1.7, 'Techno-progressivism': 1.6, 
        'Posthumanism': 1.8, 'Transhumanism': 1.9, 'Post-scarcity Economics': 1.7, 'Youth Politics': 1.3, 
        'Elderly Rights': 1.1, 'Space Exploration Advocacy': 1.5, 'Digital Rights': 1.4, 'Animal Rights': 1.2, 
        'Civic Engagement': 1.1,
    },
    '외교마찰': {
        'Nationalism': 1.4, 'Populism': 1.3, 'Conservatism': 1.1, 'Far-right': 1.2, 'Republicanism': 1.0, 
        'Technocratic': 1.1, 'Authoritarianism': 1.5, 'Totalitarianism': 1.6, 'Decentralization': 1.2, 
        'Direct Democracy': 1.0, 'Federalism': 0.9, 'Globalism': 1.3, 'Regionalist': 1.2, 
        'Interfaith Dialogue': 1.1, 'Civic Engagement': 1.1, 'Urban Development': 1.2, 'Rural Development': 1.0,
    },
    '정상상태': {
        'Centrist': 1.0, 'Liberalism': 1.1, 'Conservatism': 1.0, 'Social Democracy': 1.1, 'Green Politics': 1.2, 
        'Libertarianism': 1.0, 'Progress': 1.2, 'Innovation': 1.0, 'Sustainability': 1.3, 'Public Health': 1.2, 
        'Social Entrepreneurship': 1.0, 'Interfaith Dialogue': 1.0, 'Civic Engagement': 1.1,
    },
    '의료혁신': {
        'Social Democracy': 1.6, 'Welfare State': 1.5, 'Progressive': 1.8, 'Liberalism': 1.4, 'Public Health': 1.9, 
        'Mental Health Advocacy': 1.7, 'Disability Rights': 1.5, 'Environmentalism': 1.7, 'Civil Liberties': 1.6, 
        'Anti-racism': 1.4, 'LGBT Rights': 1.5, 'Feminism': 1.3
    },
    '문화현상': {
        'Liberalism': 1.2, 'Feminism': 1.3, 'Environmentalism': 1.5, 'Social Justice': 1.4, 'LGBT Rights': 1.6, 
        'Progressive': 1.5, 'Civil Liberties': 1.2, 'Public Health': 1.3, 'Anti-racism': 1.2, 'Interfaith Dialogue': 1.2, 
        'Civic Engagement': 1.3, 'Urban Development': 1.1,
    },
    '교육혁신': {
        'Progressive': 1.5, 'Liberalism': 1.4, 'Social Democracy': 1.6, 'Innovation': 1.3, 'Universal Basic Income': 1.2, 
        'Youth Politics': 1.5, 'Elderly Rights': 1.1, 'Feminism': 1.2, 'LGBT Rights': 1.3, 'Anti-racism': 1.0, 
        'Social Justice': 1.4, 'Civil Liberties': 1.3, 'Public Health': 1.2,
    },
    '사회운동': {
        'Feminism': 1.7, 'LGBT Rights': 1.8, 'Anti-racism': 1.6, 'Social Justice': 1.5, 'Civil Liberties': 1.4, 
        'Public Health': 1.2, 'Youth Politics': 1.5, 'Elderly Rights': 1.3, 'Environmentalism': 1.6, 'Disability Rights': 1.7, 
        'Indigenous Rights': 1.8, 'Digital Rights': 1.9, 'Animal Rights': 1.6, 'Interfaith Dialogue': 1.5, 
        'Civic Engagement': 1.4, 'Urban Development': 1.3, 'Rural Development': 1.2
    },
    '경제호황': {
        'Capitalist': 1.6, 'Conservatism': 1.1, 'Republicanism': 1.0, 'Libertarianism': 1.3, 'Mixed Economy': 1.4, 
        'Social Democracy': 1.5, 'Progressive': 1.2, 'Innovation': 1.4, 'Social Justice': 1.2, 'Environmentalism': 1.1, 
        'Sustainability': 1.3, 'Welfare State': 1.4, 'Civic Engagement': 1.1, 'Public Health': 1.2, 'Labor-rights': 1.2
    },
    '기후변화': {
        'Green Politics': 2.1, 'Environmentalism': 2.0, 'Socialism': 1.6, 'Social Democracy': 1.5, 'Progressive': 1.7, 
        'Climate Justice': 1.8, 'Sustainability': 1.6, 'Capitalist': 0.9, 'Welfare State': 1.4, 'Public Health': 1.3,
    },
    '인구변화': {
        'Nationalism': 1.2, 'Liberalism': 1.1, 'Feminism': 1.4, 'Social Justice': 1.3, 'Anti-racism': 1.2, 
        'Civic Engagement': 1.4, 'Public Health': 1.0, 'Environmentalism': 1.1, 'Labor-rights': 1.2, 
        'Direct Democracy': 1.3, 'Federalism': 1.0, 'Regionalist': 1.1, 'Youth Politics': 1.4,
    },
    '팬데믹': {
        'Public Health': 2.0, 'Social Democracy': 1.6, 'Civil Liberties': 1.2, 'Environmentalism': 1.3, 
        'Anti-racism': 1.1, 'Civic Engagement': 1.4, 'Mental Health Advocacy': 1.5, 'Disability Rights': 1.4,
        'Globalism': 1.2, 'Decentralization': 1.1, 'Regionalist': 1.0
    }
}
