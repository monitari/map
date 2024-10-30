# Description: 정치 이념과 사건의 영향 관계를 정의한 파일

# 기본 이념 스펙트럼
ideological_spectrum = ['Far-left', 'Left', 'Center-left', 'Centrist', 'Center-right', 'Right','Far-right']

# 정치 이념 스펙트럼
main_alignments = [
    # 주요 정치 이념
    'Liberalism', 'Conservatism', 'Republicanism', 'Socialism', 'Communism', 
    'Anarchism', 'Fascism', 'Social Democracy', 'Green Politics', 'Libertarianism',
    
    # 경제/사회 체제
    'Capitalist', 'Socialist', 'Mixed Economy', 'Welfare State', 'Command Economy', 
    'Market Economy', 'State Capitalism', 'Cooperative Economy', 'Sharing Economy', 'Circular Economy', 
    'Progressive', 'Neo-liberalism',
    
    # 거버넌스/정치 방식
    'Nationalism', 'Populism', 'Technocratic', 'Anti-corruption', 'Regionalist', 
    'Authoritarianism', 'Totalitarianism', 'Decentralization', 'Direct Democracy', 'Federalism',
    
    # 주요 가치/이슈
    'Environmentalism', 'Social Justice', 'Labor-rights', 'Individual-rights', 'Religious', 
    'Secularism', 'Feminism', 'Gender Equality', 'LGBT Rights', 'Privacy Rights', 
    'Civil Liberties', 'Anti-racism', 'Mental Health Advocacy', 'Digital Rights', 'Animal Rights', 
    'Indigenous Rights', 'Disability Rights', 'Youth Politics', 'Elderly Rights',
    
    # 경제 정책
    'Free-market', 'Protectionist', 'Innovation', 'Universal Basic Income', 'Cooperative Economics', 
    'Keynesianism', 'Monetarism',
    
    # 특수 관심사
    'Pacifism', 'Militarism', 'Traditionalism', 'Modernism', 'Anti-globalization', 
    'Globalism', 'Sustainability', 'Climate Justice', 'Public Health', 'Social Entrepreneurship', 
    'Interfaith Dialogue', 'Civic Engagement', 'Urban Development', 'Rural Development',
    
    # 현대적 성향
    'Transhumanism', 'Post-scarcity Economics', 'Space Exploration Advocacy', 'Artificial Intelligence Ethics', 
    'Blockchain Governance', 'Techno-progressivism', 'Posthumanism',
]

# 사건 목록
events = {
    '자연재해': { 'impact': 0.15, 'frequency': 0.06, 'importance': 8.0, 'subtypes': ['지진', '태풍', '홍수', '가뭄', '화산폭발'] },
    '이민': { 'impact': 0.25, 'frequency': 0.08, 'importance': 7.5, 'subtypes': ['난민', '이주 노동자', '불법 이민'] },
    '반이민': { 'impact': 0.3, 'frequency': 0.08, 'importance': 8.0, 'subtypes': ['이주자 규제', '난민 반대', '국경 통제', '강제 송환'] },
    '경제 불황': { 'impact': 0.4, 'frequency': 0.12, 'importance': 9.0, 'subtypes': ['실업률 증가', '물가 상승', '소득 불평등'] },
    '사회 운동': { 'impact': 0.3, 'frequency': 0.10, 'importance': 8.5, 'subtypes': ['시위', '파업', '청년 운동', '폭력 사태', '시민 운동'] },
    '노동 문제': { 'impact': 0.35, 'frequency': 0.07, 'importance': 8.0, 'subtypes': ['최저임금', '근로시간', '노동 환경', '노동조합'] },
    '안보 위협': { 'impact': 0.5, 'frequency': 0.05, 'importance': 9.5, 'subtypes': ['테러', '국제 갈등', '군사 공격', '사이버 공격', '대량 파괴 무기'] },
    '빈부격차 감소': { 'impact': 0.3, 'frequency': 0.05, 'importance': 8.2, 'subtypes': ['복지 정책 강화', '진보적 세금 정책', '소득 재분배'] },
    '기업 성장': { 'impact': 0.4, 'frequency': 0.07, 'importance': 8.5, 'subtypes': ['혁신', '산업 성장', '투자 증가', '고용 증가'] },
    '국가 안보 강화': { 'impact': 0.35, 'frequency': 0.04, 'importance': 9.0, 'subtypes': ['국경 통제 강화', '군사 훈련', '방위 산업 발전', '국방 예산 증가'] },
    '환경 보호': { 'impact': 0.25, 'frequency': 0.06, 'importance': 9.3, 'subtypes': ['온실가스 감축', '재생 에너지', '지속 가능성', '환경 교육'] },
    '사회 복지 확대': { 'impact': 0.35, 'frequency': 0.08, 'importance': 8.8, 'subtypes': ['공공 의료', '주거 지원', '교육 기회 제공'] },
    '전통적 가치 강조': { 'impact': 0.2, 'frequency': 0.05, 'importance': 7.8, 'subtypes': ['가족 중심 정책', '종교 교육', '보수적 규범'] },
    '소수자 권리 강화': { 'impact': 0.3, 'frequency': 0.08, 'importance': 8.7, 'subtypes': ['성소수자 권리', '인종 평등', '장애인 권리'] },
    '경제 자유화': { 'impact': 0.4, 'frequency': 0.07, 'importance': 8.5, 'subtypes': ['자유무역 협정', '시장 규제 완화', '세금 인하', '자본 이동 자유화'] },
    '반세계화 운동': { 'impact': 0.3, 'frequency': 0.05, 'importance': 7.6, 'subtypes': ['무역 제한', '국가 자립성 강화', '다국적 기업 규제']},
    '청년 참여 증진': { 'impact': 0.25, 'frequency': 0.06, 'importance': 8.4, 'subtypes': ['정치 교육', '청년 투표율 증가', '청년 정책', '청년 기업 지원'] },
    '기술 혁신': {'impact': 0.45, 'frequency': 0.09, 'importance': 9.2, 'subtypes': ['인공지능 발전', '로봇 공학', '바이오기술', '에너지 혁신', '블록체인 기술']},
    '정상': {'impact': 0.0, 'frequency': 0.20, 'importance': 10.0, 'subtypes': ['정치적 안정', '사회적 안정', '경제적 안정', '정책 안정']},
}

