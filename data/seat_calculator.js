// seat_calculator.js (의석수 계산)

export function calculateSeats(subdivisions) {
    const results = {}; // 선거 결과 저장 객체
    let percentage = 0; // 득표 퍼센테이지

    subdivisions.forEach(function (subdivision) {
        const population = parseInt(subdivision.getAttribute('data-population'), 10); // 인구 정보 가져오기
        const parties = JSON.parse(subdivision.getAttribute('data-parties')); // 정당 정보 가져오기

        // 총 인구수 계산
        let totalPopulation = 0;
        subdivisions.forEach(function (subdivision) {
            totalPopulation += parseInt(subdivision.getAttribute('data-population'), 10);
        });

        // 각 정당의 득표 퍼센테이지 계산
        const totalVotes = Object.values(parties).reduce((a, b) => a + b, 0); // 총 득표수 계산
        const partyPercentages = {};
        for (let party in parties) {
            partyPercentages[party] = (parties[party] / totalVotes) * 100; // 득표 퍼센테이지 계산
        }

        // 각 정당의 의석수 계산
        const seats = {};
        for (let party in partyPercentages) {
            const votes = (partyPercentages[party] / 100) * totalVotes; // 정당의 득표수 계산
            seats[party] = Math.round(votes * population / totalPopulation * 100); // 의석수 계산
            percentage += seats[party]; // 총 의석수 계산
        }

        // 결과 저장
        results[subdivision.getAttribute('data-name')] = seats;
    });

    const partySeats = {}; // 정당별 의석수 저장 객체 (비례대표 의석수)
    for (const province in results) {
        const seats = results[province]; 
        for (let party in seats) {
            if (seats[party] > 0) { // 의석수가 0보다 큰 경우만
                if (partySeats[party]) partySeats[party] += seats[party]; // 이미 있는 경우 더하기
                else partySeats[party] = seats[party]; // 없는 경우 새로 만들기
            }
        }
    }

    const localPartySeats = {}; // 지역구 의석수 저장 객체
    // 지역구 의석수 계산, 해당 행정구역에서 가장 많은 득표를 한 정당에게 1석씩 주기
    subdivisions.forEach(function (subdivision) {
        const parties = JSON.parse(subdivision.getAttribute('data-parties'));
        const maxVotes = Math.max(...Object.values(parties));
        for (let party in parties) {
            if (parties[party] === maxVotes) {
                if (localPartySeats[party]) localPartySeats[party] += 1;
                else localPartySeats[party] = 1;
            }
        }
    });

    // 0.5% 미만 정당을 버리기
    for (let party in partySeats) 
        if (partySeats[party] / percentage < 0.005) delete partySeats[party];

    // 비례대표 의석수 계산
    const semitotalSeats = Object.values(partySeats).reduce((a, b) => a + b, 0);
    const proportionalSeats = 1000 - subdivisions.length; // 비례대표 의석수
    const proportionalPartySeats = {}; // 비례대표 의석수 저장 객체
    for (let party in partySeats) {
        const percentage = partySeats[party] / semitotalSeats;
        proportionalPartySeats[party] = Math.round(percentage * proportionalSeats);
    }

    const finalSeats = {};
    // 최종 의석수 계산
    for (let party in proportionalPartySeats) {
        if (localPartySeats[party]) finalSeats[party] = localPartySeats[party] + proportionalPartySeats[party];
        else finalSeats[party] = proportionalPartySeats[party];
    }
    for (let party in localPartySeats) if (!finalSeats[party]) finalSeats[party] = localPartySeats[party];

    return {finalSeats, proportionalPartySeats, localPartySeats};
}