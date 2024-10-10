import pandas as pd
import numpy as np
import random
import math
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 정치 성향
alignments = [
    'Centrist', 'Center-left', 'Center-right', 'Far-left', 'Far-right', 'Left', 'Right', 
    'Nationalism', 'Populism', 'Environmentalism', 'Single-issue', 'Religious', 'Progressive', 'Conservative', 
    'Social Democracy', 'Social Justice', 'Liberal', 'Libertarian', 'Technocratic', 'Agrarian', 
    'Federalist', 'Separatist', 'Traditionalist', 'Militarist', 'Pacifist', 'Secular', 'Theocratic',
    'Socialist', 'Capitalist', 'Regionalist', 'Industrialist', 'Protectionist', 'Free-market', 'Labor-rights', 'Individual-rights',
    'Unification', 'Innovation', 'Authoritarian', 'Anti-corruption', 'Transparency', 'Modernist', 'Autonomist', 'Economic-development',
    'Equality', 'Socialism', 'Anti-elite', 'Anti-nuclear', 'Decentralization', 'Rural', 'Agriculture', 'Anti-immigrant'
]

# 사건 영향 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
events = {
    '자연재해': { 'impact': 9.5, 'frequency': 0.05, 'importance': 8.0, 'subtypes': ['대지진', '태풍', '홍수', '가뭄', '화산폭발'] },
    '경제위기': { 'impact': 8.3, 'frequency': 0.08, 'importance': 9.0, 'subtypes': ['금융위기', '무역전쟁', '인플레이션', '실업률급증', '산업붕괴'] },
    '안보위기': { 'impact': 10.0, 'frequency': 0.03, 'importance': 9.5, 'subtypes': ['전쟁위협', '테러', '사이버공격', '국경분쟁', '내전'] },
    '사회문제': { 'impact': 6.7, 'frequency': 0.15, 'importance': 7.5, 'subtypes': ['불평등심화', '교육위기', '고령화', '저출산', '주거난'] },
    '환경위기': { 'impact': 7.8, 'frequency': 0.10, 'importance': 8.2, 'subtypes': ['기후변화', '대기오염', '수질오염', '생태계파괴', '자원고갈'] },
    '정치스캔들': { 'impact': 5.4, 'frequency': 0.12, 'importance': 6.8, 'subtypes': ['부패', '권력남용', '선거조작', '정보유출', '정치자금비리'] },
    '기술혁신': { 'impact': 4.9, 'frequency': 0.15, 'importance': 7.0, 'subtypes': ['AI혁명', '우주개발', '신재생에너지', '바이오기술', '양자컴퓨팅'] },
    '외교관계': { 'impact': 6.3, 'frequency': 0.12, 'importance': 7.2, 'subtypes': ['동맹강화', '국제고립', '통상마찰', '문화충돌', '국제협력'] },
    '정상상태': { 'impact': 1.0, 'frequency': 0.20, 'importance': 5.0, 'subtypes': ['안정기', '성장기', '조정기', '전환기', '회복기'] }
}

