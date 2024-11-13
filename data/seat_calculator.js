// seat_calculator.js (의석수 계산)

export function calculateSeats(subdivisions) {
    const SEAT = 1500; // 총 의석수 (지역구 의석수 + 비례대표 의석수)
    const PER = 0.002; // 득표 퍼센티지 기준
    const totalPartyVotes = {}; // 정당별 총 득표 인구수 저장 객체
    const localPartySeats = {}; // 지역구 의석수 저장 객체
    let totalPopulation = 0; // 전체 인구수

    // 각 행정구역에 대해 반복
    subdivisions.forEach(subdivision => {
        const population = parseInt(subdivision.getAttribute('data-population'), 10); // 인구 정보 가져오기
        const parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기

        totalPopulation += population; // 총 인구수 계산
        const totalVotes = Object.values(parties).reduce((a, b) => a + b, 0); // 총 득표수 계산

        // 각 정당의 득표 퍼센티지 및 해당 행정구역에서의 득표 인구수 계산
        for (const [party, votes] of Object.entries(parties)) {
            const partyPercentage = votes / totalVotes;
            const votesForParty = population * partyPercentage; // 해당 행정구역에서 해당 정당 득표 인구수 계산
            totalPartyVotes[party] = (totalPartyVotes[party] || 0) + votesForParty; // 정당별 총 득표 인구수 합산
        }

        // 특정 득표 퍼센티지 이하인 정당 제거
        for (const party in totalPartyVotes) {
            if ((totalPartyVotes[party] / totalPopulation) < PER) {
                delete totalPartyVotes[party];
            }
        }

        // 지역구 의석수 계산: 최대 득표 정당에게 1석 부여
        const maxVotes = Math.max(...Object.values(parties));
        for (const [party, votes] of Object.entries(parties)) {
            if (votes === maxVotes) localPartySeats[party] = (localPartySeats[party] || 0) + 1;
        }
    });

    const proportionalSeats = SEAT - subdivisions.length; // 비례대표 의석수
    const proportionalPartySeats = {}; // 비례대표 의석수 저장 객체
    const percentage = {}; // 득표 퍼센티지 저장 객체

    // 정당별 득표 퍼센티지 계산
    for (const [party, votes] of Object.entries(totalPartyVotes)) percentage[party] = votes / totalPopulation;

    const totalPercentage = Object.values(percentage).reduce((a, b) => a + b, 0); // 총 득표 퍼센티지

    // 비례대표 의석수 계산
    for (const [party, percent] of Object.entries(percentage))  proportionalPartySeats[party] = Math.round(proportionalSeats * (percent / totalPercentage));

    const finalSeats = {}; // 최종 의석수 저장 객체

    // 비례대표 의석수 합산
    for (const [party, seats] of Object.entries(proportionalPartySeats))  finalSeats[party] = (localPartySeats[party] || 0) + seats;

    // 지역구 의석수 합산
    for (const [party, seats] of Object.entries(localPartySeats)) if (!finalSeats[party]) finalSeats[party] = seats;

    // 의석수가 0인 정당 제거
    for (const party in finalSeats) if (finalSeats[party] === 0) delete finalSeats[party];

    return { SEAT, PER, finalSeats, proportionalPartySeats, localPartySeats }; // 최종 결과 반환
}