const API_URL = "http://127.0.0.1:8000"

function httpGet(url, data, callback) {
    $.ajax({
        method: 'GET',
        url: url,
        crossDomain: true,
        beforeSend: function(xhr) {
            xhr.withCredentials = true;
        },
        data: data,
        success: callback,
    });
}


function httpPost(url, data, callback) {
    $.ajax({
        method: 'POST',
        url: url,
        crossDomain: true,
        beforeSend: function(xhr) {
            xhr.withCredentials = true;
        },
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        dataType: "json",
        success: callback,
    });
}
