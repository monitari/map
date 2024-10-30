import { calculateSeats } from './seat_calculator.js';
import { initializeMapInteractions } from './map_interactions.js';
import partyColors from './mashup/party_color.js';

const MIN_POP = 100000; // 최소 인구수
const MAX_POP = 10000000; // 최대 인구수
const MIN_DENSITY = 1; // 최소 인구 밀도
const MAX_DENSITY = 1000; // 최대 인구 밀도
const MIN_OPACITY = 0.15; // 최소 투명도
const MAX_OPACITY = 1; // 최대 투명도
const VOTE_GAP_DIVISOR = 30; // 표차 비율

window.toggleMinimize = function () { // 최소화 버튼 클릭 시 실행되는 함수
    const infoBox = document.getElementById('info-box');
    const minimizeButton = document.getElementById('minimize-button');
    infoBox.classList.toggle('minimized');
    minimizeButton.innerHTML = infoBox.classList.contains('minimized') ? '▼' : '▲'; // 최소화 상태에 따라 버튼 모양 변경
};

document.addEventListener('DOMContentLoaded', function () { // DOM(Document Object Model)이 완전히 로드되면 실행되는 함수
    const subdivisions = document.querySelectorAll('.subdivision');
    const tooltip = document.getElementById('tooltip');
    const populationToggleButton = document.getElementById('population-toggle');
    const densityToggleButton = document.getElementById('density-toggle');
    const electionToggleButton = document.getElementById('election-toggle');
    const infoBox = document.getElementById('info-box');
    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');
    const leadingPartyToggleButton = document.getElementById('leading-party-toggle');

    let populationMode = false; // 인구수 모드
    let densityMode = false; // 인구 밀도 모드
    let electionMode = false; // 선거 결과 모드
    let showLeadingPartyMode = false; // 1등 정당 표시 모드

    initializeMapInteractions(mapContainer, map); // 지도 상호작용 초기화

    function getColor(normalized) { // 정규화된 값을 받아 색상을 반환하는 함수
        const greenBlueIntensity = Math.floor(255 * (1 - normalized));
        return `rgb(250, ${greenBlueIntensity}, ${greenBlueIntensity})`; // 녹색과 파란색의 강도를 조절하여 색상 반환 (인구수가 많을수록 진한 색상)
    }

    function getPopulationColor(population) { // 인구수에 따른 색상을 반환하는 함수
        const normalized = (parseInt(population) - MIN_POP) / (MAX_POP - MIN_POP);
        return getColor(normalized); // 인구수가 많을수록 진한 색상
    }

    function getDensityColor(population, area) { // 인구 밀도에 따른 색상을 반환하는 함수
        const density = population / area;
        const normalized = (density - MIN_DENSITY) / (MAX_DENSITY - MIN_DENSITY);
        return getColor(normalized); // 인구 밀도가 높을수록 진한 색상
    }

    function getElectionColor(parties) { // 선거 결과에 따른 색상을 반환하는 함수
        let maxVote = 0; // 최대 득표수
        let secondMaxVote = 0; // 두 번째로 많은 득표수
        let leadingParty = ''; // 1등 정당

        for (let party in parties) { // 정당별 득표수 계산
            if (parties[party] > maxVote) { // 최대 득표수보다 많은 득표수가 있을 경우
                secondMaxVote = maxVote; // 두 번째로 많은 득표수를 최대 득표수로 변경
                maxVote = parties[party]; // 최대 득표수를 해당 득표수로 변경
                leadingParty = party; // 1등 정당을 해당 정당으로 변경
            } 
            else if (parties[party] > secondMaxVote) // 최대 득표수보다 적고 두 번째로 많은 득표수보다 많은 득표수가 있을 경우
                secondMaxVote = parties[party]; // 두 번째로 많은 득표수를 해당 득표수로 변경
        }

        if (!leadingParty || maxVote === secondMaxVote) 
            return 'rgba(255, 255, 255, 0.5)'; // 1등 정당이 없거나 최대 득표수와 두 번째로 많은 득표수가 같을 경우 투명한 색상 반환

        const voteGap = maxVote - secondMaxVote; // 득표수 차이
        const opacity = Math.min(MAX_OPACITY, Math.max(MIN_OPACITY, (voteGap / VOTE_GAP_DIVISOR))); // 투명도 계산
        const baseColor = partyColors[leadingParty] || 'rgb(255, 255, 255)'; // 1등 정당의 색상

        return baseColor.replace('rgb', 'rgba').replace(')', `, ${opacity})`); // 투명도를 적용한 색상 반환
    }

    function getLeadingParty(seats) { // 1등 정당을 반환하는 함수
        let leadingParty = null; // 1등 정당
        let maxSeats = 0; // 최대 의석수
        for (let party in seats) {
            if (seats[party] > maxSeats) { // 최대 의석수보다 많은 의석수가 있을 경우
                maxSeats = seats[party];
                leadingParty = party; // 1등 정당을 해당 정당으로 변경
            }
        }
        return leadingParty; // 1등 정당 반환
    }

    function applyColor() { // 색상 적용 함수
        subdivisions.forEach(subdivision => {
            const population = parseInt(subdivision.getAttribute('data-population'), 10); // 인구수
            const area = parseFloat(subdivision.getAttribute('data-area')); // 면적
            const parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당별 받은 투표율

            if (populationMode) subdivision.style.fill = getPopulationColor(population); // 인구수 모드일 경우
            else if (densityMode) subdivision.style.fill = getDensityColor(population, area); // 인구 밀도 모드일 경우
            else if (electionMode && showLeadingPartyMode) subdivision.style.fill = partyColors[getLeadingParty(parties)]; // 1등 정당 표시 모드일 경우
            else if (electionMode) subdivision.style.fill = getElectionColor(parties); // 선거 결과 모드일 경우
            else subdivision.style.fill = '#989898'; // 기본 색상
        });
    }

    function displayElectionResults(showDisplay) { // 선거 결과 표시 함수
        if (showDisplay) { // 선거 결과 표시 모드일 경우
            infoBox.style.display = 'block'; // 정보 박스 표시
            const event = subdivisions[0].getAttribute('data-events'); // 사건
            const { finalSeats, proportionalPartySeats, localPartySeats } = calculateSeats(subdivisions); // 의석 계산 (비례대표 의석, 지역구 의석)

            let resultHTML = `
                <button id="minimize-button" onclick="toggleMinimize()">▲</button>
                <h3 style="margin-bottom: 5px; margin-top: -5px;">선거 결과
                <span style="font-size: 0.8em; margin-left: 5px; color: gray; font-weight: normal;">${event}</span>
            </h3>
            <div style="font-size: 0.8em; margin-bottom: 5px;">0.5% 이상 득표율을 얻지 못한 정당은 비례대표 의석을 받지 못합니다.</div>`;

            const sortedParties = Object.keys(finalSeats).sort((a, b) => finalSeats[b] - finalSeats[a] || a.localeCompare(b));
            const finalTotalSeats = Object.values(finalSeats).reduce((a, b) => a + b, 0);
            const totalProportionalSeats = Object.values(proportionalPartySeats).reduce((a, b) => a + b, 0);
            const totalLocalSeats = Object.values(localPartySeats).reduce((a, b) => a + b, 0);

            sortedParties.forEach(party => { // 정당별 의석수 표시
                const colorBox = `<span style="display:inline-block;width:10px;height:10px;background-color:${partyColors[party]};margin-right:3px;"></span>`;
                const percentage = ((finalSeats[party] / finalTotalSeats) * 100).toFixed(2);
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
                            ${finalTotalSeats}석 <span style="font-size: 1em;">(비례 ${totalProportionalSeats}석 | 지역구 ${totalLocalSeats}석)</span></p>`;
            infoBox.innerHTML = resultHTML; // 정보 박스에 선거 결과 표시
        } 
        else infoBox.style.display = 'none'; // 선거 결과 표시 모드가 아닐 경우 정보 박스 숨김
    }

    function toggleMode(mode) { // 모드 전환 함수
        populationMode = mode === 'population'; // 인구수 모드
        densityMode = mode === 'density'; // 인구 밀도 모드
        electionMode = mode === 'election'; // 선거 결과 모드
        displayElectionResults(electionMode); // 선거 결과 표시
        applyColor(); // 색상 적용
        leadingPartyToggleButton.style.display = electionMode ? 'block' : 'none'; // 선거 결과 모드일 경우 1등 정당 표시 버튼 표시
    }

    function addToggleEventListener(button, mode) { // 토글 이벤트 리스너 추가 함수
        button.addEventListener('click', () => toggleMode(mode)); // 클릭 시 모드 전환
    }

    addToggleEventListener(populationToggleButton, 'population'); // 클릭 시 인구수 모드로 전환
    addToggleEventListener(densityToggleButton, 'density'); // 클릭 시 인구 밀도 모드로 전환
    addToggleEventListener(electionToggleButton, 'election'); // 클릭 시 선거 결과 모드로 전환

    leadingPartyToggleButton.addEventListener('click', () => { // 1등 정당 표시 버튼 클릭 시
        showLeadingPartyMode = !showLeadingPartyMode; // 1등 정당 표시 모드 전환
        applyColor(); // 색상 적용
    });

    function formatNumber(num) { // 숫자를 받아 적절한 형식으로 반환하는 함수 (ex 129304534 -> 1억 2930만 4534)
        if (num >= 100000000) return (num / 100000000).toFixed(2) + '억'; // 1억 이상일 경우
        if (num >= 10000) return (num / 10000).toFixed(2) + '만'; // 1만 이상일 경우
        return num.toString();
    }

    function generateTooltipContent(subdivision) { // 툴팁 내용 생성 함수
        const name = subdivision.getAttribute('data-name'); // 이름
        const area = subdivision.getAttribute('data-area'); // 면적
        const population = subdivision.getAttribute('data-population'); // 인구수
        const state = subdivision.getAttribute('data-state'); // 주
        const rankArea = subdivision.getAttribute('data-rank-area'); // 면적 순위
        const rankPopulation = subdivision.getAttribute('data-rank-population'); // 인구 순위
        const rankDensity = subdivision.getAttribute('data-rank-density'); // 인구 밀도 순위
        const provinceCnt = subdivision.getAttribute('data-all-province'); // 전체 지역 수
        const events = subdivision.getAttribute('data-events'); // 사건
        const parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당별 받은 투표율
        const invalidVotes = subdivision.getAttribute('data-invalid-votes'); // 무효표

        let partiesHtml = ''; // 정당별 득표율 HTML
        let otherPartiesHtml = ''; // 기타 정당 HTML
        let sortedParties = Object.keys(parties).sort((a, b) => parseFloat(parties[b]) - parseFloat(parties[a])); // 정당별 득표율 정렬
        let otherParties = []; // 기타 정당 (정당별 득표율 1% 미만)
        let counter = 0; // 카운터 (정당별 득표율 3개씩 나열)

        sortedParties.forEach(party => { // 정당별 득표율 HTML 생성
            const value = parseFloat(parties[party]); // 득표율
            const color = partyColors[party] || 'rgb(200, 200, 200)'; // 정당 색상 (없을 경우 회색)

            if (isNaN(value)) return; // 득표율이 숫자가 아닐 경우
            if (value < 1.0) otherParties.push({ party, value }); // 기타 정당에 추가 (정당별 득표율 1% 미만)
            else {
                if (counter % 3 === 0) partiesHtml += '<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">';
                partiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 4px 0 4px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: ${color}; margin-right: 5px; flex-shrink: 0;"></div>
                        ${party}<span style="color: gray; margin-left: 5px;">${value.toFixed(3)}%</span></div>`;
                if (counter % 3 === 2) partiesHtml += '</div>';
                counter++; // 카운터 증가 (정당별 득표율 3개씩 나열)
            }
        });
        if (counter % 3 !== 0) partiesHtml += '</div>'; // 정당별 득표율 3개씩 나열이 끝나지 않았을 경우 마무리

        const invalidVotesPercentage = parseFloat(invalidVotes); // 무효표 비율
        if (otherParties.length > 0 || invalidVotesPercentage > 0) { // 기타 정당이 있거나 무효표 비율이 0보다 클 경우
            const otherPartiesSum = otherParties.reduce((acc, cur) => acc + cur.value, 0); // 기타 정당 득표율 합계
            otherPartiesHtml += `
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px 0 5px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(200, 200, 200); margin-right: 5px; flex-shrink: 0;"></div>
                        기타<span style="color: gray; margin-left: 5px;">${otherPartiesSum.toFixed(3)}% (1% 미만)</span>
                    </div>
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px 0 5px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(0, 0, 0); margin-right: 5px; flex-shrink: 0;"></div>
                        무효표<span style="color: gray; margin-left: 5px;">${invalidVotesPercentage.toFixed(3)}%</span>
                    </div>
                </div>`;
        }

        let finalHtml = partiesHtml + otherPartiesHtml; // 최종 HTML

        let barHtml = ''; // 막대 HTML
        let cumulativePercentage = 0; // 누적 비율
        sortedParties.forEach(party => { // 막대 HTML 생성
            const value = parseFloat(parties[party]); // 득표율
            const color = partyColors[party] || 'rgb(200, 200, 200)'; // 정당 색상 (없을 경우 회색)

            if (isNaN(value) || value < 1.0) return; // 득표율이 숫자가 아니거나 1% 미만일 경우
            barHtml += `<div style="background-color: ${color}; height: 20px; width: ${value}%;"></div>`; // 막대 추가
            cumulativePercentage += value; // 누적 비율 증가
        });

        if (otherParties.length > 0) { // 기타 정당이 있을 경우 (정당별 득표율 1% 미만, 회색)
            const otherPartiesSum = otherParties.reduce((acc, cur) => acc + cur.value, 0); // 기타 정당 득표율 합계
            barHtml += `<div style="background-color: rgb(200, 200, 200); height: 20px; width: ${otherPartiesSum}%;"></div>`;
        }

        if (!isNaN(invalidVotesPercentage) && invalidVotesPercentage > 0) { // 무효표 비율이 숫자이고 0보다 클 경우 (검은색)
            barHtml += `<div style="background-color: black; height: 20px; width: ${invalidVotesPercentage}%;"></div>`;
        }

        return `
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 3px; margin-left: 3px;">
                ${name} <span style="font-size: 0.6em; color: gray;">${state}</span>
            </div>
            <div style="font-size: 1em; margin-left: 3px;">
                <div>면적 | ${formatNumber(area)}A <span style="font-size: 0.8em; color: gray; 
                margin-left: 5px;">(${rankArea} / ${provinceCnt}위)</span></div>
                <div>인구 | ${formatNumber(population)}명 <span style="font-size: 0.8em; color: gray; 
                margin-left: 5px;">(${rankPopulation} / ${provinceCnt}위)</span></div>
                <div>인구 밀도 | ${(population / area).toFixed(3)}명/A <span style="font-size: 0.8em; color: gray; 
                margin-left: 5px;">(${rankDensity} / ${provinceCnt}위)</span></div>
                <div style="font-size: 0.8em; color: gray; margin-top: 2px;">사건 | ${events}</span></div>
                <div style="margin-left: 10px; margin-top: 2px;">${finalHtml}</div>
                <div style="display: flex; margin-top: 10px; height: 20px; border: 1px solid #ccc;">
                    ${barHtml}
                </div>
            </div>`; // 툴팁 내용 반환
    }

    function handleMouseEnter(event) {
        const subdivision = event.currentTarget;
        tooltip.innerHTML = generateTooltipContent(subdivision);
    
        const tooltipRect = tooltip.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
    
        let tooltipX = event.pageX;
        let tooltipY = event.pageY + 7;
        if (tooltipX + tooltipRect.width > viewportWidth) tooltipX = viewportWidth - tooltipRect.width;
        if (tooltipY + tooltipRect.height > viewportHeight) tooltipY = viewportHeight - tooltipRect.height;
    
        tooltip.style.left = tooltipX + 'px';
        tooltip.style.top = tooltipY + 'px';
        tooltip.style.display = 'block';
        tooltip.classList.add('show'); // 애니메이션 클래스 추가
    
        subdivision.style.stroke = 'yellow';
        subdivision.style.strokeWidth = '5px';
    }

    function handleMouseMove(event) { // 마우스가 움직일 때 실행되는 함수
        const tooltipWidth = tooltip.offsetWidth; // 툴팁 너비
        const tooltipHeight = tooltip.offsetHeight; // 툴팁 높이
        const pageWidth = window.innerWidth; // 페이지 너비
        const pageHeight = window.innerHeight; // 페이지 높이

        let x = event.pageX; // 마우스 위치에 툴팁 표시
        let y = event.pageY + 10; // 마우스 위치에 툴팁 표시

        if (x + tooltipWidth > pageWidth) x = pageWidth - tooltipWidth; // 툴팁이 페이지 너비를 넘어갈 경우
        if (y + tooltipHeight > pageHeight) y = pageHeight - tooltipHeight; // 툴팁이 페이지 높이를 넘어갈 경우

        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
    }

    function handleMouseLeave(event) { // 마우스가 나갔을 때 실행되는 함수
        const subdivision = event.currentTarget; // 현재 요소
        tooltip.style.display = 'none'; // 툴팁 숨김
        tooltip.classList.remove('show'); // 애니메이션 클래스 제거
        subdivision.style.stroke = 'none';
        applyColor();
    }

    subdivisions.forEach(subdivision => { // 각 요소에 이벤트 리스너 추가
        subdivision.addEventListener('mouseenter', handleMouseEnter);
        subdivision.addEventListener('mousemove', handleMouseMove);
        subdivision.addEventListener('mouseleave', handleMouseLeave);
    });

    applyColor(); // 색상 적용
});