# 사건 영향 (1보다 큰 값은 긍정적 영향, 1보다 작은 값은 부정적 영향)
event_impact = {
    '자연재해': {
        'Centrist': 1.23, 'Center-left': 1.52, 'Center-right': 1.21, 'Far-left': 1.83, 'Far-right': 1.04, 'Left': 1.81, 'Right': 1.23,
        'Nationalism': 1.02, 'Populism': 1.42, 'Environmentalism': 1.84, 'Single-issue': 1.23, 'Religious': 1.14, 'Progressive': 1.73,
        'Conservative': 1.03, 'Social Democracy': 1.74, 'Social Justice': 1.45, 'Liberal': 1.34, 'Libertarian': 1.25, 'Technocratic': 1.92,
        'Agrarian': 1.05, 'Federalist': 1.24, 'Separatist': 1.06, 'Traditionalist': 1.13, 'Militarist': 0.94, 'Pacifist': 1.21, 'Secular': 1.53,
        'Theocratic': 1.04, 'Socialist': 1.82, 'Capitalist': 1.13, 'Regionalist': 1.12, 'Industrialist': 0.95, 'Protectionist': 1.23,
        'Free-market': 1.14, 'Labor-rights': 1.64, 'Individual-rights': 1.23, 'Unification': 1.24, 'Innovation': 1.45, 'Authoritarian': 1.13,
        'Anti-corruption': 1.42, 'Transparency': 1.63, 'Modernist': 1.45, 'Autonomist': 1.12, 'Economic-development': 1.14,
        'Equality': 0.85, 'Socialism': 0.92, 'Anti-elite': 0.75, 'Anti-nuclear': 1.10, 'Decentralization': 1.08, 'Rural': 0.90, 'Agriculture': 0.88, 'Anti-immigrant': 0.82 
    },
    '경제위기': {
        'Centrist': 1.24, 'Center-left': 1.53, 'Center-right': 1.62, 'Far-left': 1.84, 'Far-right': 1.63, 'Left': 1.63, 'Right': 1.54,
        'Nationalism': 1.43, 'Populism': 1.82, 'Environmentalism': 1.04, 'Single-issue': 1.03, 'Religious': 1.34, 'Progressive': 1.23,
        'Conservative': 1.34, 'Social Democracy': 1.73, 'Social Justice': 1.63, 'Liberal': 1.14, 'Libertarian': 1.63, 'Technocratic': 1.83,
        'Agrarian': 1.23, 'Federalist': 1.53, 'Separatist': 1.14, 'Traditionalist': 1.34, 'Militarist': 1.13, 'Pacifist': 1.03, 'Secular': 1.23,
        'Theocratic': 1.13, 'Socialist': 1.93, 'Capitalist': 0.94, 'Regionalist': 1.13, 'Industrialist': 1.53, 'Protectionist': 1.53,
        'Free-market': 1.03, 'Labor-rights': 1.63, 'Individual-rights': 1.14, 'Unification': 1.23, 'Innovation': 1.63, 'Authoritarian': 1.63,
        'Anti-corruption': 1.63, 'Transparency': 1.53, 'Modernist': 1.63, 'Autonomist': 1.13, 'Economic-development': 1.83,
        'Equality': 0.75, 'Socialism': 1.20, 'Anti-elite': 0.70, 'Anti-nuclear': 1.25, 'Decentralization': 1.18, 'Rural': 0.85, 'Agriculture': 0.80, 'Anti-immigrant': 0.78 
    },
    '안보위기': {
        'Centrist': 1.03, 'Center-left': 0.84, 'Center-right': 1.53, 'Far-left': 0.74, 'Far-right': 1.83, 'Left': 1.03, 'Right': 1.53,
        'Nationalism': 1.83, 'Populism': 1.73, 'Environmentalism': 0.64, 'Single-issue': 0.93, 'Religious': 1.53, 'Progressive': 0.74,
        'Conservative': 1.53, 'Social Democracy': 0.84, 'Social Justice': 0.93, 'Liberal': 1.03, 'Libertarian': 0.84, 'Technocratic': 1.34,
        'Agrarian': 1.34, 'Federalist': 1.53, 'Separatist': 1.43, 'Traditionalist': 1.53, 'Militarist': 1.93, 'Pacifist': 0.43, 'Secular': 1.23,
        'Theocratic': 1.34, 'Socialist': 1.03, 'Capitalist': 1.43, 'Regionalist': 1.23, 'Industrialist': 1.53, 'Protectionist': 1.53,
        'Free-market': 1.14, 'Labor-rights': 0.93, 'Individual-rights': 1.03, 'Unification': 1.23, 'Innovation': 1.34, 'Authoritarian': 1.73,
        'Anti-corruption': 1.23, 'Transparency': 1.03, 'Modernist': 1.23, 'Autonomist': 1.34, 'Economic-development': 1.63,
        'Equality': 0.90, 'Socialism': 0.88, 'Anti-elite': 0.65, 'Anti-nuclear': 1.28, 'Decentralization': 1.25, 'Rural': 1.10, 'Agriculture': 1.12, 'Anti-immigrant': 1.35 
    },
    '사회문제': {
        'Centrist': 1.42, 'Center-left': 1.23, 'Center-right': 1.12, 'Far-left': 1.04, 'Far-right': 0.93, 'Left': 1.24, 'Right': 1.13,
        'Nationalism': 1.05, 'Populism': 0.92, 'Environmentalism': 1.54, 'Single-issue': 1.21, 'Religious': 1.03, 'Progressive': 1.52,
        'Conservative': 0.91, 'Social Democracy': 1.43, 'Social Justice': 1.62, 'Liberal': 1.25, 'Libertarian': 1.02, 'Technocratic': 1.23,
        'Agrarian': 1.14, 'Federalist': 1.22, 'Separatist': 1.06, 'Traditionalist': 0.94, 'Militarist': 0.92, 'Pacifist': 1.32, 'Secular': 1.53,
        'Theocratic': 1.01, 'Socialist': 1.55, 'Capitalist': 0.84, 'Regionalist': 1.12, 'Industrialist': 0.91, 'Protectionist': 0.93,
        'Free-market': 1.04, 'Labor-rights': 1.64, 'Individual-rights': 1.42, 'Unification': 1.13, 'Innovation': 1.34, 'Authoritarian': 0.82,
        'Anti-corruption': 1.45, 'Transparency': 1.42, 'Modernist': 1.23, 'Autonomist': 1.12, 'Economic-development': 1.41,
        'Equality': 0.65, 'Socialism': 1.30, 'Anti-elite': 0.55, 'Anti-nuclear': 1.35, 'Decentralization': 1.20, 'Rural': 1.15, 'Agriculture': 1.18, 'Anti-immigrant': 1.12     
    },
    '환경위기': {
        'Centrist': 1.12, 'Center-left': 1.54, 'Center-right': 1.03, 'Far-left': 1.62, 'Far-right': 0.92, 'Left': 1.23, 'Right': 0.84,
        'Nationalism': 1.13, 'Populism': 1.42, 'Environmentalism': 1.92, 'Single-issue': 1.53, 'Religious': 0.93, 'Progressive': 1.42,
        'Conservative': 0.91, 'Social Democracy': 1.64, 'Social Justice': 1.32, 'Liberal': 1.12, 'Libertarian': 0.92, 'Technocratic': 1.42,
        'Agrarian': 1.23, 'Federalist': 1.03, 'Separatist': 0.92, 'Traditionalist': 0.84, 'Militarist': 0.74, 'Pacifist': 1.32, 'Secular': 1.23,
        'Theocratic': 1.02, 'Socialist': 1.62, 'Capitalist': 0.82, 'Regionalist': 1.13, 'Industrialist': 0.92, 'Protectionist': 1.02,
        'Free-market': 0.82, 'Labor-rights': 1.32, 'Individual-rights': 1.12, 'Unification': 1.12, 'Innovation': 1.52, 'Authoritarian': 0.82,
        'Anti-corruption': 1.32, 'Transparency': 1.42, 'Modernist': 1.23, 'Autonomist': 1.13, 'Economic-development': 1.32,
        'Equality': 0.50, 'Socialism': 1.45, 'Anti-elite': 0.60, 'Anti-nuclear': 1.45, 'Decentralization': 1.25, 'Rural': 1.10, 'Agriculture': 1.22, 'Anti-immigrant': 1.15
    },
    '정치스캔들': {
        'Centrist': 1.52, 'Center-left': 1.72, 'Center-right': 1.03, 'Far-left': 2.02, 'Far-right': 2.23, 'Left': 1.92, 'Right': 1.42,
        'Nationalism': 1.32, 'Populism': 2.62, 'Environmentalism': 1.32, 'Single-issue': 1.42, 'Religious': 1.32, 'Progressive': 1.72,
        'Conservative': 1.02, 'Social Democracy': 2.02, 'Social Justice': 1.82, 'Liberal': 1.72, 'Libertarian': 1.62, 'Technocratic': 1.72,
        'Agrarian': 1.32, 'Federalist': 1.42, 'Separatist': 1.42, 'Traditionalist': 1.12, 'Militarist': 1.22, 'Pacifist': 1.02, 'Secular': 1.42,
        'Theocratic': 1.02, 'Socialist': 1.82, 'Capitalist': 1.52, 'Regionalist': 1.32, 'Industrialist': 1.32, 'Protectionist': 1.42,
        'Free-market': 1.62, 'Labor-rights': 1.72, 'Individual-rights': 1.62, 'Unification': 1.42, 'Innovation': 1.72, 'Authoritarian': 2.02,
        'Anti-corruption': 2.42, 'Transparency': 2.02, 'Modernist': 1.62, 'Autonomist': 1.52, 'Economic-development': 1.52,
        'Equality': 1.20, 'Socialism': 1.10, 'Anti-elite': 0.70, 'Anti-nuclear': 1.30, 'Decentralization': 1.15, 'Rural': 1.10, 'Agriculture': 1.20, 'Anti-immigrant': 1.18
    },
    '기술혁신': {
        'Centrist': 1.62, 'Center-left': 1.52, 'Center-right': 1.72, 'Far-left': 2.02, 'Far-right': 1.32, 'Left': 1.72, 'Right': 1.62,
        'Nationalism': 1.32, 'Populism': 1.82, 'Environmentalism': 1.82, 'Single-issue': 1.42, 'Religious': 1.52, 'Progressive': 2.02,
        'Conservative': 1.52, 'Social Democracy': 1.82, 'Social Justice': 1.52, 'Liberal': 1.72, 'Libertarian': 1.72, 'Technocratic': 2.32,
        'Agrarian': 1.32, 'Federalist': 1.52, 'Separatist': 1.42, 'Traditionalist': 1.22, 'Militarist': 1.42, 'Pacifist': 1.42, 'Secular': 1.62,
        'Theocratic': 1.22, 'Socialist': 1.52, 'Capitalist': 2.02, 'Regionalist': 1.52, 'Industrialist': 2.02, 'Protectionist': 1.42,
        'Free-market': 2.32, 'Labor-rights': 1.62, 'Individual-rights': 1.62, 'Unification': 1.52, 'Innovation': 2.42, 'Authoritarian': 1.22,
        'Anti-corruption': 1.72, 'Transparency': 1.52, 'Modernist': 2.02, 'Autonomist': 1.62, 'Economic-development': 2.02,
        'Equality': 1.35, 'Socialism': 1.38, 'Anti-elite': 1.15, 'Anti-nuclear': 1.50, 'Decentralization': 1.28, 'Rural': 1.15, 'Agriculture': 1.20, 'Anti-immigrant': 1.12 
    },
    '외교관계': {
        'Centrist': 1.52, 'Center-left': 1.63, 'Center-right': 1.74, 'Far-left': 1.53, 'Far-right': 1.85, 'Left': 1.64, 'Right': 1.82,
        'Nationalism': 2.01, 'Populism': 1.83, 'Environmentalism': 1.24, 'Single-issue': 1.34, 'Religious': 1.63, 'Progressive': 1.65,
        'Conservative': 1.54, 'Social Democracy': 1.84, 'Social Justice': 1.52, 'Liberal': 1.63, 'Libertarian': 1.23, 'Technocratic': 1.82,
        'Agrarian': 1.45, 'Federalist': 1.62, 'Separatist': 1.42, 'Traditionalist': 1.53, 'Militarist': 1.84, 'Pacifist': 1.62, 'Secular': 1.64,
        'Theocratic': 1.42, 'Socialist': 1.64, 'Capitalist': 1.82, 'Regionalist': 1.53, 'Industrialist': 1.74, 'Protectionist': 1.73,
        'Free-market': 1.63, 'Labor-rights': 1.64, 'Individual-rights': 1.74, 'Unification': 1.62, 'Innovation': 1.84, 'Authoritarian': 1.64,
        'Anti-corruption': 1.74, 'Transparency': 1.73, 'Modernist': 1.74, 'Autonomist': 1.63, 'Economic-development': 1.74,
        'Equality': 0.85, 'Socialism': 1.15, 'Anti-elite': 0.70, 'Anti-nuclear': 1.35, 'Decentralization': 1.28, 'Rural': 1.12, 'Agriculture': 1.18, 'Anti-immigrant': 1.40 
    },
    '정상상태': {
        'Centrist': 1.53, 'Center-left': 1.64, 'Center-right': 1.63, 'Far-left': 1.54, 'Far-right': 1.53, 'Left': 1.54, 'Right': 1.53,
        'Nationalism': 1.43, 'Populism': 1.54, 'Environmentalism': 1.54, 'Single-issue': 1.32, 'Religious': 1.43, 'Progressive': 1.54,
        'Conservative': 1.53, 'Social Democracy': 1.64, 'Social Justice': 1.54, 'Liberal': 1.54, 'Libertarian': 1.54, 'Technocratic': 1.54,
        'Agrarian': 1.43, 'Federalist': 1.43, 'Separatist': 1.43, 'Traditionalist': 1.43, 'Militarist': 1.54, 'Pacifist': 1.54, 'Secular': 1.54,
        'Theocratic': 1.24, 'Socialist': 1.54, 'Capitalist': 1.64, 'Regionalist': 1.43, 'Industrialist': 1.54, 'Protectionist': 1.43,
        'Free-market': 1.54, 'Labor-rights': 1.54, 'Individual-rights': 1.54, 'Unification': 1.54, 'Innovation': 1.54, 'Authoritarian': 1.34,
        'Anti-corruption': 1.54, 'Transparency': 1.54, 'Modernist': 1.54, 'Autonomist': 1.43, 'Economic-development': 1.54,
        'Equality': 1.10, 'Socialism': 1.25, 'Anti-elite': 1.15, 'Anti-nuclear': 1.08, 'Decentralization': 1.15, 'Rural': 1.05, 'Agriculture': 1.08, 'Anti-immigrant': 1.18 
    }
}

