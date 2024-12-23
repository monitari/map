from collections import defaultdict

output_file = "data/mashup/province_info.txt"

info = {
    "아젠타, 테트라 주, 15610, 256870",
    "테트리다모스, 테트라 주, 4004, 538756",
    "츠비키, 아이리카 주, 64770, 9513084",
    "하르바트, 아이리카 주, 61565, 10837747",
    "테타, 테트라 주, 1139, 948012",
    "아칸타, 테트라 주, 13030, 360397",
    "메르네, 아이리카 주, 47346, 18595416",
    "리에다, 미네바 주, 17833, 945311",
    "테트리비제모스, 테트라 주, 6028, 354321",
    "파르티엔타, 테트라 주, 14983, 342456",
    "아이리카, 아이리카 주, 59364, 39251427",
    "마링고, 바니카-메고차 주, 35353, 167891",
    "미바나, 미네바 주, 8748, 2573904",
    "에디아다, 미네바 주, 30323, 548009",
    "미에고, 바니카-메고차 주, 2360, 1561469",
    "솔바, 미네바 주, 1386, 3851321",
    "이벤토, 바니카-메고차 주, 54726, 231480",
    "유칸타, 테트라 주, 13125, 380445",
    "메고리, 바니카-메고차 주, 34012, 216789",
    "아바나, 미네바 주, 3786, 2249110",
    "아브레, 아이리카 주, 34582, 9851850",
    "민마나, 미네바 주, 2734, 1695675",
    "민고, 바니카-메고차 주, 56790, 267333",
    "모에바, 미네바 주, 12252, 2648183",
    "유프란, 미치바 주, 50235, 210355",
    "바니아, 바니카-메고차 주, 19364, 204567",
    "코에가, 미네바 주, 7337, 2767890",
    "메가, 미네바 주, 4161, 1581238",
    "만토, 미네바 주, 560, 1465853",
    "피에트라, 아이리카 주, 73821, 13553084",
    "아리나, 미네바 주, 1631, 1491306",
    "미츠비, 미치바 주, 1704, 4984629",
    "미치바, 미치바 주, 8791, 2331284",
    "나릴로, 미치바 주, 41071, 801653",
    "아신가, 안텐시 주, 28959, 1630567",
    "베아골, 세그레차 주, 46999, 456789",
    "미느리오, 하파차 주, 63404, 4855486",
    "산시아고, 미치바 주, 37427, 867810",
    "키골, 세그레차 주, 7829, 644226",
    "세골, 세그레차 주, 2633, 2344813",
    "페아골, 세그레차 주, 15326, 754183",
    "메초오비카, 아이리카 주, 96232, 23570738",
    "리에골, 세그레차 주, 49150, 436178",
    "시세디, 안텐시 주, 5867, 3377913",
    "오고이모, 하파차 주, 110187, 3940649",
    "키르가, 안텐시 주, 71130, 3612571",
    "오브니, 도마니 주, 19049, 3967305",
    "우프레나, 미치바 주, 25774, 2457032",
    "비에노, 안텐시 주, 54822, 1380888",
    "미골, 세그레차 주, 8397, 592467",
    "메링골, 세그레차 주, 19423, 367338",
    "알고, 미치바 주, 31745, 432560",
    "메즈노, 안텐시 주, 47463, 1235958",
    "메고이오, 미치바 주, 39435, 542567",
    "키에오, 그미즈리 주, 31075, 6249109",
    "티레니오, 하파차 주, 60705, 17159813",
    "파시벤토, 하파차 주, 112034, 6867660",
    "하롱골, 세그레차 주, 37143, 367890",
    "케릴티, 도마니 주, 30109, 2973010",
    "아스타나, 하파차 주, 22520, 10465110",
    "바스바드, 도마니 주, 40647, 4076893",
    "민마, 베고차 주, 2296, 3965915",
    "모반토, 베고차 주, 19190, 2832567",
    "아핀고, 안텐시 주, 44648, 1048183",
    "모베이, 베고차 주, 26097, 1719494",
    "미톤노, 그미즈리 주, 22755, 8054321",
    "테안타, 베고차 주, 877, 2731852",
    "에링고, 도마니 주, 5505, 5440468",
    "가안, 도마니 주, 2183, 2450110",
    "메깅고, 그미즈리 주, 16524, 7268147",
    "그미즈리, 그미즈리 주, 7156, 13085184",
    "메옹, 도마니 주, 646, 546281",
    "호오토, 그미즈리 주, 25742, 8554321",
    "브고홀, 도마니 주, 16647, 843210",
    "리안토, 베고차 주, 23923, 1666890",
    "산세오, 하파차 주, 57483, 14604567",
    "오고소, 베고차 주, 16726, 2169613",
    "트롱페이, 베고차 주, 21503, 1445019",
    "바티아, 베고차 주, 1130, 2948395",
    "모호보드, 안텐시 주, 85052, 709112",
    "오크모, 그미즈리 주, 33745, 6354041",
    "이베이, 베고차 주, 18482, 1049483",
    "페린, 베고차 주, 17663, 1783819",
    "아센시, 그미즈리 주, 18170, 7696287",
    "모옹홀, 도마니 주, 13621, 550783",
    "메고기, 도마니 주, 24440, 1053931",
    "페아그, 그미즈리 주, 22777, 9654381",
    "파미즈, 림덴시 주, 20188, 3134301",
    "커피, 도마니 주, 22279, 2369303",
    "펜보드, 림덴시 주, 25812, 1150321",
    "스피가, 림덴시 주, 17773, 2419239",
    "아르고, 림덴시 주, 5354, 4379408",
    "모호카, 림덴시 주, 39070, 467139",
    "하싱고, 하파차 주, 61294, 5967177",
    "즈조이, 도마니 주, 21355, 1035838",
    "아린키고, 하파차 주, 104498, 2557860",
    "모리고, 림덴시 주, 5766, 2254321",
    "비엥고, 하파차 주, 52859, 4301297",
    "메바치, 림덴시 주, 18934, 2510012",
    "레링가, 베고차 주, 6712, 1232567",
    "린토카, 림덴시 주, 31773, 495485",
    "메르노, 그라나데 주, 22995, 604940",
    "라토카, 림덴시 주, 31120, 561934",
    "안트로아싱가, 카리아-로 주, 7080, 3490123",
    "낙소, 림덴시 주, 20361, 2134201",
    "모잉고, 하파차 주, 51149, 5143210",
    "보어, 림덴시 주, 14841, 434428",
    "보빈, 림덴시 주, 12440, 1721567",
    "보피노, 그라나데 주, 19203, 451938",
    "세오고, 림덴시 주, 13288, 1854321",
    "안트리포어, 포어 주, 16728, 579103",
    "시안, 림덴시 주, 12778, 972274",
    "하르고, 하파차 주, 4685, 341036",
    "피고모싱고메고차바데다, 카리아-로 주, 41301, 1971401",
    "노베라니나, 카리아-로 주, 1153, 871901",
    "라간, 포어 주, 3787, 639914",
    "미베이토메고차피덴타, 카리아-로 주, 57100, 2067860",
    "안파, 포어 주, 8036, 935869",
    "아르테, 포어 주, 871, 2150499",
    "세가, 포어 주, 3503, 1140691",
    "페카그라나다, 그라나데 주, 19377, 545938",
    "아르모텐타, 카리아-로 주, 26913, 1516108",
    "테사, 포어 주, 4973, 1345411",
    "그라나다, 그라나데 주, 6241, 1284631",
    "오르도기, 포어 주, 7727, 761932",
    "메네트리포어, 포어 주, 46344, 741317",
    "안파키, 그라나데 주, 7720, 418591",
    "아파그라나다, 그라나데 주, 17588, 379483",
    "안파기, 메세기 주, 37367, 651835",
    "나다이, 메세기 주, 7343, 784184",
    "크라나, 메세기 주, 14967, 559913",
    "크레이, 메세기 주, 16987, 1659311",
    "포크란, 메세기 주, 1704, 3754815",
    "옹피오, 메세기 주, 26655, 585509",
    "메세기, 메세기 주, 30948, 1696380"
}

