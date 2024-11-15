// mouse_events.js

let originalFill = null; // 기존 fill 색상을 저장하는 변수
let tooltipTimeout; // 애니메이션 중첩 방지용 변수

// 마우스가 올라갔을 때
export const handleMouseEnter = (event, tooltip, generateTooltipContent) => {
    const subdivision = event.currentTarget;
    originalFill = subdivision.style.fill || 'rgba(0, 0, 0, 1)';
    const content = generateTooltipContent(subdivision);

    if (tooltipTimeout) clearTimeout(tooltipTimeout); // 기존 타이머 취소

    tooltip.innerHTML = content; // 툴팁 내용 설정
    tooltip.style.left = `${event.pageX + 10}px`;
    tooltip.style.top = `${event.pageY + 10}px`;

    tooltip.classList.remove('hide'); // 숨김 상태 제거
    tooltip.classList.add('show'); // 표시 상태 추가
    tooltip.style.opacity = '1'; // 투명도 설정
    tooltip.style.visibility = 'visible'; // 표시 상태 추가

    // 애니메이션을 위해 transition 추가
    subdivision.style.transition = 'fill 0.3s ease';
    subdivision.style.fill = 'rgba(255, 255, 150, 1)';
};

// 마우스가 움직일 때
export const handleMouseMove = (event, tooltip) => {
    const tooltipRect = tooltip.getBoundingClientRect();
    let x = event.pageX + 10; // 마우스 포인터의 오른쪽
    let y = event.pageY + 10; // 마우스 포인터의 아래쪽

    // 화면을 벗어나지 않도록 위치 조정
    if (x + tooltipRect.width > window.innerWidth) x = window.innerWidth - tooltipRect.width;
    if (y + tooltipRect.height > window.innerHeight) y = window.innerHeight - tooltipRect.height;

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
};

// 마우스가 떠났을 때
export const handleMouseLeave = (event, tooltip) => {
    const subdivision = event.currentTarget;

    if (tooltipTimeout) clearTimeout(tooltipTimeout); // 기존 타이머 취소

    tooltip.classList.remove('show'); // 표시 상태 제거
    tooltip.classList.add('hide'); // 숨김 상태 추가
    tooltip.style.opacity = '0'; // 투명도 설정

    // subdivision 색 복원
    subdivision.style.fill = originalFill;
    subdivision.style.transition = 'fill 0.3s ease';

    // 사라지는 애니메이션 이후 툴팁 완전히 숨기기
    tooltipTimeout = setTimeout(() => {
        tooltip.style.visibility = 'hidden'; // 완전히 숨김
    }, 300); // transition 시간과 일치 (0.3s)
};