# 사건 영향
event_impact = {
    '자연재해': {
        'Far-left': 1.5, 'Left': 1.4, 'Center-left': 1.3, 'Centrist': 1.1, 'Center-right': 1.0, 'Right': 0.9, 'Far-right': 0.5,
        'Liberalism': 1.1, 'Republicanism': 1.0, 'Socialism': 1.4, 'Communism': 1.5, 'Anarchism': 0.7, 'Fascism': 0.5, 'Social Democracy': 1.3,
        'Green Politics': 1.9, 'Libertarianism': 0.8, 'Capitalist': 0.9, 'Mixed Economy': 1.2, 'Welfare State': 1.6, 'Market Economy': 0.8,
        'Environmentalism': 1.8, 'Social Justice': 1.5, 'Labor-rights': 1.4, 'Civil Liberties': 1.0, 'Anti-racism': 1.2, 'Public Health': 1.0,
        'Urban Development': 1.2, 'Disability Rights': 1.3
    },
    '이민': {
        'Far-left': 1.2, 'Left': 1.3, 'Center-left': 1.1, 'Centrist': 1.0, 'Center-right': 0.8, 'Right': 0.6, 'Far-right': 0.5,
        'Liberalism': 1.2, 'Conservatism': 0.6, 'Republicanism': 0.7, 'Socialism': 1.4, 'Anarchism': 1.0, 'Nationalism': 0.5,
        'Social Justice': 1.3, 'Labor-rights': 1.1, 'Individual-rights': 1.2, 'Civil Liberties': 1.1, 'Anti-racism': 1.5
    },
    '반이민': {
        'Far-left': 0.8, 'Left': 0.9, 'Center-left': 1.0, 'Centrist': 1.1, 'Center-right': 1.3, 'Right': 1.5, 'Far-right': 1.8,
        'Nationalism': 1.7, 'Populism': 1.6, 'Authoritarianism': 1.5, 'Conservatism': 1.4, 'Republicanism': 1.3, 'Anti-globalization': 1.2
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
    '기술 혁신': {
        'Far-left': 1.2, 'Left': 1.3, 'Center-left': 1.4, 'Centrist': 1.1, 'Center-right': 1.3, 'Right': 1.5, 'Far-right': 1.4,
        'Liberalism': 1.4, 'Socialism': 1.3, 'Communism': 1.1, 'Anarchism': 1.2, 'Social Democracy': 1.3, 'Green Politics': 1.2,
        'Libertarianism': 1.5, 'Capitalist': 1.6, 'Mixed Economy': 1.3, 'Welfare State': 1.2, 'Market Economy': 1.4,
        'Environmentalism': 1.3, 'Social Justice': 1.1, 'Labor-rights': 1.2, 'Civil Liberties': 1.3, 'Anti-racism': 1.1,
        'Public Health': 1.2, 'Urban Development': 1.4, 'Disability Rights': 1.1, 'Technocratic': 2.0, 'Digital Rights': 1.3,
        'Blockchain Governance': 1.2, 'Universal Basic Income': 1.5, 'Interfaith Dialogue': 1.1, 'Civic Engagement': 1.4,
        'Techno-progressivism': 1.6, 'Posthumanism': 1.3, 'Transhumanism': 1.2, 'Post-scarcity Economics': 1.4,
        'Space Exploration Advocacy': 1.5, 'Artificial Intelligence Ethics': 1.3, 'Sustainability': 1.2
    },
    '정상': {
        'Far-left': 0.5, 'Left': 0.7, 'Center-left': 1.0, 'Centrist': 1.5, 'Center-right': 1.0, 'Right': 0.7, 'Far-right': 0.5,
        'Liberalism': 1.5, 'Conservatism': 1.4, 'Republicanism': 1.3, 'Socialism': 1.1, 'Communism': 1.1, 'Anarchism': 0.6,
        'Fascism': 0.5, 'Social Democracy': 1.2, 'Green Politics': 1.3, 'Libertarianism': 0.8, 'Capitalist': 0.9, 'Mixed Economy': 1.2,
        'Welfare State': 1.4, 'Market Economy': 0.8, 'Environmentalism': 1.3, 'Social Justice': 1.5, 'Labor-rights': 1.4,
        'Civil Liberties': 1.0, 'Anti-racism': 1.2, 'Public Health': 1.0, 'Urban Development': 1.2
    }
}
