document.addEventListener('DOMContentLoaded', function () {
    let subdivisions = document.querySelectorAll('.subdivision');
    let tooltip = document.getElementById('tooltip');
    let toggleButton = document.getElementById('population-toggle');
    let densityToggleButton = document.getElementById('density-toggle');
    let populationMode = false; // Initial population mode: off
    let densityMode = false; // Initial density mode: off

    // 인구에 따라 색상을 설정하는 함수
    function getPopulationColor(population) {
        let minPop = 100000;  // 최소 인구
        let maxPop = 10000000; // 최대 인구
        let normalized = (parseInt(population) - minPop) / (maxPop - minPop);
        let greenBlueIntensity = Math.floor(255 * (1 - normalized)); 
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정
    }

    // 인구 밀도에 따라 색상을 설정하는 함수
    function getDensityColor(population, area) {
        let density = population / area; // 인구 밀도 계산
        let minDensity = 1; // 최소 밀도
        let maxDensity = 1000; // 최대 밀도
        let normalized = (density - minDensity) / (maxDensity - minDensity);
        let greenBlueIntensity = Math.floor(255 * (1 - normalized));
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`;  // 빨간색 고정
    }

    // Function to apply color based on current mode
    function applyColor() {
        subdivisions.forEach(function (subdivision) {
            let population = parseInt(subdivision.getAttribute('data-population'), 10);
            let area = parseFloat(subdivision.getAttribute('data-area')); // 면적 가져오기
            if (populationMode) {
                subdivision.style.fill = getPopulationColor(population); // Color based on population
            } else if (densityMode) {
                subdivision.style.fill = getDensityColor(population, area); // Color based on density
            } else {
                subdivision.style.fill = '#989898'; // Default color
            }
        });
    }

    // Toggle button functionality
    toggleButton.addEventListener('click', function () {
        populationMode = !populationMode; // Toggle the population mode
        densityMode = false; // 밀도 모드를 끔
        applyColor(); // Apply the new color scheme
    });

    // Density toggle button functionality
    densityToggleButton.addEventListener('click', function () {
        densityMode = !densityMode; // Toggle the density mode
        populationMode = false; // 인구 모드를 끔
        applyColor(); // Apply the new color scheme
    });

    // Tooltip functionality for subdivision hover
    subdivisions.forEach(function (subdivision) {
        subdivision.addEventListener('mouseenter', function (event) {
            let name = subdivision.getAttribute('data-name');
            let area = subdivision.getAttribute('data-area');
            let population = subdivision.getAttribute('data-population');
            
            tooltip.innerHTML = `Name: ${name}<br>Area: ${area}A <br>Population: ${population}명
            <br>Density: ${(population / area).toFixed(2)}명/A`; // 툴팁에 이름, 면적, 인구, 밀도 표시
            tooltip.style.display = 'block'; 
            tooltip.style.left = event.pageX + 'px';  
            tooltip.style.top = (event.pageY + 10) + 'px';
            subdivision.style.stroke = 'yellow'; // Highlight the subdivision
            subdivision.style.strokeWidth = '5px'; // Highlight the subdivision
        });

        subdivision.addEventListener('mousemove', function (event) {
            tooltip.style.left = event.pageX + 'px';  
            tooltip.style.top = (event.pageY + 10) + 'px';
        });

        subdivision.addEventListener('mouseleave', function () {
            tooltip.style.display = 'none';
            subdivision.style.stroke = 'none';
            applyColor(); // Reset color when leaving the subdivision
        });
    });

    // Initial setup
    applyColor();
});
