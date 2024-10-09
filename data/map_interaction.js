document.addEventListener('DOMContentLoaded', function () { // 페이지가 로드되면 실행
    let subdivisions = document.querySelectorAll('.subdivision'); // 모든 지역 요소 가져오기
    let tooltip = document.getElementById('tooltip'); // 툴팁 요소 가져오기
    let populationToggleButton = document.getElementById('population-toggle'); // 인구 토글 버튼 가져오기
    let densityToggleButton = document.getElementById('density-toggle'); // 밀도 토글 버튼 가져오기
    let electionToggleButton = document.getElementById('election-toggle'); // 선거 토글 버튼 가져오기
    let showLeadingPartyButton = document.getElementById('show-leading-party'); // 1등 정당 토글 버튼 가져오기
    let populationMode = false; // 인구 모드
    let densityMode = false; // 밀도 모드
    let electionMode = false; // 선거 모드
    let showLeadingPartyMode = false; // 1등 정당 색상 모드
    
    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');
    let scale = 1; // 초기 확대/축소 비율
    let translateX = 0; // 드래그에 따른 x축 이동
    let translateY = 0; // 드래그에 따른 y축 이동
    let isDragging = false; // 드래그 중인지 여부
    let startX, startY; // 드래그 시작 좌표

    // 정당에 따라 색상 매핑
    const partyColors = {
        // 주요 정당
        '자유혁신당': 'rgb(255, 77, 77)',         // 진한 분홍색 (진보-개혁 성향)
        '중앙당': 'rgb(255, 215, 0)',            // 금색 (중도)
        '통합당': 'rgb(65, 105, 225)',            // 로열 블루 (보수)
        '사회민주당': 'rgb(255, 107, 107)',        // 연한 빨간색 (사회민주주의)
        '진보당': 'rgb(255, 20, 147)',            // 딥 핑크 (진보)
        '보수당': 'rgb(0, 0, 128)',            // 네이비 블루 (보수)
    
        // 소수 정당
        '개혁당': 'rgb(255, 160, 122)',            // 연한 샐몬색 (자유주의)
        '민주통합당': 'rgb(255, 105, 180)',        // 핫 핑크 (중도좌파)
        '미래연합': 'rgb(70, 130, 180)',          // 스틸 블루 (기술관료)
        '평화당': 'rgb(152, 251, 152)',            // 연한 초록색 (환경, 평화)
        '시민당': 'rgb(240, 230, 140)',            // 카키 (시민중심)
        '녹색당': 'rgb(34, 139, 34)',            // 포레스트 그린 (환경)
        '노동당': 'rgb(205, 92, 92)',            // 인디안 레드 (사회주의)
        '국민당': 'rgb(25, 25, 112)',            // 미드나잇 블루 (국수주의)
        '정의당': 'rgb(218, 112, 214)',            // 오키드 (사회정의)
        '미래당': 'rgb(0, 206, 209)',            // 다크 터콰이즈 (혁신)
        '자유민주연합': 'rgb(135, 206, 235)',      // 하늘색 (자유주의)
        '청년당': 'rgb(147, 112, 219)',            // 보라색 (청년중심)
        '농민당': 'rgb(139, 69, 19)',            // 새들 브라운 (농업)
        '평화통일당': 'rgb(144, 238, 144)',        // 라이트 그린 (평화)
        '과학기술당': 'rgb(64, 224, 208)',        // 터콰이즈 (과학기술)
    
        // 지역 정당
        '그미즈리 민주당': 'rgb(135, 206, 235)',    // 하늘색 (그미즈리 지역)
        '하파차 인민당': 'rgb(153, 50, 204)',      // 보라색 (하파차 지역)
        '도마니 연합': 'rgb(255, 165, 0)',         // 오렌지 (도마니 지역)
        '테트라 인민당': 'rgb(139, 69, 19)'       // 갈색 (테트라 지역)
    };
    // 마우스 휠로 확대/축소
    mapContainer.addEventListener('wheel', (event) => {
        event.preventDefault();
    
        const rect = mapContainer.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;
    
        const delta = event.deltaY > 0 ? -0.2 : 0.2; // 마우스 휠 방향에 따라 확대/축소 비율 결정
        const newScale = Math.min(Math.max(1, scale + delta), 5); // 최소 1배, 최대 5배로 제한
        
        // 확대/축소 비율에 따른 중심점 조정 (기존 좌표계를 기준으로 재조정)
        const ratio = newScale / scale;
        const newOriginX = (offsetX - translateX) * (1 - ratio);
        const newOriginY = (offsetY - translateY) * (1 - ratio);
    
        // translate 값에 새 origin 좌표 반영
        translateX += newOriginX;
        translateY += newOriginY;
    
        scale = newScale;

        // 1배일때 원래위치로 돌아가기
        if (scale === 1) {
            map.style.transition = 'transform 0.3s ease-out'; // 부드럽게 이동
            translateX = 0;
            translateY = 0;
        }
        else map.style.transition = 'transform 0s'; // 이동 없음

        // CSS 변환 적용 (translate와 scale을 함께 적용)
        map.style.transformOrigin = '0 0'; // 고정
        map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    });
    
    // 마우스 드래그로 지도 이동
    mapContainer.addEventListener('mousedown', (event) => {
        if (event.button === 0) { // 왼쪽 버튼
            isDragging = true;
            startX = event.clientX;
            startY = event.clientY;
        }
    });
    
    // 드래그 중일 때 이동
    mapContainer.addEventListener('mousemove', (event) => {
        if (isDragging) {
            const dx = event.clientX - startX;
            const dy = event.clientY - startY;
    
            translateX += dx;
            translateY += dy;
    
            map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    
            startX = event.clientX;
            startY = event.clientY;
        }
    });
    
    // 드래그 종료
    mapContainer.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
    // 드래그 종료
    mapContainer.addEventListener('mouseleave', () => {
        isDragging = false;
    });    
    
    // 인구에 따라 색상을 설정하는 함수
    function getPopulationColor(population) {
        let minPop = 100000;  // 최소 인구
        let maxPop = 10000000; // 최대 인구
        let normalized = (parseInt(population) - minPop) / (maxPop - minPop); // 정규화
        let greenBlueIntensity = Math.floor(255 * (1 - normalized));  // 녹색과 청색 강도
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정
    }

    // 인구 밀도에 따라 색상을 설정하는 함수
    function getDensityColor(population, area) {
        let density = population / area; // 인구 밀도 계산
        let minDensity = 1; // 최소 밀도
        let maxDensity = 1000; // 최대 밀도
        let normalized = (density - minDensity) / (maxDensity - minDensity); // 정규화
        let greenBlueIntensity = Math.floor(255 * (1 - normalized)); // 녹색과 청색 강도
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정
    }

    // 정당 득표율에 따라 색상을 설정하는 함수
    function getElectionColor(parties) {
        let maxVote = 0;
        let secondMaxVote = 0;
        let leadingParty = '';
        for (let party in parties) {
            if (parties[party] > maxVote) {
                secondMaxVote = maxVote;
                maxVote = parties[party];
                leadingParty = party;
            } else if (parties[party] > secondMaxVote) {
                secondMaxVote = parties[party];
            }
        }
        const voteGap = maxVote - secondMaxVote;
        const opacity = Math.min(1, voteGap / 10); // 득표율 차이에 따라 투명도 설정 (최대 1)
        const baseColor = partyColors[leadingParty] || 'rgb(255, 255, 255)'; // 기본 흰색
        return baseColor.replace('rgb', 'rgba').replace(')', `, ${opacity})`); // 투명도 적용
    }

    // 1등 정당의 색상만 적용하는 함수
    function getLeadingPartyColor(parties) {
        let maxVote = 0;
        let leadingParty = '';
        for (let party in parties) {
            if (parties[party] > maxVote) {
                maxVote = parties[party];
                leadingParty = party;
            }
        }
        return partyColors[leadingParty]; // 1등 정당 색상 반환
    }

    // 색상을 적용하는 함수
    function applyColor() {
        subdivisions.forEach(function (subdivision) {
            let population = parseInt(subdivision.getAttribute('data-population'), 10);
            let area = parseFloat(subdivision.getAttribute('data-area')); // 면적 가져오기
            let parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기
            if (populationMode) subdivision.style.fill = getPopulationColor(population); // 인구 모드일 때 색상 적용
            else if (densityMode) subdivision.style.fill = getDensityColor(population, area); // 밀도 모드일 때 색상 적용
            else if (electionMode && showLeadingPartyMode) subdivision.style.fill = getLeadingPartyColor(parties); // 1등 정당 모드일 때 색상 적용
            else if (electionMode) subdivision.style.fill = getElectionColor(parties); // 선거 모드일 때 색상 적용
            else subdivision.style.fill = '#989898'; // 기본 색상
        });
    }

    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    populationToggleButton.addEventListener('click', function () { 
        populationMode = !populationMode; // 인구 모드 전환
        densityMode = false; // 밀도 모드를 끔
        applyColor(); // 색상 적용
    });

    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    densityToggleButton.addEventListener('click', function () {
        densityMode = !densityMode; // 밀도 모드 전환 
        populationMode = false; // 인구 모드를 끔
        applyColor(); // 색상 적용
    });

    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    electionToggleButton.addEventListener('click', function () {
        electionMode = !electionMode;
        populationMode = false; // 인구 모드를 끔
        densityMode = false; // 밀도 모드를 끔
        applyColor();
    });

    // "선거 결과" 버튼 클릭 시 "1등 정당" 버튼 표시/숨김
    document.getElementById('election-toggle').addEventListener('click', function() {
        const leadingPartyButton = document.getElementById('leading-party-toggle');
        if (leadingPartyButton.style.display === 'none' || leadingPartyButton.style.display === '')
            leadingPartyButton.style.display = 'block';
        else leadingPartyButton.style.display = 'none';
    });
    // "1등 정당" 버튼 클릭 시 1등 정당 색상 모드 전환
    document.getElementById('leading-party-toggle').addEventListener('click', function () {
        showLeadingPartyMode = !showLeadingPartyMode; // 1등 정당 색상 모드 전환
        applyColor(); // 색상 적용
    });
    
    // 툴팁을 표시하고 색상을 변경하는 이벤트 리스너
    subdivisions.forEach(function (subdivision) {
        subdivision.addEventListener('mouseenter', function (event) {
            let name = subdivision.getAttribute('data-name'); // 이름 가져오기
            let area = subdivision.getAttribute('data-area'); // 면적 가져오기
            let population = subdivision.getAttribute('data-population'); // 인구 가져오기
            let state = subdivision.getAttribute('data-state'); // 속한 주의 이름 가져오기
            let rank_area = subdivision.getAttribute('data-rank-area'); // 면적 순위 가져오기
            let rank_population = subdivision.getAttribute('data-rank-population'); // 인구 순위 가져오기
            let rank_density = subdivision.getAttribute('data-rank-density'); // 밀도 순위 가져오기
            let province_cnt = subdivision.getAttribute('data-all-province'); // 전체 지역 수 
            let events = subdivision.getAttribute('data-events'); // 이벤트 정보 가져오기
            let parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기
            let invalid_votes = subdivision.getAttribute('data-invalid-votes'); // 무효표 가져오기
            let total_votes = subdivision.getAttribute('data-total-votes'); // 총합 득표율 가져오기
            
            function formatNumber(num) { // 숫자를 보기 좋게 포맷팅하는 함수 (억, 만 단위)
                if (num >= 100000000) return (num / 100000000).toFixed(2) + '억';
                else if (num >= 10000) return (num / 10000).toFixed(2) + '만';
                else return num.toString();
            }

            // 정당 정보를 유동적으로 추가
            let partiesHtml = '';
            let otherPartiesHtml = ''; // 5% 미만 정당을 저장할 변수
            
            // 정당을 득표율에 따라 정렬
            let sortedParties = Object.keys(parties).sort((a, b) => parseFloat(parties[b]) - parseFloat(parties[a]));
            
            let otherParties = [];
            for (let party of sortedParties) {
                let value = parseFloat(parties[party]);
                let color = partyColors[party] || 'rgb(200, 200, 200)'; // 기본 색상 설정
                
                if (isNaN(value)) value = 0;
                if (value < 5.0) otherParties.push(`${party}: ${value.toFixed(3)}%`);
                else {
                    partiesHtml += `
                        <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 5px;">
                            <div style="width: 12px; height: 12px; background-color: ${color}; margin-right: 5px;"></div>
                            ${party}: ${value.toFixed(3)}%
                        </div>`;
                }
            }
            
            // 기타 정당을 회색으로 묶어서 표시
            if (otherParties.length > 0) {
                // 5% 미만 정당 득표율을 합산
                let otherPartiesSum = otherParties.reduce((acc, cur) => acc + parseFloat(cur.split(': ')[1]), 0);
                otherPartiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 5px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(200, 200, 200); margin-right: 5px;"></div>
                        기타: ${otherPartiesSum.toFixed(3)}% (5% 미만)
                    </div>`;
            }
            
            // 최종 HTML 결합
            let finalHtml = partiesHtml + otherPartiesHtml;

            // 기타 정당 추가
            if (otherPartiesHtml) {
                partiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 5px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(200, 200, 200); margin-right: 5px;"></div>
                        기타: 
                    </div>` + otherPartiesHtml;
            }

            tooltip.innerHTML = `
                <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 5px;">
                    ${name} <span style="font-size: 0.6em; color: gray;">${state}</span>
                </div>
                <div style="font-size: 1em;">
                    <div>면적 | ${formatNumber(area)}A <span style="font-size: 0.8em; color: gray; 
                    margin-left: 5px;">(${rank_area} / ${province_cnt}위)</span></div>
                    <div>인구 | ${formatNumber(population)}명 <span style="font-size: 0.8em; color: gray; 
                    margin-left: 5px;">(${rank_population} / ${province_cnt}위)</span></div>
                    <div>인구 밀도 | ${(population / area).toFixed(3)}명/A <span style="font-size: 0.8em; color: gray; 
                    margin-left: 5px;">(${rank_density} / ${province_cnt}위)</span></div>
                    <div style="font-size: 0.8em; color: gray; margin-top: 5px;">
                        <div style = "margin-top: 5px;"> 사건 | <span style="font-weight: bold;">${events}</span></div>
                        <div style = "margin-top: 5px;"> 정당 득표율 | </div>
                        <div style="margin-left: 10px;">${finalHtml}</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                            <div style="flex: 1; min-width: 20%;">무효표: ${parseFloat(invalid_votes).toFixed(3)}%</div>
                            <div style="flex: 1; min-width: 20%;">총합: ${parseFloat(total_votes).toFixed(3)}%</div>
                        </div>
                    </div>
                </div>
            `;

            tooltip.style.display = 'block'; // 툴팁 표시
            tooltip.style.left = event.pageX + 'px'; // 툴팁 위치 설정
            tooltip.style.top = (event.pageY + 7) + 'px'; // 툴팁 위치 설정
            subdivision.style.stroke = 'yellow'; // 노란색 테두리
            subdivision.style.strokeWidth = '5px'; // 테두리 두께
        });
    
        // 마우스 이동 이벤트 리스너를 추가하여 툴팁을 따라다니게 함
        subdivision.addEventListener('mousemove', function (event) {
            let tooltipWidth = tooltip.offsetWidth;
            let tooltipHeight = tooltip.offsetHeight;
            let pageWidth = window.innerWidth;
            let pageHeight = window.innerHeight;
            
            let x = event.pageX;
            let y = event.pageY + 10;
        
            // 화면 밖으로 나가지 않도록 경계 조건 추가
            if (x + tooltipWidth > pageWidth) x = pageWidth - tooltipWidth;
            if (y + tooltipHeight > pageHeight) y = pageHeight - tooltipHeight;
        
            tooltip.style.left = x + 'px';
            tooltip.style.top = y + 'px';
        });        
    
        // 마우스 떠남 이벤트 리스너를 추가하여 툴팁을 숨기고 색상을 초기화함
        subdivision.addEventListener('mouseleave', function () {
            tooltip.style.display = 'none';
            subdivision.style.stroke = 'none';
            applyColor(); // 색상 초기화
        });
    });

    applyColor(); // 색상 초기화
});