provinceinfo = {
    "그라나데": {
        "안파키": {"구역1"},
        "아파그라나다": {"구역1"},
        "페카그라나다": {"구역1"},
        "그라나다": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7"},
        "보피노": {"구역1"},
        "메르노": {"구역1"},
    },
    "바니카-메고차": {
        "바니아": {"구역1"},
        "미에고": {"구역1", "구역2", "구역3", "구역4"},
        "메고리": {"구역1"},
        "민고": {"구역1"},
        "이벤토": {"구역1"},
        "마링고": {"구역1"},
    },
    "베고차": {
        "모베이": {"구역1", "구역2", "구역3", "구역4"},
        "트롱페이": {"구역1", "구역2", "구역3", "구역4"},
        "바티아": {"구역1", "구역2", "구역3", "구역4"},
        "이베이": {"구역1", "구역2", "구역3"},
        "페린": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "리안토": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "오고소": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "민마": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7"},
        "테안타": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7"},
        "모반토": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8"},
        "레링가": {"구역1", "구역2", "구역3"},
    },
    "세그레차": {
        "하롱골": {"구역1"},
        "미골": {"구역1", "구역2"},
        "메링골": {"구역1"},
        "세골": {"구역1", "구역2", "구역3", "구역4", "구역5",},
        "키골": {"구역1", "구역2"},
        "리에골": {"구역1"},
        "페아골": {"구역1", "구역2"},
        "베아골": {"구역1"},
    },
    "아이리카": {
        "메초오비카": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10",
                "구역11", "구역12", "구역13", "구역14", "구역15", "구역16", "구역17", "구역18", "구역19", "구역20",
                "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28", "구역29", "구역30",
                "구역31", "구역32", "구역33", "구역34", "구역35", "구역36", "구역37", "구역38", "구역39", "구역40",
                "구역41",
        },
        "아브레": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12"},
        "피에트라": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12",
                "구역13", "구역14", "구역15", "구역16", "구역17", "구역18", "구역19"},
        "아이리카": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10",
                "구역11", "구역12", "구역13", "구역14", "구역15", "구역16", "구역17", "구역18", "구역19", "구역20",
                "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28", "구역29", "구역30",
                "구역31", "구역32", "구역33", "구역34", "구역35", "구역36", "구역37", "구역38",
        },
        "메르네": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12",
                "구역13", "구역14", "구역15", "구역16", "구역17", "구역18", "구역19"},
        "츠비키": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13"},
        "하르바트": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13",
                "구역14", "구역15", "구역16", "구역17", "구역18", "구역19", "구역20"},
    },
    "안텐시": {
        "모호보드": {"구역1"},
        "아핀고": {"구역1", "구역2"},
        "비에노": {"구역1", "구역2"},
        "시세디": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14"},
        "메즈노": {"구역1", "구역2"},
        "아신가": {"구역1", "구역2", "구역3"},
        "키르가": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14",
                "구역15", "구역16", "구역17", "구역18"},
    },
    "테트라": {
        "아젠타": {"구역1"},
        "아칸타": {"구역1"},
        "파르티엔타": {"구역1"},
        "유칸타": {"구역1"},
        "테트리다모스": {"구역1"},
        "테트리비제모스": {"구역1"},
        "테타": {"구역1", "구역2"},
    },
    "카리아-로": {
        "노베라니나": {"구역1", "구역2"},
        "아르모텐타": {"구역1", "구역2", "구역3", "구역4"},
        "피고모싱고메고차바데다": {"구역1", "구역2", "구역3", "구역4"},
        "미베이토메고차피덴타": {"구역1", "구역2", "구역3", "구역4"},
        "안트로아싱가": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7"},
    },
    "포어": {
        "메네트리포어": {"구역1", "구역2"},
        "안트리포어": {"구역1"},
        "라간": {"구역1", "구역2", "구역3"},
        "안파": {"구역1", "구역2", "구역3", "구역4"},
        "테사": {"구역1", "구역2", "구역3", "구역4"},
        "아르테": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8"},
        "세가": {"구역1", "구역2"},
        "오르도기": {"구역1", "구역2", "구역3", "구역4"},
    },
    "하파차": {
        "파시벤토": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14",
                "구역15", "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22",},
        "오고이모": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",},
        "미느리오": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                 "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28", "구역29"},
        "산세오": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28", "구역29", "구역30", "구역31", "구역32"},
        "아스타나": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                 "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24"
        },
        "티레니오": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                 "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28", "구역29", "구역30",
                    "구역31", "구역32", "구역33", "구역34", "구역35", "구역36", "구역37", "구역38", "구역39", "구역40", "구역41", "구역42", "구역43", "구역44", "구역45",
                    "구역46", "구역47", "구역48", "구역49",},
        "비엥고": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15", "구여16", "구역17", "구역18"},
        "아린키고": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12"},
        "하싱고": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                 "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24", "구역25"},
        "모잉고": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                 "구역16", "구역17", "구역18", "구역19", "구역20", "구역21", "구역22", "구역23", "구역24", "구역25", "구역26", "구역27", "구역28"},
        "하르고": {"구역1"},
    },
    "그미즈리": {
        "오크모": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14",},
        "페아그": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",},
        "미톤노": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11",},
        "아센시": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12",},
        "그미즈리": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15", "구역16"},
        "메깅고": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12",},
        "키에오": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11",},
        "호오토": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",
                "구역16", "구역17", "구역18", "구역19",},
    },
    "도마니": {
        "즈조이": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6"},
        "커피": {"구역1", "구역2", "구역3", "구역4"},
        "메고기": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "에링고": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "바스바드": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "케릴티": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7"},
        "오브니": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "모옹홀": {"구역1"},
        "브고홀": {"구역1", "구역2"},
        "가안": {"구역1", "구역2", "구역3", "구역4",},
        "메옹": {"구역1"},
    },
    "림덴시": {
        "아르고": {"구역1", "구역2", "구역3", "구역4"},
        "펜보드": {"구역1", "구역2"},
        "스피가": {"구역1", "구역2", "구역3"},
        "파미즈": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "메바치": {"구역1", "구역2", "구역3"},
        "모리고": {"구역1", "구역2", "구역3", "구역4"},
        "라토카": {"구역1"},
        "린토카": {"구역1"},
        "낙소": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "보빈": {"구역1", "구역2", "구역3", "구역4"},
        "세오고": {"구역1", "구역2", "구역3", "구역4"},
        "모호카": {"구역1"},
        "보어": {"구역1"},
        "시안": {"구역1", "구역2", "구역3"},
    },
    "메세기": {
        "나다이": {"구역1", "구역2"},
        "옹피오": {"구역1"},
        "크라나": {"구역1"},
        "메세기": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6",},
        "포크란": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8"},
        "크레이": {"구역1", "구역2", "구역3", "구역4", "구역5",},
        "안파기": {"구역1", "구역2"},
    },
    "미치바": {
        "메고이오": {"구역1"},
        "알고": {"구역1"},
        "우프레나": {"구역1", "구역2", "구역3", "구역4", "구역5",},
        "미츠비": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7", "구역8"},
        "미치바": {"구역1", "구역2", "구역3", "구역4", "구역5",},
        "나릴로": {"구역1", "구역2"},
        "산시아고": {"구역1", "구역2"},
        "유프란": {"구역1"},
    },
    "미네바": {
        "아리나": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7",},
        "만토": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역6",},
        "메가": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7",},
        "코에가": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7",},
        "민마나": {"구역1", "구역2", "구역3", "구역4",},
        "모에바": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6"},
        "아바나": {"구역1", "구역2", "구역3", "구역4", "구역5"},
        "솔바": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7",
               "구역8", "구역9", "구역10", "구역11", "구역12", "구역13", "구역14", "구역15",},
        "미바나": {"구역1", "구역2", "구역3", "구역4", "구역5", "구역6", "구역7",},
        "에디아다": {"구역1"},
        "리에다": {"구역1", "구역2"},
    }
}

