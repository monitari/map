document.addEventListener('DOMContentLoaded', function () { // 페이지가 로드되면 실행
    let subdivisions = document.querySelectorAll('.subdivision'); // 모든 지역 요소 가져오기
    let tooltip = document.getElementById('tooltip'); // 툴팁 요소 가져오기
    let populationToggleButton = document.getElementById('population-toggle'); // 인구 토글 버튼 가져오기
    let densityToggleButton = document.getElementById('density-toggle'); // 밀도 토글 버튼 가져오기
    let electionToggleButton = document.getElementById('election-toggle'); // 선거 토글 버튼 가져오기
    let infoBox = document.getElementById('info-box'); // 정보 박스 가져오기
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
        '중앙당': 'rgb(255, 223, 0)',           // 골드 (중도)
        '통합 트라야비야': 'rgb(0, 102, 204)',  // 로열 블루 (보수)
        '사회민주당': 'rgb(255, 182, 193)',     // 라이트 핑크 (진보)
        '자유민주연합': 'rgb(135, 206, 250)',   // 라이트 스카이 블루 (자유주의)
    
        '개혁당': 'rgb(255, 165, 0)',           // 오렌지 (자유주의)
        '국가를 위한 보수당': 'rgb(0, 51, 102)', // 다크 블루 (보수)
        '국민자유전선': 'rgb(210, 105, 30)',     // 초콜릿 (보수-국수주의)
        '민주시민모임': 'rgb(75, 0, 130)',        // 인디고 (중도좌파)
        '녹색당': 'rgb(0, 128, 0)',              // 그린 (환경)
        '새희망당': 'rgb(160, 82, 45)',         // 시에나 (보수-국수주의)
        '시민이 모였다!': 'rgb(240, 230, 140)', // 카키 (시민중심)
        '자유혁신당': 'rgb(255, 99, 71)',       // 토마토 (진보-개혁 성향)
        '진보를 외치다': 'rgb(255, 105, 180)',  // 핫 핑크 (진보)
        '청년당': 'rgb(147, 112, 219)',         // 미디엄 퍼플 (청년중심)
    
        '공산당': 'rgb(255, 0, 0)',             // 레드 (공산주의)
        '과학기술당': 'rgb(64, 224, 208)',      // 터콰이즈 (과학기술)
        '국민행동당': 'rgb(25, 25, 112)',       // 미드나잇 블루 (국수주의)
        '노동자당': 'rgb(255, 69, 0)',          // 오렌지 레드 (노동)
        '보호하자 자연!': 'rgb(0, 128, 128)',   // 틸 (환경)
        '농민당': 'rgb(139, 69, 19)',           // 새들 브라운 (농업)
        '미래당': 'rgb(0, 206, 209)',           // 다크 터콰이즈 (혁신)
        '보호하라!': 'rgb(255, 223, 0)',        // 골드 (보수-반이민)
        '생명당': 'rgb(255, 105, 180)',         // 핫 핑크 (생명권)
        '전사회당': 'rgb(255, 20, 147)',        // 딥 핑크 (사회주의)
        '정의': 'rgb(186, 85, 211)',            // 미디엄 오키드 (사회정의)
        '통일당': 'rgb(255, 140, 0)',           // 다크 오렌지 (통일)
        '특이점이 온다': 'rgb(70, 130, 180)',   // 스틸 블루 (기술관료)
        '평화': 'rgb(144, 238, 144)',           // 라이트 그린 (환경, 평화)
    
        '그미즈리 민주당': 'rgb(100, 149, 237)', // 콘플라워 블루 (그미즈리 지역)
        '도마니 연합': 'rgb(255, 165, 0)',       // 오렌지 (도마니 지역)
        '림덴시를 위하여': 'rgb(255, 99, 71)',   // 토마토 (림덴시 지역)
        '살기좋은 안텐시': 'rgb(0, 255, 127)',   // 스프링 그린 (안텐시 지역)
        '세오어 보호당': 'rgb(205, 92, 92)',     // 인디안 레드 (세오어 지역)
        '테트라 인민당': 'rgb(140, 200, 0)',     // 옐로우 그린 (테트라 지역)
        '하파차의 후예': 'rgb(153, 50, 204)',    // 다크 오키드 (하파차 지역)
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
        else { 
            map.style.transition = 'transform 0s'; // 이동 없음
        }

        // CSS 변환 적용 (translate와 scale을 함께 적용)
        map.style.transformOrigin = '0 0'; // 고정
        map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    });
    
    // 마우스 드래그로 지도 이동
    mapContainer.addEventListener('mousedown', (event) => {
        map.style.transition = 'transform 0s'; // 이동 없음
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

        // 득표율을 비교하여 가장 높은 정당과 두 번째로 높은 득표율 계산
        for (let party in parties) {
            if (parties[party] > maxVote) {
                secondMaxVote = maxVote;
                maxVote = parties[party];
                leadingParty = party;
            } else if (parties[party] > secondMaxVote) secondMaxVote = parties[party];
        }
        // 예외 처리: 정당이 없거나 득표율이 동일한 경우 기본 흰색 반환
        if (!leadingParty || maxVote === secondMaxVote) return 'rgba(255, 255, 255, 0.5)'; // 흰색과 투명도 0.5 기본 값

        const voteGap = maxVote - secondMaxVote; 
        // 투명도 계산: 득표율 차이가 작을수록 낮은 투명도, 득표율 차이가 커야 진해짐
        const opacity = Math.min(1, Math.max(0.3, voteGap / 10)); // 최소 투명도 0.3, 더 큰 갭 필요
        // 정당에 따라 기본 색상 설정, 없으면 흰색
        const baseColor = partyColors[leadingParty] || 'rgb(255, 255, 255)';
        
        // rgba로 변환하고 투명도 적용
        return baseColor.replace('rgb', 'rgba').replace(')', `, ${opacity})`);
    }

    // 1등 정당을 가져오는 함수
    function getLeadingParty(seats) {
        let leadingParty = null;
        let maxSeats = 0;
        for (let party in seats) {
            if (seats[party] > maxSeats) {
                maxSeats = seats[party];
                leadingParty = party;
            }
        }
        return leadingParty;
    }

    // 색상을 적용하는 함수
    function applyColor() {
        subdivisions.forEach(function (subdivision) {
            let population = parseInt(subdivision.getAttribute('data-population'), 10);
            let area = parseFloat(subdivision.getAttribute('data-area')); // 면적 가져오기
            let parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기
            if (populationMode) subdivision.style.fill = getPopulationColor(population); // 인구 모드일 때 색상 적용
            else if (densityMode) subdivision.style.fill = getDensityColor(population, area); // 밀도 모드일 때 색상 적용
            else if (electionMode && showLeadingPartyMode) subdivision.style.fill = partyColors[getLeadingParty(parties)]; // 1등 정당 색상 모드일 때 색상 적용
            else if (electionMode) subdivision.style.fill = getElectionColor(parties); // 선거 모드일 때 색상 적용
            else subdivision.style.fill = '#989898'; // 기본 색상
        });
    }

    // 선거 결과 데이터를 정보 박스에 표시하는 함수
    function displayElectionResults(showDisplay) {
        if (showDisplay) {
            infoBox.style.display = 'block'; // 정보 박스 표시
            const results = {}; // 선거 결과 저장 객체
            let event = ""; // 이벤트 정보 저장
                
            subdivisions.forEach(function (subdivision) {
                const population = parseInt(subdivision.getAttribute('data-population'), 10); // 인구 정보 가져오기
                const events = subdivision.getAttribute('data-events'); // 이벤트 정보 가져오기
                const parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기
                event = events; // 이벤트 정보 저장
    
                // 각 정당의 득표 퍼센테이지 계산
                const totalVotes = Object.values(parties).reduce((a, b) => a + b, 0); // 총 득표수 계산
                const partyPercentages = {};
                for (let party in parties) {
                    partyPercentages[party] = (parties[party] / totalVotes) * 100; // 득표 퍼센테이지 계산
                }

                // 총 인구수 계산
                let totalPopulation = 0;
                subdivisions.forEach(function (subdivision) {
                    totalPopulation += parseInt(subdivision.getAttribute('data-population'), 10);
                });

                // 각 정당의 의석수 계산
                const seats = {};
                for (let party in partyPercentages) {
                    if (partyPercentages[party] >= 3) {
                        const votes = (partyPercentages[party] / 100) * totalVotes; // 정당의 득표수 계산
                        seats[party] = Math.round(votes * population / totalPopulation * 100); // 의석수 계산
                        if (seats[party] === 0) seats[party] = 1; // 의석수가 0인 경우 1로 설정 (최소 1석)
                    }
                }

                // 결과 저장
                results[subdivision.getAttribute('data-name')] = seats;
            });
    
            const partySeats = {}; // 정당별 의석수 저장 객체    
            // 각 행정구역의 정당별 의석수 합산
            for (const province in results) {
                const seats = results[province]; 
                for (let party in seats) {
                    if (partySeats[party]) partySeats[party] += seats[party];
                    else partySeats[party] = seats[party];
                }
            }
    
        // 정보 박스에 선거 결과 표시 (내림차순 정렬)
        let resultHTML = `<h3 style="margin-bottom: 12px;">선거 결과 <span style="font-size: 0.8em;">${event}</span></h3>`;
        const sortedParties = Object.keys(partySeats).sort((a, b) => {
            if (partySeats[b] === partySeats[a]) return a.localeCompare(b); // 개수가 같으면 가나다순으로 정렬
            return partySeats[b] - partySeats[a]; // 내림차순 정렬
        });

        // 총 의석수 계산
        const finaltotalSeats = Object.values(partySeats).reduce((acc, cur) => acc + cur, 0);

        sortedParties.forEach(party => {
            const colorBox = `<span style="display:inline-block;width:10px;height:10px;background-color:${partyColors[party]};margin-right:3px;"></span>`;
            const percentage = ((partySeats[party] / finaltotalSeats) * 100).toFixed(2);
            resultHTML += `
                <div style="display: flex; align-items: center; margin: 3px 0;">
                    <p style="line-height: 1.2; margin: 0; flex-grow: 1;">${colorBox}${party} ${partySeats[party]}석 (${percentage}%)</p>
                    <div style="background-color: ${partyColors[party]}; height: 10px; width: ${percentage}%;"></div>
                </div>`;
        });

        resultHTML += `<p style="font-weight:bold; margin-top: 5px; margin-bottom: 2px; font-size: 1.2em;">총 의석수 | ${finaltotalSeats}석</p>`;
        infoBox.innerHTML = resultHTML;
        } else infoBox.style.display = 'none'; // 정보 박스 숨김
    }

    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    populationToggleButton.addEventListener('click', function () { 
        populationMode = true; // 인구 모드 전환
        displayElectionResults(false); // 선거 결과 끄기
        densityMode = false; // 밀도 모드를 끔
        electionMode = false; // 선거 모드를 끔
        applyColor(); // 색상 적용
        document.getElementById('leading-party-toggle').style.display = 'none'; // 1등 정당 버튼 숨기기
    });
    
    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    densityToggleButton.addEventListener('click', function () {
        densityMode = true; // 밀도 모드 전환
        displayElectionResults(false); // 선거 결과 끄기
        populationMode = false; // 인구 모드를 끔
        electionMode = false; // 선거 모드를 끔
        applyColor(); // 색상 적용
        document.getElementById('leading-party-toggle').style.display = 'none'; // 1등 정당 버튼 숨기기
    });
    
    // 클릭 이벤트 리스너를 추가하여 모드를 전환하는 함수
    electionToggleButton.addEventListener('click', function () {
        electionMode = true; // 선거 모드 전환
        displayElectionResults(true); // 선거 결과 표시
        populationMode = false; // 인구 모드를 끔
        densityMode = false; // 밀도 모드를 끔
        applyColor();
        document.getElementById('leading-party-toggle').style.display = 'block'; // 1등 정당 버튼 표시
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
                        
            function formatNumber(num) { // 숫자를 보기 좋게 포맷팅하는 함수 (억, 만 단위)
                if (num >= 100000000) return (num / 100000000).toFixed(2) + '억';
                else if (num >= 10000) return (num / 10000).toFixed(2) + '만';
                else return num.toString();
            }

            // 정당 정보를 유동적으로 추가
            let partiesHtml = '';
            let otherPartiesHtml = ''; // 3% 미만 정당을 저장할 변수
            
            // 정당을 득표율에 따라 정렬
            let sortedParties = Object.keys(parties).sort((a, b) => parseFloat(parties[b]) - parseFloat(parties[a]));            
            let otherParties = []; // 3% 미만 정당을 저장할 배열
            let counter = 0; // 카운터 추가
            
            // 총 인구수 계산
            let totalPopulation = 0;
            subdivisions.forEach(function (subdivision) {
                totalPopulation += parseInt(subdivision.getAttribute('data-population'), 10);
            });
            
            // 각 정당의 득표 퍼센테이지 계산
            const totalVotes = Object.values(parties).reduce((a, b) => a + b, 0); // 총 득표수 계산
            const partyPercentages = {};
            for (let party in parties) partyPercentages[party] = (parties[party] / totalVotes) * 100; // 득표 퍼센테이지 계산
            
            // 각 정당의 의석수 계산 (득표율이 3% 이상인 경우만)
            const seats = {};
            for (let party in partyPercentages) {
                if (partyPercentages[party] >= 3) {
                    const votes = (partyPercentages[party] / 100) * totalVotes; // 정당의 득표수 계산
                    seats[party] = Math.round(votes * population / totalPopulation * 100); // 의석수 계산
                    if (seats[party] === 0) seats[party] = 1; // 의석수가 0인 경우 1로 설정 (최소 1석)
                }
            }
            
            // 정당별 득표율을 HTML로 변환
            for (let party of sortedParties) {
                let value = parseFloat(parties[party]);
                let color = partyColors[party] || 'rgb(200, 200, 200)'; // 기본 색상 설정
            
                if (isNaN(value)) value = 0;
                if (value < 3.0) otherParties.push({ party, value }); // 3% 미만 정당은 따로 저장
                else {
                    if (counter % 3 === 0) partiesHtml += '<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">';
                    partiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 4px 0 4px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: ${color}; margin-right: 5px; flex-shrink: 0;"></div>
                        ${party}: ${value.toFixed(3)}% (${seats[party]}석)
                    </div>`;
                    if (counter % 3 === 2) partiesHtml += '</div>';
                    counter++;
                }
            }
            if (counter % 3 !== 0) partiesHtml += '</div>'; // 마지막 줄을 닫음
            
            // 기타 정당과 무효표를 회색으로 묶어서 표시
            let invalidVotesPercentage = parseFloat(invalid_votes);
            if (otherParties.length > 0 || invalidVotesPercentage > 0) {
                // 3% 미만 정당 득표율을 합산
                let otherPartiesSum = otherParties.reduce((acc, cur) => acc + cur.value, 0);
                otherPartiesHtml += `
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                    text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px 0 5px; font-size: 12px;">
                            <div style="width: 12px; height: 12px; background-color: rgb(200, 200, 200); margin-right: 5px; flex-shrink: 0;"></div>
                            기타: ${otherPartiesSum.toFixed(3)}% (3% 미만)
                        </div>
                        <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                    text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px 0 5px; font-size: 12px;">
                            <div style="width: 12px; height: 12px; background-color: rgb(0, 0, 0); margin-right: 5px; flex-shrink: 0;"></div>
                            무효표: ${invalidVotesPercentage.toFixed(3)}%
                        </div>
                    </div>`;
            }
                        
            // 최종 HTML 결합
            let finalHtml = partiesHtml + otherPartiesHtml;
            
            // 막대그래프 생성
            let barHtml = '';
            let cumulativePercentage = 0;
            for (let party of sortedParties) {
                let value = parseFloat(parties[party]);
                let color = partyColors[party] || 'rgb(200, 200, 200)'; // 기본 색상 설정
            
                if (isNaN(value)) value = 0;
                if (value >= 3.0) {
                    let width = value; // 득표율을 너비로 사용
                    barHtml += `<div style="background-color: ${color}; height: 20px; width: ${width}%;"></div>`;
                    cumulativePercentage += width;
                }
            }
            
            // 기타 정당 막대 추가
            if (otherParties.length > 0) {
                let otherPartiesSum = otherParties.reduce((acc, cur) => acc + cur.value, 0);
                let width = otherPartiesSum; // 득표율을 너비로 사용
                barHtml += `<div style="background-color: rgb(200, 200, 200); height: 20px; width: ${width}%;"></div>`;
            }
            
            // 무효표 막대 추가
            if (!isNaN(invalidVotesPercentage) && invalidVotesPercentage > 0) {
                let width = invalidVotesPercentage; // 득표율을 너비로 사용
                barHtml += `<div style="background-color: black; height: 20px; width: ${width}%;"></div>`;
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
                        <div style="margin-left: 10px;">${finalHtml}</div>
                        <div style="display: flex; margin-top: 10px; height: 20px; border: 1px solid #ccc;">
                            ${barHtml}
                        </div>
                    </div>
                </div>
            `;

            // 화면 경계를 벗어나지 않도록 조정
            const tooltipRect = tooltip.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            // 툴팁 위치 설정
            let tooltipX = event.pageX;
            let tooltipY = event.pageY + 7;
            if (tooltipX + tooltipRect.width > viewportWidth) tooltipX = viewportWidth - tooltipRect.width;
            if (tooltipY + tooltipRect.height > viewportHeight) tooltipY = viewportHeight - tooltipRect.height;

            tooltip.style.left = tooltipX + 'px';
            tooltip.style.top = tooltipY + 'px';
            
            tooltip.style.display = 'block'; // 툴팁 표시
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