# 주요 대형 정당
major_parties = {
    '중앙당': ['Centrist', 'Right', 'Big Tent', 'Center-right', 'Center-left', 'Conservative', 'Liberal'],
    '통합 트라야비야': ['Center-right', 'Right', 'Conservative', 'Nationalism', 'Populism'],
    '개혁당': ['Liberal', 'Right', 'Reformist', 'Technocratic', 'Innovation', 'Progressive', 'Center-right'],
    '자유민주연합': ['Liberal', 'Right', 'Free-market', 'Individual-rights', 'Conservative', 'Center-right', 'Technocratic'],
}

# 중형 규모 정당
medium_parties = {
    '사회민주당': ['Social Democracy', 'Center-left', 'Progressive', 'Social Justice', 'Labor-rights', 'Environmentalism'],
    '민주와 자유': ['Centrist', 'Center-left', 'Progressive', 'Social Justice', 'Environmentalism', 'Anti-corruption'],
    '진보를 외치다': ['Left', 'Progressive', 'Social Justice', 'Environmentalism', 'Anti-corruption'],
    '민주통합당': ['Center-left', 'Progressive', 'Social Justice', 'Environmentalism', 'Labor-rights', 'Social Democracy'],
    '청년당': ['Youth-focused', 'Progressive', 'Digital', 'Innovation', 'Social Justice', 'Center-left', 'Centrist'],
    '국가를 위한 보수당': ['Nationalism', 'Right', 'Conservative', 'Traditionalist', 'Religious', 'Free-market'],
    '시민이 모였다!': ['Centrist', 'Anti-corruption', 'Transparency', 'Progressive', 'Center-left', 'Left'],
    '자유혁신당': ['Center-left', 'Left', 'Progressive', 'Reformist', 'Technocratic', 'Innovation'],
    '국민자유전선': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist', 'Regionalist'],
    '새희망당': ['Right', 'Conservative', 'Traditionalist', 'Nationalism', 'Protectionist', 'Regionalist'],
}

