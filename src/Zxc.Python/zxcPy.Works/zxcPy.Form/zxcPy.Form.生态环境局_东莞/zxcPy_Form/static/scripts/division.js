
//初始镇街列表
function initTownList(tagList) {
    $("#" + tagList).empty();
    var objList = document.getElementById(tagList);
    var dictTown = getDivison_town();
    for (var key in dictTown) {
        objList.appendChild(new Option(key, key));
    }
};
//调整镇街对应村社区列表
function changeVillageList(nameTown, tagList_village) {
    $("#" + tagList_village).empty();
    var objList_v = document.getElementById(tagList_village);
    var dictTown = getDivison_town();
    var itemsTown = dictTown[nameTown];
    for (var item in itemsTown) {
        objList_v.appendChild(new Option(itemsTown[item], itemsTown[item]));
    }
};
