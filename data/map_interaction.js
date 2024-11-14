// map_interaction.js

import { calculateSeats } from './seat_calculator.js';
import { initializeMapInteractions } from './map_interactions.js';
import partyColors from './mashup/party_color.js';
import { handleMouseEnter, handleMouseMove, handleMouseLeave } from './mouse_events.js';

const MIN_OPACITY = 0.15;
const MAX_OPACITY = 1;
const VOTE_GAP_DIVISOR = 40;
const MINVOTE = 1;
const MIN_POP = 10000;
const MAX_POP = 3000000;
const MIN_DENSITY = 0;
const MAX_DENSITY = 5000;

// 행정구역 이름 숨기기
document.querySelectorAll('.province-name').forEach(name => name.classList.add('hidden'));

// 정보 상자 최소화/최대화 토글 함수
window.toggleMinimize = function () {
    const infoBox = document.getElementById('info-box');
    const minimizeButton = document.getElementById('minimize-button');
    infoBox.classList.toggle('minimized');
    if (!infoBox.classList.contains('minimized')) minimizeButton.innerHTML = '<i class="fas fa-minus"></i>';
    else minimizeButton.innerHTML = '　';
};

document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 선택
    const subdivisions = document.querySelectorAll('.subdivision');
    const tooltip = document.getElementById('tooltip');
    const darkModeToggleButton = document.getElementById('dark-mode-toggle');
    const populationToggleButton = document.getElementById('population-toggle');
    const densityToggleButton = document.getElementById('density-toggle');
    const electionToggleButton = document.getElementById('election-toggle');
    const leadingPartyToggleButton = document.getElementById('leading-party-toggle');
    const toggleNamesButton = document.getElementById('toggle-names');
    const rangeSliderContainer = document.getElementById('range-slider-container');
    const rangeSliderMin = document.getElementById('range-slider-min');
    const rangeSliderMax = document.getElementById('range-slider-max');
    const rangeValue = document.getElementById('range-value');
    const scaleBarInner = document.getElementById('scale-bar-inner');
    const infoBox = document.getElementById('info-box');
    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');
    
    let mode = ''; // 현재 모드
    let showLeadingPartyMode = false; // 주요 정당 모드 표시 여부
    let MIN_VALUE = 0;
    let MAX_VALUE = 1000000;
    scaleBarInner.style.width = '100%';
    
    // 지도 상호작용 초기화
    initializeMapInteractions(mapContainer, map);

    // 색상 계산 함수
    const getColor = (normalized) => `rgba(250, 0, 0, ${normalized})`;

    // 슬라이더 값 변경 이벤트 리스너 추가
    const updateRangeValue = () => {
        let min = parseInt(rangeSliderMin.value, 10);
        let max = parseInt(rangeSliderMax.value, 10);
    
        // 최소값이 최대값보다 큰 경우 값을 교환
        if (min > max) {
            [min, max] = [max, min];
            rangeSliderMin.value = min;
            rangeSliderMax.value = max;
        }
    
        rangeValue.textContent = `${mode === 'population' ? '인구' : '인구 밀도'} | 
        ${min}${mode === 'population' ? '명' : '명/A'} - ${max}${mode === 'population' ? '명' : '명/A'}`;
        MIN_VALUE = min;
        MAX_VALUE = max;
        applyColor();
    };

    // 인구 밀도 슬라이더 값 변경 이벤트 리스너 추가
    rangeSliderMin.addEventListener('input', updateRangeValue);
    rangeSliderMax.addEventListener('input', updateRangeValue);

    // 인구 기반 색상 계산 함수
    const getPopulationColor = (population) => {
        const normalized = (parseInt(population) - MIN_VALUE) / (MAX_VALUE - MIN_VALUE);
        return getColor(normalized);
    };
    
    // 인구 밀도 기반 색상 계산 함수
    const getDensityColor = (population, area) => {
        const density = population / area;
        const normalized = (density - MIN_VALUE) / (MAX_VALUE - MIN_VALUE);
        return getColor(normalized);
    };

    // 선거 결과 기반 색상 계산 함수
    const getElectionColor = (parties) => {
        let maxVote = 0,
            secondMaxVote = 0,
            leadingParty = '';

        for (let party in parties) {
            const vote = parties[party];
            if (vote > maxVote) {
                secondMaxVote = maxVote;
                maxVote = vote;
                leadingParty = party;
            } 
            else if (vote > secondMaxVote) secondMaxVote = vote;
        }

        if (!leadingParty || maxVote === secondMaxVote) return 'rgba(255, 255, 255, 0.5)';

        const voteGap = maxVote - secondMaxVote;
        const opacity = Math.min(MAX_OPACITY, Math.max(MIN_OPACITY, voteGap / VOTE_GAP_DIVISOR));
        const baseColor = partyColors[leadingParty] || 'rgb(255, 255, 255)';

        return baseColor.replace('rgb', 'rgba').replace(')', `, ${opacity})`);
    };

    // 주요 정당 계산 함수
    const getLeadingParty = (seats) => {
        let leadingParty = null, maxSeats = 0;
        for (let party in seats) {
            if (seats[party] > maxSeats) {
                maxSeats = seats[party];
                leadingParty = party;
            }
        }
        return leadingParty;
    };

    // 색상 적용 함수
    const applyColor = () => {
        subdivisions.forEach(subdivision => {
            const population = parseInt(subdivision.getAttribute('data-population'), 10);
            const area = parseFloat(subdivision.getAttribute('data-area'));
            const parties = JSON.parse(subdivision.getAttribute('data-parties'));

            if (mode === 'population') {
                subdivision.style.fill = getPopulationColor(population);
            } else if (mode === 'density') {
                subdivision.style.fill = getDensityColor(population, area);
            } else if (mode === 'election') {
                if (showLeadingPartyMode) {
                    subdivision.style.fill = partyColors[getLeadingParty(parties)];
                } else {
                    subdivision.style.fill = getElectionColor(parties);
                }
            } else {
                subdivision.style.fill = 'rgb(200, 200, 200)';
            }
        });
    };

    // 선거 결과 표시 함수
    const displayElectionResults = (show) => {
        if (show) {
            infoBox.style.display = 'block';
            const event = subdivisions[0].getAttribute('data-events');
            const { SEAT, PER, finalSeats, proportionalPartySeats, localPartySeats } = calculateSeats(subdivisions);

            const sortedParties = Object.keys(finalSeats).sort((a, b) => finalSeats[b] - finalSeats[a] || a.localeCompare(b));
            const finalTotalSeats = Object.values(finalSeats).reduce((a, b) => a + b, 0);
            const totalProportionalSeats = Object.values(proportionalPartySeats).reduce((a, b) => a + b, 0);
            const totalLocalSeats = Object.values(localPartySeats).reduce((a, b) => a + b, 0);

            let resultHTML = `
                <button id="minimize-button" onclick="toggleMinimize()"><i class="fas fa-minus"></i></button>
                <h3 class="result-header">선거 결과
                    <span class="event-date">${event}</span>
                </h3>
                <div class="seat-info">
                    비례대표는 전체 ${SEAT}석에서 지역구를 제외한 ${SEAT - totalLocalSeats}석(이론치) 중 ${PER * 100}% 이상 득표한 정당에 배분됩니다.
                </div>`;

            sortedParties.forEach(party => {
                const colorBox = `<span class="color-box" style="background-color:${partyColors[party]};"></span>`;
                const percentage = ((finalSeats[party] / finalTotalSeats) * 100).toFixed(2);
                resultHTML += `
                    <div class="party-result">
                        <p class="party-info">
                            ${colorBox}${party} ${finalSeats[party]}석
                            <span class="party-percentage">${percentage}% (${proportionalPartySeats[party] || 0} + ${localPartySeats[party] || 0})</span>
                        </p>
                        <div class="percentage-bar" style="background-color: ${partyColors[party]}; width: ${percentage}%;"></div>
                    </div>`;
            });

            resultHTML += `<p class="total-seats">
                            ${finalTotalSeats}석 <span class="seat-details">(비례 ${totalProportionalSeats}석 + 지역구 ${totalLocalSeats}석)</span>
                        </p>`;

            infoBox.innerHTML = resultHTML;
        }
        else infoBox.style.display = 'none';
    };

    // 모드 토글 함수
    const toggleMode = (newMode) => {
        mode = newMode;
        displayElectionResults(mode === 'election');
        applyColor();
        leadingPartyToggleButton.style.display = mode === 'election' ? 'block' : 'none';
        if (mode === 'population') {
            MIN_VALUE = MIN_POP;
            MAX_VALUE = MAX_POP;
            rangeSliderMin.min = MIN_POP;
            rangeSliderMin.max = MAX_POP;
            rangeSliderMax.min = MIN_POP;
            rangeSliderMax.max = MAX_POP;
        } else if (mode === 'density') {
            MIN_VALUE = MIN_DENSITY;
            MAX_VALUE = MAX_DENSITY;
            rangeSliderMin.min = MIN_DENSITY;
            rangeSliderMin.max = MAX_DENSITY;
            rangeSliderMax.min = MIN_DENSITY;
            rangeSliderMax.max = MAX_DENSITY;
        }
        rangeSliderContainer.style.display = (mode === 'population' || mode === 'density') ? 'block' : 'none';
        applyColor();
    };

    // 이벤트 리스너 추가
    populationToggleButton.addEventListener('click', () => {
        toggleMode('population');
        rangeSliderMin.value = MIN_POP;
        rangeSliderMax.value = MAX_POP;
        rangeValue.textContent = `인구 | ${rangeSliderMin.value}명 - ${rangeSliderMax.value}명`;
    });
    densityToggleButton.addEventListener('click', () => {
        toggleMode('density');
        rangeSliderMin.value = MIN_DENSITY;
        rangeSliderMax.value = MAX_DENSITY;
        rangeValue.textContent = `인구 밀도 | ${rangeSliderMin.value}명/A - ${rangeSliderMax.value}명/A`;
    });
    electionToggleButton.addEventListener('click', () => toggleMode('election'));

    // 1등 정당 토글 버튼 이벤트 리스너 추가
    leadingPartyToggleButton.addEventListener('click', () => {
        showLeadingPartyMode = !showLeadingPartyMode;
        applyColor();
    });

    // 행정구역 이름 토글 버튼 이벤트 리스너 추가
    toggleNamesButton.addEventListener('click', () => {
        document.querySelectorAll('.province-name').forEach(name => name.classList.toggle('hidden'));
        if (toggleNamesButton.textContent.includes('행정구역 이름 보기')) toggleNamesButton.innerHTML = '<i class="fas fa-map-signs"></i> 행정구역 이름 숨기기';
        else toggleNamesButton.innerHTML = '<i class="fas fa-map-signs"></i> 행정구역 이름 보기';
    });

    // 다크 모드 토글 버튼 이벤트 리스너 추가
    darkModeToggleButton.addEventListener('click', function() {
        document.body.classList.toggle('light-mode');
        if (document.body.classList.contains('light-mode')) this.innerHTML = '<i class="far fa-lightbulb"></i>'; // 전구 켜짐 아이콘
        else this.innerHTML = '<i class="fas fa-lightbulb"></i>'; // 전구 꺼짐 아이콘
    });

    // 숫자 포맷 함수
    const formatNumber = (num) => {
        if (num >= 1e8) return (num / 1e8).toFixed(2) + '억';
        if (num >= 1e4) return (num / 1e4).toFixed(2) + '만';
        return num.toString();
    };

    // 툴팁 내용 생성 함수
    const generateTooltipContent = (subdivision) => {
        const subname = subdivision.getAttribute('data-subname');
        const name = subdivision.getAttribute('data-name');
        const area = subdivision.getAttribute('data-area');
        const population = subdivision.getAttribute('data-population');
        const state = subdivision.getAttribute('data-state');
        const rankArea = subdivision.getAttribute('data-rank-area');
        const rankPopulation = subdivision.getAttribute('data-rank-population');
        const rankDensity = subdivision.getAttribute('data-rank-density');
        const events = subdivision.getAttribute('data-events');
        const parties = JSON.parse(subdivision.getAttribute('data-parties'));
        const invalidVotes = parseFloat(subdivision.getAttribute('data-invalid-votes'));

        let partiesHtml = '';
        let otherParties = [];
        let counter = 0;

        const sortedParties = Object.keys(parties)
            .filter(party => !isNaN(parties[party]))
            .sort((a, b) => parties[b] - parties[a]);

        sortedParties.forEach(party => {
            const value = parseFloat(parties[party]);
            const color = partyColors[party] || 'rgb(200, 200, 200)';

            if (value < MINVOTE) {
                otherParties.push({ party, value });
            } else {
                if (counter % 3 === 0) partiesHtml += '<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">';
                const colorBox = `<span class="color-box" style="background-color:${color}; width: 12px; height: 12px; margin-right: 5px;"></span>`;
                partiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 4px; font-size: 12px;">
                        ${colorBox}
                        ${party}<span style="color: gray; margin-left: 5px;">${value.toFixed(3)}%</span>
                    </div>`;
                if (counter % 3 === 2) partiesHtml += '</div>';
                counter++;
            }
        });
        if (counter % 3 !== 0) partiesHtml += '</div>';
        
        let otherHtml = '';
        if (otherParties.length > 0 || invalidVotes > 0) {
            const otherSum = otherParties.reduce((acc, cur) => acc + cur.value, 0);
            const otherColorBox = `<span class="color-box other" style="width: 12px; height: 12px; margin-right: 5px;"></span>`;            
            const invalidColorBox = `<span class="color-box" style="background-color: rgb(0, 0, 0); width: 12px; height: 12px; margin-right: 5px;"></span>`;
            otherHtml += `
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 4px; font-size: 12px;">
                        ${otherColorBox}기타<span style="color: gray; margin-left: 5px;">${otherSum.toFixed(3)}% (${MINVOTE}% 미만)</span>
                    </div>
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px; font-size: 12px; justify-content: flex-end;">
                        ${invalidColorBox}무효표<span style="color: gray; margin-left: 5px;">${invalidVotes.toFixed(3)}%</span>
                    </div>
                </div>`;
        }

        let barHtml = '';
        sortedParties.forEach(party => {
            const value = parseFloat(parties[party]);
            const color = partyColors[party] || 'rgb(200, 200, 200)';
            if (value >= MINVOTE) barHtml += `<div class="bar-segment" style="background-color: ${color}; flex-grow: ${value};"></div>`;
        });

        if (otherParties.length > 0) {
            const otherSum = otherParties.reduce((acc, cur) => acc + cur.value, 0);
            barHtml += `<div class="bar-segment other" style="flex-grow: ${otherSum};"></div>`;
        }
        if (invalidVotes > 0)  barHtml += `<div class="bar-segment invalid" style="flex-grow: ${invalidVotes};"></div>`;

        return `
            <div class="location-header">
                ${subname} <span class="location-details">${name}, ${state} 주</span>
            </div>
            <div class="location-stats">
                <div class="stat-group">
                    <div class="stat-item">
                        <span class="stat-label">인구 |</span> 
                        <span class="population-number">${formatNumber(population)}명</span>
                        <span class="rank">(${rankPopulation} / ${subdivisions.length}위)</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">면적 |</span> 
                        <span class="area-number">${formatNumber(area)}A</span>
                        <span class="rank">(${rankArea} / ${subdivisions.length}위)</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">인구 밀도 |</span> 
                        <span class="density-number">${(population / area).toFixed(3)}명/A</span>
                        <span class="rank">(${rankDensity} / ${subdivisions.length}위)</span>
                    </div>
                </div>
                <div class="events">
                    <span class="stat-label">사건</span> | ${events}
                </div>
                <div class="party-info">
                    ${partiesHtml + otherHtml}
                </div>
                <div class="bar-container">
                    ${barHtml}
                </div>
            </div>`;
    };

    // 각 행정구역에 마우스 이벤트 리스너 추가
    subdivisions.forEach(subdivision => {
        subdivision.addEventListener('mouseenter', (event) => handleMouseEnter(event, tooltip, generateTooltipContent));
        subdivision.addEventListener('mousemove', (event) => handleMouseMove(event, tooltip));
        subdivision.addEventListener('mouseleave', (event) => handleMouseLeave(event, tooltip, applyColor));
    });

    // 초기 색상 적용
    applyColor();
    
});