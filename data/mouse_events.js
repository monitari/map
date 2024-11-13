// mouse_events.js

// 마우스가 올라갔을 때
export const handleMouseEnter = (event, tooltip, generateTooltipContent) => {
    const subdivision = event.currentTarget;
    tooltip.innerHTML = generateTooltipContent(subdivision);
    tooltip.style.display = 'block';
    tooltip.classList.add('show');

    subdivision.style.stroke = 'yellow';
    subdivision.style.strokeWidth = '3px';
};

// 마우스가 움직일 때
export const handleMouseMove = (event, tooltip) => {
    const tooltipRect = tooltip.getBoundingClientRect();
    let x = event.pageX;
    let y = event.pageY + 10;

    if (x + tooltipRect.width > window.innerWidth) x = window.innerWidth - tooltipRect.width;
    if (y + tooltipRect.height > window.innerHeight) y = window.innerHeight - tooltipRect.height;

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
};

// 마우스가 떠났을 때
export const handleMouseLeave = (event, tooltip, applyColor) => {
    const subdivision = event.currentTarget;
    tooltip.style.display = 'none';
    tooltip.classList.remove('show');

    subdivision.style.stroke = 'none';
    applyColor();
};