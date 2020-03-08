
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function Vertify() {
    if (getCookie("MetaInfo") == 0) {
        return true
    } else {
        return false
    }
}

function SetStorage(document) {
    sessionStorage.setItem("FirstName", "{{ FirstName }}");
    sessionStorage.setItem("OtherNames", "{{ OtherNames }}");
    sessionStorage.setItem("Image", "{{ Image }}");
    sessionStorage.setItem("Info", "{{ Info }}");
    sessionStorage.setItem("Sex", "{{ Sex }}");
    sessionStorage.setItem("Birthday", "{{ Birthday }}");
    sessionStorage.setItem("Year", "{{ Year }}");
}

function FillIn(document) {
    if (Object.is(Vertify(), true)) {
        sessionStorage.setItem("FirstName", "{{ FirstName }}");
        sessionStorage.setItem("OtherNames", "{{ OtherNames }}");
        sessionStorage.setItem("Image", "{{ Image }}");
        sessionStorage.setItem("Info", "{{ Info }}");
        sessionStorage.setItem("Sex", "{{ Sex }}");
        sessionStorage.setItem("Birthday", "{{ Birthday }}");
        sessionStorage.setItem("Year", "{{ Year }}");
    }
    document.getElementById("Name").innerHTML = sessionStorage.getItem('FirstName') + " " + sessionStorage.getItem('OtherNames');
    document.getElementById("Info").innerHTML = sessionStorage.getItem('Info');
    document.getElementById("Sex").innerHTML = sessionStorage.getItem('Sex');
    document.getElementById("Birthday").innerHTML = sessionStorage.getItem('Birthday');
    document.getElementById("Year").innerHTML = sessionStorage.getItem('Year');
}



function TypeIn(document) {
    if (Object.is(Vertify(), true)) {
        SetStorage(document)
    }

}