# 소수 정당
minor_parties = {
    '노동자당': ['Social Democracy', 'Left', 'Labor-rights', 'Social Justice', 'Progressive', 'Far-left'],
    '특이점이 온다': ['Technocratic', 'Modernist', 'Innovation', 'Progressive', 'Environmentalism'],
    '평화': ['Pacifist', 'Environmentalism', 'Social Justice', 'Progressive'],
    '녹색환경보호당': ['Environmentalism', 'Progressive', 'Social Justice', 'Left'],
    '국민행동당': ['Populism', 'Right', 'Nationalism', 'Anti-corruption', 'Transparency', 'Conservative'],
    '정의': ['Social Justice', 'Left', 'Progressive', 'Environmentalism', 'Anti-corruption'],
    '미래당': ['Technocratic', 'Innovation', 'Progressive', 'Environmentalism'],
    '농민당': ['Agrarian', 'Right', 'Protectionist', 'Agriculture', 'Rural', 'Conservative'],
    '통일당': ['Pacifist', 'Unification', 'Conservative', 'Centrist', 'Right', 'Nationalism'],
    '과학기술당': ['Technocratic', 'Innovation', 'Progressive', 'Environmentalism'],
    '전사회당': ['Far-left', 'Equality', 'Socialism', 'Social Justice', 'Progressive', 'Anti-elite'],
    '생명당': ['Environmentalism', 'Progressive', 'Social Justice', 'Regionalist', 'Anti-nuclear', 'Decentralization'],
    '보호하라!': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist', 'Anti-immigrant'],
}

# 지역 정당
regional_parties = {
    '그미즈리 민주당': {'region': '그미즈리', 'ideology': ['Centrist', 'Right', 'Economic-development', 'Industrialist', 'Technocratic', 'Progressive']},
    '하파차의 후예': {'region': '하파차', 'ideology': ['Nationalism', 'Right', 'Conservative', 'Traditionalist', 'Regionalist', 'Protectionist']},
    '도마니 연합': {'region': '도마니', 'ideology': ['Centrist', 'Right', 'Conservative', 'Economic-development', 'Industrialist', 'Technocratic']},
    '테트라 인민당': {'region': '테트라', 'ideology':  ['Socialist', 'Left', 'Progressive', 'Social Justice', 'Environmentalism', 'Labor-rights']},
    '세오어 보호당': {'region': '그라나데, 포어', 'ideology': ['Far-right', 'Nationalism', 'Conservative', 'Traditionalist', 'Protectionist', 'Regionalist']},
    '살기좋은 안텐시' : {'region': '안텐시', 'ideology': ['Environmentalism', 'Progressive', 'Social Justice', 'Centrist', 'Left', 'Regionalist']},
    '림덴시를 위하여': {'region': '림덴시', 'ideology': ['Agrarian', 'Rural', 'Conservative', 'Traditionalist', 'Protectionist', 'Regionalist']},
}

