const API_URL = "http://localhost:8000";
const GOOGLE_CLIENT_ID = "1047753082993-1iftbpo90ar6die9le8hffheu3pscik0.apps.googleusercontent.com";

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

/// Clear localstorage to force user to login again
function logoutAll() {
    localStorage.removeItem("userid");
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    localStorage.removeItem("tokenExpire");
    localStorage.removeItem("loginMethod");

    try {
        google.accounts.id.disableAutoSelect();
    } catch {
    }
}
