function querySearch(data) {
    var url = window.location.protocol + "//" + window.location.host + "/stocks/stock-suggestion/?data="+data;
    return $.get({
        url: url,
        contentType: "application/json",
        dataType: 'json'
    });
}