# 주와 행정구역별 정당 선호 지수 정의 (예시)
party_preference_map = {
    # 아이리카 주 (수도권, 경제, 문화, 예술의 중심)
    "메초오비카": {"Conservative": 1.32, "Progressive": 0.68},
    "아브레": {"Conservative": 1.21, "Progressive": 0.79},
    "피에트라": {"Conservative": 0.83, "Progressive": 1.17},
    "아이리카": {"Conservative": 0.95, "Progressive": 1.05},
    "메르네": {"Conservative": 0.92, "Progressive": 1.08},
    "츠비키": {"Conservative": 0.87, "Progressive": 1.13},
    "하르바트": {"Conservative": 1.11, "Progressive": 0.89},

    # 그라나데 주 (어업 중심, 낙후)
    "안파키": {"Conservative": 1.23, "Progressive": 0.77},
    "아파그라나다": {"Conservative": 1.14, "Progressive": 0.86},
    "페카그라나다": {"Conservative": 1.06, "Progressive": 0.94},
    "그라나다": {"Conservative": 1.12, "Progressive": 0.88},
    "보피노": {"Conservative": 1.22, "Progressive": 0.78},
    "메르노": {"Conservative": 1.13, "Progressive": 0.87},

    # 그미즈리 주 (1급 행정구, 중공업, 교통 중심)
    "오크모": {"Conservative": 1.12, "Progressive": 0.88},
    "미톤노": {"Conservative": 1.15, "Progressive": 0.85},
    "페아그": {"Conservative": 0.91, "Progressive": 1.09},
    "그미즈리": {"Conservative": 0.85, "Progressive": 1.15},
    "아센시": {"Conservative": 1.02, "Progressive": 0.98},
    "메깅고": {"Conservative": 0.94, "Progressive": 1.06},
    "호오토": {"Conservative": 1.11, "Progressive": 0.89},
    "키에오": {"Conservative": 0.93, "Progressive": 1.07},

    # 도마니 주 (첨단 산업 중심)
    "오브니": {"Conservative": 1.19, "Progressive": 0.81},
    "바스바드": {"Conservative": 1.13, "Progressive": 0.87},
    "케릴티": {"Conservative": 1.21, "Progressive": 0.79},
    "메고기": {"Conservative": 1.15, "Progressive": 0.85},
    "에링고": {"Conservative": 1.02, "Progressive": 0.98},
    "커피": {"Conservative": 1.18, "Progressive": 0.82},
    "즈조이": {"Conservative": 1.11, "Progressive": 0.89},
    "가안": {"Conservative": 1.20, "Progressive": 0.80},
    "브고홀": {"Conservative": 1.14, "Progressive": 0.86},
    "모옹홀": {"Conservative": 1.17, "Progressive": 0.83},
    "메옹": {"Conservative": 1.12, "Progressive": 0.88},

    # 림덴시 주 (1차 산업 중심, 기업농, 축산업의 중심)
    "파미즈": {"Conservative": 0.82, "Progressive": 1.18},
    "스피가": {"Conservative": 0.91, "Progressive": 1.09},
    "아르고": {"Conservative": 0.84, "Progressive": 1.16},
    "모리고": {"Conservative": 0.93, "Progressive": 1.07},
    "펜보드": {"Conservative": 0.85, "Progressive": 1.15},
    "메바치": {"Conservative": 0.92, "Progressive": 1.08},
    "모호카": {"Conservative": 0.83, "Progressive": 1.17},
    "린토카": {"Conservative": 0.94, "Progressive": 1.06},
    "낙소": {"Conservative": 0.86, "Progressive": 1.14},
    "보빈": {"Conservative": 0.91, "Progressive": 1.09},
    "라토카": {"Conservative": 0.87, "Progressive": 1.13},
    "세오고": {"Conservative": 0.90, "Progressive": 1.10},
    "시안": {"Conservative": 0.84, "Progressive": 1.16},
    "보어": {"Conservative": 0.89, "Progressive": 1.11},

    # 메세기 주 (최북단, 광업 중심)
    "크라나": {"Conservative": 1.01, "Progressive": 0.99},
    "나다이": {"Conservative": 1.12, "Progressive": 0.88},
    "옹피오": {"Conservative": 0.92, "Progressive": 1.08},
    "메세기": {"Conservative": 1.03, "Progressive": 0.97},
    "포크란": {"Conservative": 1.11, "Progressive": 0.89},
    "크레이": {"Conservative": 0.93, "Progressive": 1.07},
    "안파기": {"Conservative": 1.04, "Progressive": 0.96},

    # 미네바 주 (혁신 지구, IT 중심, 국경지대)
    "아리나": {"Conservative": 0.81, "Progressive": 1.19},
    "만토": {"Conservative": 0.92, "Progressive": 1.08},
    "메가": {"Conservative": 0.83, "Progressive": 1.17},
    "코에가": {"Conservative": 0.91, "Progressive": 1.09},
    "민마나": {"Conservative": 0.82, "Progressive": 1.18},
    "모에바": {"Conservative": 0.93, "Progressive": 1.07},
    "아바나": {"Conservative": 0.84, "Progressive": 1.16},
    "솔바": {"Conservative": 0.90, "Progressive": 1.10},
    "미바나": {"Conservative": 0.85, "Progressive": 1.15},
    "에디아다": {"Conservative": 0.94, "Progressive": 1.06},
    "리에다": {"Conservative": 0.86, "Progressive": 1.14},

    # 미치바 주 (행정 수도, 중앙 지역, 교육 중심)
    "메고이오": {"Conservative": 0.81, "Progressive": 1.19},
    "우프레나": {"Conservative": 0.92, "Progressive": 1.08},
    "미츠비": {"Conservative": 0.80, "Progressive": 1.20},
    "알고": {"Conservative": 0.84, "Progressive": 1.16},
    "산시아고": {"Conservative": 0.91, "Progressive": 1.09},
    "나릴로": {"Conservative": 0.83, "Progressive": 1.17},
    "유프란": {"Conservative": 0.92, "Progressive": 1.08},
    "미치바": {"Conservative": 0.85, "Progressive": 1.15},

    # 바니카-메고차 주 (산맥 지역, 관광 중심, 낙후)
    "바니아": {"Conservative": 1.21, "Progressive": 0.79},
    "미에고": {"Conservative": 1.13, "Progressive": 0.87},
    "메고리": {"Conservative": 1.22, "Progressive": 0.78},
    "민고": {"Conservative": 1.14, "Progressive": 0.86},
    "이벤토": {"Conservative": 1.20, "Progressive": 0.80},
    "마링고": {"Conservative": 1.11, "Progressive": 0.89},

    # 베고차 주 (산업 중심, 중공업)
    "모베이": {"Conservative": 1.02, "Progressive": 0.98},
    "트롱페이": {"Conservative": 1.11, "Progressive": 0.89},
    "바티아": {"Conservative": 0.91, "Progressive": 1.09},
    "이베이": {"Conservative": 1.03, "Progressive": 0.97},
    "페린": {"Conservative": 1.12, "Progressive": 0.88},
    "리안토": {"Conservative": 0.93, "Progressive": 1.07},
    "오고소": {"Conservative": 1.04, "Progressive": 0.96},
    "민마": {"Conservative": 1.10, "Progressive": 0.90},
    "테안타": {"Conservative": 0.92, "Progressive": 1.08},
    "모반토": {"Conservative": 1.05, "Progressive": 0.95},
    "레링가": {"Conservative": 1.09, "Progressive": 0.91},

    # 세그레차 주 (농업 중심, 산맥 지역, 낙후)
    "하롱골": {"Conservative": 1.22, "Progressive": 0.78},
    "미골": {"Conservative": 1.13, "Progressive": 0.87},
    "메링골": {"Conservative": 1.21, "Progressive": 0.79},
    "세골": {"Conservative": 1.12, "Progressive": 0.88},
    "키골": {"Conservative": 1.20, "Progressive": 0.80},
    "리에골": {"Conservative": 1.11, "Progressive": 0.89},
    "페아골": {"Conservative": 1.23, "Progressive": 0.77},
    "베아골": {"Conservative": 1.14, "Progressive": 0.86},

    # 안텐시 주 (산맥 지역, 교통 요지, 경공업)
    "모호보드": {"Conservative": 0.91, "Progressive": 1.09},
    "아핀고": {"Conservative": 0.82, "Progressive": 1.18},
    "비에노": {"Conservative": 0.93, "Progressive": 1.07},
    "시세디": {"Conservative": 0.84, "Progressive": 1.16},
    "메즈노": {"Conservative": 0.89, "Progressive": 1.11},
    "아신가": {"Conservative": 0.83, "Progressive": 1.17},
    "키르가": {"Conservative": 0.92, "Progressive": 1.08},

    # 카리아-로 주 (거대한 섬, 관광, 물류 유통의 중심)
    "노베라니나": {"Conservative": 1.01, "Progressive": 0.99},
    "아르모텐타": {"Conservative": 1.12, "Progressive": 0.88},
    "피고모싱고메고차바데다": {"Conservative": 0.93, "Progressive": 1.07},
    "미베이토메고차피덴타": {"Conservative": 1.04, "Progressive": 0.96},
    "안트로아싱가": {"Conservative": 1.11, "Progressive": 0.89},

    # 테트라 주 (산맥, 트라야비야의 알프스, 관광 중심)
    "아젠타": {"Conservative": 0.92, "Progressive": 1.08},
    "아칸타": {"Conservative": 1.03, "Progressive": 0.97},
    "파르티엔타": {"Conservative": 0.94, "Progressive": 1.06},
    "유칸타": {"Conservative": 1.02, "Progressive": 0.98},
    "테트리다모스": {"Conservative": 0.91, "Progressive": 1.09},
    "테트리비제모스": {"Conservative": 1.04, "Progressive": 0.96},
    "테타": {"Conservative": 0.93, "Progressive": 1.07},

    # 포어 주 (농업 중심 지역)
    "메네트리포어": {"Conservative": 0.92, "Progressive": 1.08},
    "안트리포어": {"Conservative": 1.03, "Progressive": 0.97},
    "라간": {"Conservative": 0.94, "Progressive": 1.06},
    "안파": {"Conservative": 1.02, "Progressive": 0.98},
    "테사": {"Conservative": 0.91, "Progressive": 1.09},
    "아르테": {"Conservative": 1.04, "Progressive": 0.96},
    "세가": {"Conservative": 0.93, "Progressive": 1.07},
    "오르도기": {"Conservative": 1.01, "Progressive": 0.99},

    # 하파차 주 (1급 행정구, 제 2의 경제 중심, 제조업, 기술 개발)
    "파시벤토": {"Conservative": 0.92, "Progressive": 1.08},
    "오고이모": {"Conservative": 1.03, "Progressive": 0.97},
    "미느리오": {"Conservative": 0.92, "Progressive": 1.08},
    "산세오": {"Conservative": 1.11, "Progressive": 0.89},
    "아스타나": {"Conservative": 0.88, "Progressive": 1.12},
    "티레니오": {"Conservative": 0.94, "Progressive": 1.06},
    "비엥고": {"Conservative": 0.91, "Progressive": 1.09},
    "아린키고": {"Conservative": 1.02, "Progressive": 0.98},
    "하싱고": {"Conservative": 0.93, "Progressive": 1.07},
    "모잉고": {"Conservative": 1.01, "Progressive": 0.99},
    "하르고": {"Conservative": 0.92, "Progressive": 1.08},
}

