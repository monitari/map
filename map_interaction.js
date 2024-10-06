document.addEventListener('DOMContentLoaded', function () {
    let subdivisions = document.querySelectorAll('.subdivision');
    let tooltip = document.getElementById('tooltip');
    let toggleButton = document.getElementById('population-toggle');
    let populationMode = false; // Initial mode: off

    // 인구에 따라 색상을 설정하는 함수
    function getPopulationColor(population) {
        let minPop = 10000;  // 최소 인구
        let maxPop = 10000000; // 최대 인구
        let normalized = (parseInt(population) - minPop) / (maxPop - minPop);
        
        // 인구가 적을수록 녹색, 파랑 값이 올라가서 연한 색이 됨
        let greenBlueIntensity = Math.floor(255 * (1 - normalized)); 
        
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정, 적을수록 연한 빨강(흰색에 가까움)
    }

    // Function to apply population color based on current mode
    function applyPopulationColor() {
        subdivisions.forEach(function (subdivision) {
            let population = parseInt(subdivision.getAttribute('data-population'), 10);
            if (populationMode) {
                subdivision.style.fill = getPopulationColor(population); // 인구에 따라 색상 변경
            } else {
                subdivision.style.fill = '#989898'; // 기본 색상
            }
        });
    }

    // Toggle button functionality
    toggleButton.addEventListener('click', function () {
        populationMode = !populationMode; // 토글 모드 전환
        applyPopulationColor(); // 새로운 색상 적용
    });

    // Tooltip functionality for subdivision hover
    subdivisions.forEach(function (subdivision) {
        subdivision.addEventListener('mouseenter', function (event) {
            let name = subdivision.getAttribute('data-name');
            let area = subdivision.getAttribute('data-area');
            let population = subdivision.getAttribute('data-population');
            
            tooltip.innerHTML = `Name: ${name}<br>Area: ${area}<br>Population: ${population}`;
            tooltip.style.display = 'block'; 
            tooltip.style.left = event.pageX + 'px';  
            tooltip.style.top = (event.pageY + 10) + 'px';
            subdivision.style.stroke = 'yellow';
        });

        subdivision.addEventListener('mousemove', function (event) {
            tooltip.style.left = event.pageX + 'px';  
            tooltip.style.top = (event.pageY + 10) + 'px';
        });

        subdivision.addEventListener('mouseleave', function () {
            tooltip.style.display = 'none';
            subdivision.style.stroke = 'none';
            applyPopulationColor(); // Reset color when leaving the subdivision
        });
    });

    // Initial setup
    applyPopulationColor();
});
