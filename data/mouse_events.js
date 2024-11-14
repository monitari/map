// mouse_events.js

// 기존 stroke 색상을 저장하는 변수
let originalStroke = null;

// 마우스가 올라갔을 때
export const handleMouseEnter = (event, tooltip, generateTooltipContent) => {
    const subdivision = event.currentTarget;
    originalStroke = subdivision.style.stroke;
    const content = generateTooltipContent(subdivision);

    if (tooltip.innerHTML !== content) tooltip.innerHTML = content;
    if (tooltip.style.display !== 'block') tooltip.style.display = 'block';
    if (!tooltip.classList.contains('show')) tooltip.classList.add('show');

    subdivision.style.stroke = 'yellow';
    subdivision.style.strokeWidth = '3px';
};

// 마우스가 움직일 때
export const handleMouseMove = (event, tooltip) => {
    const tooltipRect = tooltip.getBoundingClientRect();
    let x = event.pageX + 5;
    let y = event.pageY + 5;

    if (x + tooltipRect.width > window.innerWidth) x = window.innerWidth - tooltipRect.width;
    if (y + tooltipRect.height > window.innerHeight) y = window.innerHeight - tooltipRect.height;

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
};

// 마우스가 떠났을 때
export const handleMouseLeave = (event, tooltip, applyColor) => {
    const subdivision = event.currentTarget;

    if (tooltip.style.display !== 'none') tooltip.style.display = 'none';
    if (tooltip.classList.contains('show')) tooltip.classList.remove('show');

    subdivision.style.stroke = originalStroke;
    subdivision.style.strokeWidth = '1px'; // 원래 두께로 복원
    applyColor();
};