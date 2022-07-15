function querySearch(callback) {
    var url = window.location.protocol + "//" + window.location.host + "/stocks/stock-suggestion";
    return $.get({
        url: url,
        contentType: "application/json",
        dataType: 'json'
    });
}