// map_interaction.js

import { calculateSeats } from './seat_calculator.js';
import { initializeMapInteractions } from './map_interactions.js';
import partyColors from './mashup/party_color.js';
import { handleMouseEnter, handleMouseMove, handleMouseLeave } from './mouse_events.js';

const MIN_POP = 50000;
const MAX_POP = 3000000;
const MIN_DENSITY = 1;
const MAX_DENSITY = 5000;
const MIN_OPACITY = 0.15;
const MAX_OPACITY = 1;
const VOTE_GAP_DIVISOR = 40;
const MINVOTE = 1;

// 정보 상자 최소화/최대화 토글 함수
window.toggleMinimize = function () {
    const infoBox = document.getElementById('info-box');
    const minimizeButton = document.getElementById('minimize-button');
    infoBox.classList.toggle('minimized');
    minimizeButton.textContent = infoBox.classList.contains('minimized') ? '▼' : '▲';
};

document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 선택
    const subdivisions = document.querySelectorAll('.subdivision');
    const tooltip = document.getElementById('tooltip');
    const populationToggleButton = document.getElementById('population-toggle');
    const densityToggleButton = document.getElementById('density-toggle');
    const electionToggleButton = document.getElementById('election-toggle');
    const leadingPartyToggleButton = document.getElementById('leading-party-toggle');
    const toggleNamesButton = document.getElementById('toggle-names');
    const infoBox = document.getElementById('info-box');
    const mapContainer = document.getElementById('map-container');
    const map = document.getElementById('map');

    let mode = ''; // 현재 모드
    let showLeadingPartyMode = false; // 주요 정당 모드 표시 여부

    // 지도 상호작용 초기화
    initializeMapInteractions(mapContainer, map);

    // 색상 계산 함수
    const getColor = (normalized) => `rgb(250, ${Math.floor(255 * (1 - normalized))}, ${Math.floor(255 * (1 - normalized))})`;

    // 인구 기반 색상 계산 함수
    const getPopulationColor = (population) => {
        const normalized = (parseInt(population) - MIN_POP) / (MAX_POP - MIN_POP);
        return getColor(normalized);
    };

    // 인구 밀도 기반 색상 계산 함수
    const getDensityColor = (population, area) => {
        const density = population / area;
        const normalized = (density - MIN_DENSITY) / (MAX_DENSITY - MIN_DENSITY);
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
            } else if (vote > secondMaxVote) {
                secondMaxVote = vote;
            }
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
                <button id="minimize-button" onclick="toggleMinimize()">▲</button>
                <h3 style="margin-bottom: 5px; margin-top: -5px;">선거 결과
                <span style="font-size: 0.8em; margin-left: 5px; color: gray; font-weight: normal;">${event}</span>
                </h3>
                <div style="font-size: 0.8em; margin-bottom: 5px;">
                비례대표 의석수는 전체 ${SEAT}석에서 지역구 의석수를 제외한 ${SEAT - totalLocalSeats}석(이론치) 중에서 ${PER * 100}% 이상을 받은 정당에게 배분됩니다.
                </div>`;

            sortedParties.forEach(party => {
                const colorBox = `<span style="display:inline-block;width:10px;height:10px;background-color:${partyColors[party]};margin-right:3px;"></span>`;
                const percentage = ((finalSeats[party] / finalTotalSeats) * 100).toFixed(2);
                resultHTML += `
                    <div style="display: flex; align-items: center; margin: 3px 0;">
                        <p style="line-height: 1.2; margin: 0; flex-grow: 1;">
                            ${colorBox}${party} ${finalSeats[party]}석
                            <span style="font-size: 0.7em;">${percentage}% (${proportionalPartySeats[party] || 0} + ${localPartySeats[party] || 0})</span>
                        </p>
                        <div style="background-color: ${partyColors[party]}; height: 10px; width: ${percentage}%;"></div>
                    </div>`;
            });

            resultHTML += `<p style="font-weight:bold; margin-top: 5px; margin-bottom: 2px; font-size: 1.2em;">
                            ${finalTotalSeats}석 <span style="font-size: 1em;">(비례 ${totalProportionalSeats}석 + 지역구 ${totalLocalSeats}석)</span></p>`;
            infoBox.innerHTML = resultHTML;
        } else {
            infoBox.style.display = 'none';
        }
    };

    // 모드 토글 함수
    const toggleMode = (newMode) => {
        mode = newMode;
        displayElectionResults(mode === 'election');
        applyColor();
        leadingPartyToggleButton.style.display = mode === 'election' ? 'block' : 'none';
    };

    // 이벤트 리스너 추가
    populationToggleButton.addEventListener('click', () => toggleMode('population'));
    densityToggleButton.addEventListener('click', () => toggleMode('density'));
    electionToggleButton.addEventListener('click', () => toggleMode('election'));

    leadingPartyToggleButton.addEventListener('click', () => {
        showLeadingPartyMode = !showLeadingPartyMode;
        applyColor();
    });

    toggleNamesButton.addEventListener('click', () => {
        document.querySelectorAll('.province-name').forEach(name => name.classList.toggle('hidden'));
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
                partiesHtml += `
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 4px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: ${color}; margin-right: 5px;"></div>
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
            otherHtml += `
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(200, 200, 200); margin-right: 5px;"></div>
                        기타<span style="color: gray; margin-left: 5px;">${otherSum.toFixed(3)}% (${MINVOTE}% 미만)</span>
                    </div>
                    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden; 
                                text-overflow: ellipsis; flex-grow: 1; min-width: 0; margin: 0 5px; font-size: 12px;">
                        <div style="width: 12px; height: 12px; background-color: rgb(0, 0, 0); margin-right: 5px;"></div>
                        무효표<span style="color: gray; margin-left: 5px;">${invalidVotes.toFixed(3)}%</span>
                    </div>
                </div>`;
        }

        let barHtml = '';
        sortedParties.forEach(party => {
            const value = parseFloat(parties[party]);
            const color = partyColors[party] || 'rgb(200, 200, 200)';
            if (value >= MINVOTE) {
                barHtml += `<div style="background-color: ${color}; height: 20px; width: ${value}%;"></div>`;
            }
        });

        if (otherParties.length > 0) {
            const otherSum = otherParties.reduce((acc, cur) => acc + cur.value, 0);
            barHtml += `<div style="background-color: rgb(200, 200, 200); height: 20px; width: ${otherSum}%;"></div>`;
        }

        if (invalidVotes > 0) {
            barHtml += `<div style="background-color: black; height: 20px; width: ${invalidVotes}%;"></div>`;
        }

        return `
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 3px; margin-left: 3px;">
                ${subname}<span style="font-size: 0.6em; color: gray; margin-left: 5px;">${name}, ${state} 주</span>
            </div>
            <div style="font-size: 1em; margin-left: 3px;">
                <div>면적 | ${formatNumber(area)}A <span style="font-size: 0.8em; color: gray; margin-left: 5px;">(${rankArea}위)</span></div>
                <div>인구 | ${formatNumber(population)}명 <span style="font-size: 0.8em; color: gray; margin-left: 5px;">(${rankPopulation}위)</span></div>
                <div>인구 밀도 | ${(population / area).toFixed(3)}명/A <span style="font-size: 0.8em; color: gray; margin-left: 5px;">(${rankDensity}위)</span></div>
                <div style="font-size: 0.8em; color: gray; margin-top: 2px;">사건 | ${events}</div>
                <div style="margin-left: 10px; margin-top: 2px;">${partiesHtml + otherHtml}</div>
                <div style="display: flex; margin-top: 10px; height: 20px; border: 1px solid #ccc;">${barHtml}</div>
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