// map_interactions.js

export function initializeMapInteractions(mapContainer, map) { // 지도 상호작용 초기화
    const MIN_SCALE = 1; // 최소 확대 배율
    const MAX_SCALE = 5; // 최대 확대 배율
    const SCALE_STEP = 0.2; // 확대 배율 증감량
    const TRANSITION_DURATION = '0.1s'; // 변환 효과 지속 시간
    const NO_TRANSITION = '0s'; // 변환 효과 없음

    let scale = MIN_SCALE; // 확대 배율
    let translateX = 0; // X축 이동 거리
    let translateY = 0; // Y축 이동 거리
    let isDragging = false; // 드래그 여부
    let startX, startY; // 드래그 시작 지점

    function applyTransform() { // 변환 적용
        map.style.transformOrigin = '0 0'; // 변환 기준점
        map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    function handleWheel(event) { // 마우스 휠 이벤트 처리
        event.preventDefault(); // 기본 동작 방지

        const rect = mapContainer.getBoundingClientRect(); // 지도 컨테이너의 위치 및 크기
        const offsetX = event.clientX - rect.left; // X축 위치
        const offsetY = event.clientY - rect.top; // Y축 위치

        const delta = event.deltaY > 0 ? -SCALE_STEP : SCALE_STEP; // 확대 배율 증감량
        const newScale = Math.min(Math.max(MIN_SCALE, scale + delta), MAX_SCALE); // 새로운 확대 배율

        const ratio = newScale / scale; // 확대 배율 비율
        const newOriginX = (offsetX - translateX) * (1 - ratio); // X축 변환 기준점
        const newOriginY = (offsetY - translateY) * (1 - ratio); // Y축 변환 기준점

        translateX += newOriginX;
        translateY += newOriginY; // 변환 기준점 적용
        scale = newScale; // 확대 배율 적용

        map.style.transition = scale === MIN_SCALE ? `transform ${TRANSITION_DURATION} ease-out` : 
            `transform ${NO_TRANSITION}`; // 변환 효과 적용(최소 확대 배율일 경우 효과 적용)
        if (scale === MIN_SCALE) { // 최소 확대 배율일 경우 초기화
            translateX = 0;
            translateY = 0;
        }

        applyTransform(); // 변환 적용
    }

    function handleMouseDown(event) { // 마우스 다운 이벤트 처리
        if (event.button === 0) { // 마우스 왼쪽 버튼 클릭 시
            isDragging = true; // 드래그 상태로 설정
            startX = event.clientX; 
            startY = event.clientY;
            map.style.transition = `transform ${TRANSITION_DURATION} ease-out`;
        }
    }

    function handleMouseMove(event) { // 마우스 이동 이벤트 처리
        if (isDragging) { // 드래그 중일 경우
            const dx = event.clientX - startX; // X축 이동 거리
            const dy = event.clientY - startY; // Y축 이동 거리

            translateX += dx;
            translateY += dy;
            applyTransform(); // 변환 적용

            startX = event.clientX;
            startY = event.clientY;
        }
    }

    function handleMouseUpOrLeave() { // 마우스 업 또는 벗어남 이벤트 처리
        isDragging = false; // 드래그 상태 해제
    }

    mapContainer.addEventListener('wheel', handleWheel); // 마우스 휠 이벤트
    mapContainer.addEventListener('mousedown', handleMouseDown); // 마우스 다운 이벤트
    mapContainer.addEventListener('mousemove', handleMouseMove); // 마우스 이동 이벤트
    mapContainer.addEventListener('mouseup', handleMouseUpOrLeave); // 마우스 업 이벤트
    mapContainer.addEventListener('mouseleave', handleMouseUpOrLeave); // 마우스 벗어남 이벤트
}