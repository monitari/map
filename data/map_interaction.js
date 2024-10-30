import { calculateSeats } from './seat_calculator.js';
import { initializeMapInteractions } from './map_interactions.js';
import partyColors from './mashup/party_color.js';

const MIN_POP = 100000; // 최소 인구수
const MAX_POP = 10000000; // 최대 인구수
const MIN_DENSITY = 1; // 최소 인구밀도
const MAX_DENSITY = 1000; // 최대 인구밀도

window.toggleMinimize = function () { // 최소화 버튼 클릭 시 실행되는 함수
    const infoBox = document.getElementById('info-box');
    infoBox.classList.toggle('minimized');
    const minimizeButton = document.getElementById('minimize-button');
    minimizeButton.innerHTML = infoBox.classList.contains('minimized') ? '▼' : '▲'; // 최소화 상태에 따라 버튼 모양 변경
};

document.addEventListener('DOMContentLoaded', function () { // 페이지 로드 시 실행되는 함수
    const subdivisions = document.querySelectorAll('.subdivision');
    const tooltip = document.getElementById('tooltip');
    const populationToggleButton = document.getElementById('population-toggle');
    const densityToggleButton = document.getElementById('density-toggle');
    const electionToggleButton = document.getElementById('election-toggle');
    const infoBox = document.getElementById('info-box');
    let populationMode = false; // 인구수 모드
    let densityMode = false; // 인구밀도 모드
    let electionMode = false; // 선거 모드
    let showLeadingPartyMode = false; // 1등 정당 표시 모드

    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');
    initializeMapInteractions(mapContainer, map); // 지도 상호작용 초기화

    function getPopulationColor(population) { // 인구수에 따른 색상 반환
        const normalized = (parseInt(population) - MIN_POP) / (MAX_POP - MIN_POP);
        const greenBlueIntensity = Math.floor(255 * (1 - normalized));
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`; // 인구수가 많을수록 진한 색상
    }

    function getDensityColor(population, area) { // 인구밀도에 따른 색상 반환
        const density = population / area;
        const normalized = (density - MIN_DENSITY) / (MAX_DENSITY - MIN_DENSITY);
        const greenBlueIntensity = Math.floor(255 * (1 - normalized));
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`; // 인구밀도가 높을수록 진한 색상
    }

    function getElectionColor(parties) { // 선거 결과에 따른 색상 반환
        let maxVote = 0; // 1등 정당의 득표수
        let secondMaxVote = 0; // 2등 정당의 득표수
        let leadingParty = ''; // 1등 정당

        for (let party in parties) {
            if (parties[party] > maxVote) { // 1등 정당의 득표수
                secondMaxVote = maxVote;
                maxVote = parties[party];
                leadingParty = party;
            } 
            else if (parties[party] > secondMaxVote) secondMaxVote = parties[party]; // 2등 정당의 득표수
        }

        if (!leadingParty || maxVote === secondMaxVote) return 'rgba(255, 255, 255, 0.5)'; // 1등 정당이 없거나 1등과 2등의 득표수가 같을 경우

        const voteGap = maxVote - secondMaxVote; // 1등과 2등의 득표수 차이
        const opacity = Math.min(1, Math.max(0.15, (voteGap / 30))); // 1등과 2등의 득표수 차이에 따라 투명도 조절 (0.15 ~ 1, 30퍼센트 이상 차이 시 1)
        const baseColor = partyColors[leadingParty] || 'rgb(255, 255, 255)'; // 1등 정당의 색상

        return baseColor.replace('rgb', 'rgba').replace(')', `, ${opacity})`); // 1등 정당의 색상에 투명도 적용
    }

    function getLeadingParty(seats) { // 1등 정당 반환
        let leadingParty = null; // 1등 정당
        let maxSeats = 0; // 1등 정당의 의석수
        for (let party in seats) {
            if (seats[party] > maxSeats) {
                maxSeats = seats[party];
                leadingParty = party;
            }
        }
        return leadingParty;
    }

    function applyColor() { // 색상 적용
        subdivisions.forEach(subdivision => {
            const population = parseInt(subdivision.getAttribute('data-population'), 10);
            const area = parseFloat(subdivision.getAttribute('data-area'));
            const parties = JSON.parse(subdivision.getAttribute('data-parties'));
            if (populationMode) subdivision.style.fill = getPopulationColor(population); // 인구수 모드일 경우 인구수에 따른 색상 적용
            else if (densityMode) subdivision.style.fill = getDensityColor(population, area); // 인구밀도 모드일 경우 인구밀도에 따른 색상 적용
            else if (electionMode && showLeadingPartyMode) 
                subdivision.style.fill = partyColors[getLeadingParty(parties)]; // 선거 모드이면서 1등 정당 표시 모드일 경우 1등 정당의 색상 적용
            else if (electionMode) subdivision.style.fill = getElectionColor(parties); // 선거 모드일 경우 선거 결과에 따른 색상 적용
            else subdivision.style.fill = '#989898'; // 기본 색상 (회색)
        });
    }

    function displayElectionResults(showDisplay) { // 선거 결과 표시
        if (showDisplay) { // 선거 결과 표시 모드일 경우
            infoBox.style.display = 'block';
            const event = subdivisions[0].getAttribute('data-events');
            const { finalSeats, proportionalPartySeats, localPartySeats } = calculateSeats(subdivisions); // 의석 계산 (최종 의석, 비례대표 의석, 지역구 의석)

            let resultHTML = `
                <button id="minimize-button" onclick="toggleMinimize()">▲</button>
                <h3 style="margin-bottom: 5px; margin-top: -5px;">선거 결과
                <span style="font-size: 0.8em; margin-left: 5px; color: gray; font-weight: normal;">${event}</span>
            </h3>`;
            resultHTML += `<div style="font-size: 0.8em; margin-bottom: 5px;">0.5% 이상 득표율을 얻지 못한 정당은 비례대표 의석을 받지 못합니다.</div>`;
            const sortedParties = Object.keys(finalSeats).sort((a, b) => {
                if (finalSeats[b] === finalSeats[a]) return a.localeCompare(b); // 의석 수가 같을 경우 정당 이름 순으로 정렬
                return finalSeats[b] - finalSeats[a]; // 의석 수가 많은 순으로 정렬
            });

            const finaltotalSeats = Object.values(finalSeats).reduce((a, b) => a + b, 0);
            const totalProportionalSeats = Object.values(proportionalPartySeats).reduce((a, b) => a + b, 0);
            const totalLocalSeats = Object.values(localPartySeats).reduce((a, b) => a + b, 0);

            sortedParties.forEach(party => { // 정당별 의석 수 표시
                const colorBox = `<span style="display:inline-block;width:10px;height:10px;background-color:${partyColors[party]};margin-right:3px;"></span>`;
                const percentage = ((finalSeats[party] / finaltotalSeats) * 100).toFixed(2); // 비율 계산 (소수점 2자리까지)
                resultHTML += `
                    <div style="display: flex; align-items: center; margin: 3px 0;">
                        <p style="line-height: 1.2; margin: 0; flex-grow: 1;">
                            ${colorBox}${party} ${finalSeats[party]}석
                            <span style="font-size: 0.7em;">${percentage}% (비례 ${proportionalPartySeats[party] || 0} | 지역구 ${localPartySeats[party] || 0})</span>
                        </p>
                        <div style="background-color: ${partyColors[party]}; height: 10px; width: ${percentage}%;"></div>
                    </div>`;
            });
            resultHTML += `<p style="font-weight:bold; margin-top: 5px; margin-bottom: 2px; font-size: 1.2em;">
                            ${finaltotalSeats}석 <span style="font-size: 1em;">(비례 ${totalProportionalSeats}석 | 지역구 ${totalLocalSeats}석)</span></p>`;
            infoBox.innerHTML = resultHTML;
        } 
        else infoBox.style.display = 'none'; // 선거 결과 표시 모드가 아닐 경우
    }

    function toggleMode(mode) { // 모드 전환
        populationMode = mode === 'population'; // 인구수 모드
        densityMode = mode === 'density'; // 인구밀도 모드
        electionMode = mode === 'election'; // 선거 모드
        displayElectionResults(electionMode); // 선거 결과 표시
        applyColor(); // 색상 적용
        document.getElementById('leading-party-toggle').style.display = electionMode ? 'block' : 'none'; // 선거 모드일 경우 1등 정당 표시 버튼 표시
    }

    function handleMouseEnter(event, subdivision) { // 마우스가 지역구에 들어갔을 때 실행되는 함수
        tooltip.innerHTML = getTooltipContent(subdivision);
        setTooltipPosition(event, tooltip); // 툴팁 위치 설정
        tooltip.style.display = 'block'; // 툴팁 표시
        subdivision.style.stroke = 'yellow'; // 테두리 색상 변경
        subdivision.style.strokeWidth = '5px';
    }

    function handleMouseMove(event) { // 마우스가 지역구 위에서 움직일 때 실행되는 함수
        setTooltipPosition(event, tooltip);
    }

    function handleMouseLeave(subdivision) { // 마우스가 지역구에서 나갔을 때 실행되는 함수
        tooltip.style.display = 'none'; // 툴팁 숨김
        subdivision.style.stroke = 'none'; // 테두리 제거
        applyColor();
    }

    populationToggleButton.addEventListener('click', () => toggleMode('population')); // 인구수 모드로 전환
    densityToggleButton.addEventListener('click', () => toggleMode('density')); // 인구밀도 모드로 전환
    electionToggleButton.addEventListener('click', () => toggleMode('election')); // 선거 모드로 전환

    subdivisions.forEach(subdivision => { // 각 지역구에 대해 이벤트 리스너 추가
        subdivision.addEventListener('mouseenter', event => handleMouseEnter(event, subdivision)); // 마우스가 지역구에 들어갔을 때
        subdivision.addEventListener('mousemove', handleMouseMove); // 마우스가 지역구 위에서 움직일 때
        subdivision.addEventListener('mouseleave', () => handleMouseLeave(subdivision)); // 마우스가 지역구에서 나갔을 때
    });

    document.getElementById('leading-party-toggle').addEventListener('click', function () { // 1등 정당 표시 버튼 클릭 시 실행되는 함수
        showLeadingPartyMode = !showLeadingPartyMode; // 1등 정당 표시 모드 전환
        applyColor(); // 색상 적용
    });

    applyColor(); // 색상 적용
});