def parse_info(info):
    parsed_data = []
    for entry in info:
        province, state, area, population = entry.split(", ")
        state = state.replace(" 주", "")
        parsed_data.append({
            "province": province,
            "state": state,
            "area": int(area),
            "population": int(population)
        })
    return parsed_data

def sort_and_group_data(parsed_data, provinceinfo):
    grouped_data = defaultdict(lambda: defaultdict(list))
    
    for item in parsed_data:
        grouped_data[item["state"]][item["province"]].append(item)
    
    for state in grouped_data:
        for province in grouped_data[state]:
            grouped_data[state][province].sort(key=lambda x: x["area"])
    
    sorted_data = []
    for state in sorted(grouped_data.keys()):
        for province in sorted(grouped_data[state].keys()):
            if province in provinceinfo.get(state, {}):
                num_subprovinces = len(provinceinfo[state][province])
                for item in grouped_data[state][province]:
                    for subprovince in sorted(provinceinfo[state][province]):
                        sorted_data.append({
                            "province": item["province"],
                            "state": state,
                            "subprovince": subprovince,
                            "area": item["area"] // num_subprovinces,
                            "population": item["population"] // num_subprovinces
                        })
    return sorted_data

def write_sorted_data(sorted_data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for item in sorted_data:
            sub = item["province"] + item["subprovince"] # 구별을 위해
            file.write(f"{sub}, {item['province']}, {item['state']}, {item['area']}, {item['population']}\n")

def main():
    parsed_data = parse_info(info)
    sorted_data = sort_and_group_data(parsed_data, provinceinfo)
    write_sorted_data(sorted_data, output_file)
    print(output_file, "파일을 최신 데이터로 업데이트하였습니다.")

if __name__ == "__main__":
    main()