def calculate_priority(event):
    # 각 요소에 대한 점수와 가중치
    impact_score = event['impact'] * 1.5  # 영향력
    frequency_score = event['frequency'] * 1.2  # 빈도
    importance_score = event['importance']
    
    # 총 점수 계산
    total_score = impact_score + frequency_score + importance_score
    return total_score

def get_priority_event():
    # 가중치에 따라 사건 선택
    events_list = list(events.keys())
    pr = [events[event]['frequency'] for event in events_list]
    return random.choices(events_list, weights=pr)[0]

def calculate_population_density(province_info):
    # 인구 밀도 계산
    density = province_info['인구'] / province_info['면적']
    return density

def calculate_party_preference_index(province_info_row):
    # 주 및 행정구역에 따른 개인 선호 정당 지수 계산
    state = province_info_row['주']
    district = province_info_row['행정구역']

    # 각 주와 행정구역에 대한 정치적 성향을 기반으로 선호 지수 설정
    preference_index = {
        'Conservative': 1.0,
        'Progressive': 1.0,
    }

    # 주에 대한 선호 지수 반영
    if state in party_preference_map:
        for party, impact in party_preference_map[state].items():
            preference_index[party] *= impact

    # 행정구역에 대한 선호 지수 반영
    if district in party_preference_map:
        for party, impact in party_preference_map[district].items():
            preference_index[party] *= impact

    return preference_index  # 각 정당에 대한 상대적 선호 지수


