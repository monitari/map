document.addEventListener('DOMContentLoaded', function () { // 페이지가 로드되면 실행
    let subdivisions = document.querySelectorAll('.subdivision'); // 모든 지역 요소 가져오기
    let tooltip = document.getElementById('tooltip'); // 툴팁 요소 가져오기
    let populationToggleButton = document.getElementById('population-toggle'); // 인구 토글 버튼 가져오기
    let densityToggleButton = document.getElementById('density-toggle'); // 밀도 토글 버튼 가져오기
    let populationMode = false; // 인구 모드
    let densityMode = false; // 밀도 모드
    
    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');
    let scale = 1; // 초기 확대/축소 비율
    let originX = 0; // 확대/축소 중심점
    let originY = 0; // 확대/축소 중심점
    let translateX = 0; // 드래그에 따른 x축 이동
    let translateY = 0; // 드래그에 따른 y축 이동
    let isDragging = false; // 드래그 중인지 여부
    let startX, startY; // 드래그 시작 좌표
    
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
    
    mapContainer.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
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
    }``

    // 인구 밀도에 따라 색상을 설정하는 함수
    function getDensityColor(population, area) {
        let density = population / area; // 인구 밀도 계산
        let minDensity = 1; // 최소 밀도
        let maxDensity = 1000; // 최대 밀도
        let normalized = (density - minDensity) / (maxDensity - minDensity); // 정규화
        let greenBlueIntensity = Math.floor(255 * (1 - normalized)); // 녹색과 청색 강도
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정
    }

    // 색상을 적용하는 함수
    function applyColor() {
        subdivisions.forEach(function (subdivision) {
            let population = parseInt(subdivision.getAttribute('data-population'), 10);
            let area = parseFloat(subdivision.getAttribute('data-area')); // 면적 가져오기
            if (populationMode) subdivision.style.fill = getPopulationColor(population); // 인구 모드일 때 색상 적용
            else if (densityMode) subdivision.style.fill = getDensityColor(population, area); // 밀도 모드일 때 색상 적용
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
            let province_cnt = subdivision.getAttribute('data-all-province'); // 전체 지역 수 가져오기
    
            function formatNumber(num) { // 숫자를 보기 좋게 포맷팅하는 함수 (억, 만 단위)
                if (num >= 100000000) return (num / 100000000).toFixed(2) + '억';
                else if (num >= 10000) return (num / 10000).toFixed(2) + '만';
                else return num.toString();
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
                    <div>인구 밀도 | ${(population / area).toFixed(2)}명/A <span style="font-size: 0.8em; color: gray; 
                    margin-left: 5px;">(${rank_density} / ${province_cnt}위)</span></div>
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
