// map_interactions.js

export function initializeMapInteractions(mapContainer, map) {
    const MIN_SCALE = 1;
    const MAX_SCALE = 10;
    const SCALE_STEP = 0.3;
    const TRANSITION_DURATION = '0.1s';
    const NO_TRANSITION = '0s';

    let scale = MIN_SCALE;
    let translateX = 0;
    let translateY = 0;
    let isDragging = false;
    let startX, startY;
    let isTransforming = false;

    const scaleBarInner = document.getElementById('scale-bar-inner');
    const scaleText = document.getElementById('scale-text');

    function updateScaleBar() {
        const scaleLength = Math.max(6, 400 / scale); // 최소 길이를 6으로 설정
        scaleBarInner.style.width = `${scaleLength * 100 / 400}%`; // 400을 기준으로 퍼센트 계산
        scaleText.textContent = `${Math.round(scaleLength)} B`;
    }

    function applyTransform() {
        if (!isTransforming) {
            isTransforming = true;
            requestAnimationFrame(() => {
                map.style.transformOrigin = '0 0';
                map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                updateScaleBar(); // 스케일 바 업데이트
                isTransforming = false;
            });
        }
    }

    function handleWheel(event) {
        event.preventDefault();

        const rect = mapContainer.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;

        const delta = event.deltaY > 0 ? -SCALE_STEP : SCALE_STEP;
        const newScale = Math.min(Math.max(MIN_SCALE, scale + delta), MAX_SCALE);

        const ratio = newScale / scale;
        const newOriginX = (offsetX - translateX) * (1 - ratio);
        const newOriginY = (offsetY - translateY) * (1 - ratio);

        translateX += newOriginX;
        translateY += newOriginY;
        scale = newScale;

        map.style.transition = scale === MIN_SCALE ? `transform ${TRANSITION_DURATION} ease-out` : `transform ${NO_TRANSITION}`;
        if (scale === MIN_SCALE) {
            translateX = 0;
            translateY = 0;
        }

        applyTransform();
    }

    function handleMouseDown(event) {
        if (event.button === 0) {
            isDragging = true;
            startX = event.clientX;
            startY = event.clientY;
            map.style.transition = `transform ${NO_TRANSITION}`;
        }
    }

    function handleMouseMove(event) {
        if (isDragging) {
            const dx = event.clientX - startX;
            const dy = event.clientY - startY;

            translateX += dx;
            translateY += dy;
            startX = event.clientX;
            startY = event.clientY;

            applyTransform();
        }
    }

    function handleMouseUpOrLeave() { 
        isDragging = false;
    }

    mapContainer.addEventListener('wheel', handleWheel, { passive: false });
    mapContainer.addEventListener('mousedown', handleMouseDown);
    mapContainer.addEventListener('mousemove', handleMouseMove);
    mapContainer.addEventListener('mouseup', handleMouseUpOrLeave);
    mapContainer.addEventListener('mouseleave', handleMouseUpOrLeave);
}