def calculate_indexes(province_info):
    # 도시지수 계산 (인구밀도가 높은 경우 도시지수가 높다고 가정)
    province_info['도시지수'] = province_info['인구밀도'] / province_info['인구밀도'].max() * 100

    # 주별로 경제지수를 계산 (주별 인구와 면적을 고려한 단순 경제지수 가정)
    economic_indexes = province_info.groupby('주').apply(
        lambda x: (x['인구'].sum() / x['면적'].sum()) / (province_info['인구'].sum() / province_info['면적'].sum()) * 100
    ).reset_index(name='경제지수')
    
    province_info = province_info.merge(economic_indexes, on='주')
        
    # 주 지수 계산 (예시: 주별 인구 밀도 평균)
    province_info['주지수'] = province_info.groupby('주')['인구밀도'].transform('mean')
    
    # 행정구역 지수 계산 (예시: 행정구역별 인구 밀도 평균)
    province_info['행정구역지수'] = province_info.groupby('행정구역')['인구밀도'].transform('mean')
    
    return province_info

def logistic_function(x, L=2, k=0.05, x0=50):
    # 로지스틱 함수: x가 증가할수록 0과 L 사이의 값을 반환 (k는 기울기 조절)
    exponent = -k * (x - x0)
    if exponent > 700: exponent = 700  # 너무 큰 값이면 최댓값으로 고정
    elif exponent < -700: exponent = -700 # 너무 작은 값이면 최솟값으로 고정
    return 0.1 + (L - 0.1) / (1 + math.exp(exponent))


def adjust_alignment_with_indexes(vote_shares, province_info_row, event):
    # 주별 도시 및 경제 지수를 기반으로 정당별 투표율 조정
    city_index = province_info_row['도시지수']
    economic_index = province_info_row['경제지수']
    # 개인 선호 정당 지수를 추가
    party_preference_index = calculate_party_preference_index(province_info_row)

    # 정치 성향에 따라 지수 영향을 반영 (로지스틱 함수로 조정)
    # L: 최대 투표율, k: 기울기, x0: 기준값, city_index: 도시지수, economic_index: 경제지수
    # 진보적 정당은 도시지수가 높을수록, 보수적 정당은 경제지수가 높을수록 투표율이 높아짐

    alignment_impact = {
        'Progressive': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Conservative': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Centrist': logistic_function(city_index, L=1.5, k=0.04, x0=50) * logistic_function(economic_index, L=1.5, k=0.04, x0=50),
        'Left': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Right': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Big Tent': logistic_function(city_index, L=1.5, k=0.04, x0=50) * logistic_function(economic_index, L=1.5, k=0.04, x0=50),
        'Social Democracy': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Technocratic': logistic_function(city_index, L=1.5, k=0.04, x0=50) * logistic_function(economic_index, L=1.5, k=0.04, x0=50),
        'Nationalism': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Populism': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Environmentalism': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Liberalism': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Agrarian': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Protectionist': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Social Justice': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Pacifist': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Industrialist': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Labor-rights': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Autonomist': logistic_function(city_index, L=2.0, k=0.05, x0=50) * logistic_function(economic_index, L=1.0, k=0.03, x0=50),
        'Traditionalist': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Religious': logistic_function(city_index, L=1.0, k=0.03, x0=50) * logistic_function(economic_index, L=2.0, k=0.05, x0=50),
        'Economic-development': logistic_function(city_index, L=1.5, k=0.04, x0=50) * logistic_function(economic_index, L=1.5, k=0.04, x0=50),
    }

    # 기존 계산된 정당별 투표율에 정치 성향 및 개인 선호 지수 반영
    for party in vote_shares.keys():
        for ideology in alignments:
            if ideology in major_parties.get(party, []) or ideology in medium_parties.get(party, []) or ideology in minor_parties.get(party, []):
                impact = alignment_impact.get(ideology, 1.0) * party_preference_index.get(party, 1.0)  # 개인 선호 지수 곱하기
                vote_shares[party] *= impact

    return vote_shares

