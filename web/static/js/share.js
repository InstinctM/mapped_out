const API_URL = "http://127.0.0.1:8000"

function httpGet(url, data, callback) {
    $.ajax({
        type: 'GET',
        url: url,
        crossDomain: true,
        beforeSend: function(xhr) {
            xhr.withCredentials = true;
        },
        data: data,
        success: callback,
    });
}