def calculate_vote_shares(event, state, row):
    # 기본 투표율 계산
    regional_party_found = False  # 지역 정당 존재 여부 확인
    relevant_regional_parties = {}  # 해당 주의 지역 정당만 포함

    for party, party_state in regional_parties.items():
        if party_state['region'].find(',') != -1:  # 여러 지역에 걸쳐 있는 경우
            regions = party_state['region'].split(', ')
            formatted_state = state.strip().lower()
            if any((region.strip() + " 주").lower() == formatted_state for region in regions):
                regional_party_found = True
                relevant_regional_parties[party] = party_state
        else:
            formatted_party_state = (party_state['region'] + " 주").strip().lower()
            formatted_state = state.strip().lower()
            if formatted_party_state == formatted_state:
                regional_party_found = True
                relevant_regional_parties[party] = party_state

    if regional_party_found: # 지역 정당이 있는 경우
        while True:
            ma, me, mi, reg = random.uniform(40.0, 60.0), random.uniform(20.0, 30.0), random.uniform(10.0, 20.0), random.uniform(0.0, 10.0)
            if 90 <= ma + me + mi + reg <= 110: break
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(0, me) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))]
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))]
    else: # 지역 정당이 없는 경우
        while True:
            ma, me, mi, reg = random.uniform(40.0, 60.0), random.uniform(20.0, 30.0), random.uniform(0.0, 20.0), 0.0
            if 90 <= ma + me + mi + reg <= 110: break
        major_votes = [random.uniform(0, ma) for _ in range(len(major_parties))]
        medium_votes = [random.uniform(0, ma) for _ in range(len(medium_parties))]
        minor_votes = [random.uniform(0, mi) for _ in range(len(minor_parties))]
        reg_votes = [random.uniform(0, reg) for _ in range(len(relevant_regional_parties))]

    # 정당별 투표율 할당
    vote_shares = {}

    # 대형 정당, 중형 정당, 소수 정당, 지역 정당 순으로 반복
    all_parties = [
        (major_parties, major_votes),
        (medium_parties, medium_votes),
        (minor_parties, minor_votes),
        (relevant_regional_parties, reg_votes)
    ]
    
    for parties, votes in all_parties: # 대형 정당, 중형 정당, 소수 정당, 지역 정당 순으로 반복
        for i, party in enumerate(parties.keys()):
            party_impact = sum(event_impact.get(event, {}).get(ideology, 1.0) for ideology in parties[party]) / len(parties[party])
            vote_shares[party] = round(votes[i] * party_impact, 3)

    # 투표율 계산 후 정당 성향 및 도시/경제 지수 반영
    vote_shares = adjust_alignment_with_indexes(vote_shares, row, event)

    # 투표율이 95% 미만인 경우 조정
    total_votes = sum(vote_shares.values())
    while total_votes < random.uniform(95, 98):
        for party in vote_shares.keys():
            vote_shares[party] *= 1.001
        total_votes = sum(vote_shares.values())

    # 투표율이 100%가 넘는 경우 조정
    total_votes = sum(vote_shares.values())
    while total_votes > random.uniform(95, 98):
        for party in vote_shares.keys():
            vote_shares[party] /= 1.001
        total_votes = sum(vote_shares.values())

    return vote_shares

def process_data_with_indexes(province_info):
    # 먼저 도시지수와 경제지수를 계산하여 추가
    province_info = calculate_indexes(province_info) # 도시지수, 경제지수, 주지수, 행정구역지수 추가
    data = [] # 결과 데이터를 저장할 리스트
    global_event = get_priority_event() # 전국적 사건 선택
    global_sub_event = random.choices(events[global_event]['subtypes']) # 전국적 사건의 세부 사건 선택
    
    for state, cities in province_info.groupby('주'):
        local_event = get_priority_event() # 주 단위 사건 선택
        local_sub_event = random.choices(events[local_event]['subtypes']) # 주 단위 사건의 세부 사건 선택

        # 우선 순위에 따라 사건 선택
        if calculate_priority(events[local_event]) > calculate_priority(events[global_event]):
            local_event, local_sub_event = global_event, global_sub_event
        # 사건이 같고 세부 사건이 다른 경우
        if local_event == global_event: local_sub_event = global_sub_event # 세부 사건을 동일하게 설정
        for _, row in cities.iterrows(): # 주별 행정구역별로 반복
            result_row = {
                '주': state,
                '행정구역': row['행정구역'],
                '면적': row['면적'],
                '인구': row['인구'],
                '인구밀도': row['인구밀도'],
                '사건': local_event + ' - ' + local_sub_event[0],
                '도시지수': row['도시지수'],  # 계산된 도시지수 추가
                '경제지수': row['경제지수']   # 계산된 경제지수 추가
            }

            # 투표율 계산 및 조정
            vote_shares = calculate_vote_shares(local_event, state, row)  # row 인자 추가
            result_row.update(vote_shares)
            
            # 무효표
            result_row['무효표'] = 100 - sum(vote_shares.values())
            
            # 총합 계산
            total = sum(vote_shares.values()) + result_row['무효표']
            result_row['총합'] = round(total, 3)
            
            data.append(result_row)
    
    return data

def read_province_info(file_path):
    # 파일에서 주별 정보 읽기
    try:
        province_info = pd.read_csv(file_path, sep=',', names=['행정구역', '주', '면적', '인구'])
        province_info['인구밀도'] = province_info['인구'] / province_info['면적']
        return province_info
    except Exception as e: # 파일 읽기 오류 처리
        print(f"Error reading file: {e}")
        return None

def main():
    province_info = read_province_info('data/province_info.txt')
    province_info['주'] = province_info['주'].str.strip() # 주 이름 공백 제거

    if province_info is not None:
        data = process_data_with_indexes(province_info)
        df = pd.DataFrame(data)
        
        # 열 순서 정리
        columns_order = ['주', '행정구역', '면적', '인구', '인구밀도', '도시지수', '경제지수', '사건'] + \
                       list(major_parties.keys()) + list(medium_parties.keys()) + list(minor_parties.keys()) + \
                       list(regional_parties.keys()) + ['무효표', '총합']
        
        df = df[columns_order]
        df.to_excel('data/election_result.xlsx', index=False)
        print("선거 결과 데이터가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()