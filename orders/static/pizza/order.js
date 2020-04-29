// call to jQuery's ajaxSetup will cause all AJAX requests to send back the CSRF token in the custom X-CSRFTOKEN header
//https://docs.djangoproject.com/en/dev/ref/csrf/#ajax

// Acquiring the token that will on each XHRequest be set un the X-CSRFToken header
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Set the header on your AJAX request, while protecting the CSRF token from being sent to other domains
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    // beforeSend is a function which is to be run before the request is being sent, a pre-request callback function that can be used to modify the jqXHR object before it's sent
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// check local storage for preselected menu items last time
var preselection = localStorage.getItem("preselection");

function previous_selection () {
  if (localStorage.getItem("preselection") != null) {
    console.log("PRESELECTION IS: ", preselection);
    const data = new FormData();
    data.append("preselection", preselection);
    const request = new XMLHttpRequest();
    request.open('POST', '/prebasket');
    //method setRequestHeader() sets the value of an HTTP request header, must be called after calling open() but before send()
    // syntax: setRequestHeader(header, value) header: name of header whose value is to be set; value: value to set as the body of the header
    // but why is below line necessary if already called in beforeSend above?
    const csrftoken = getCookie('csrftoken');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    console.log("DATA IS: ", data);
    request.send(data);
    console.log("PRESELECTION IS: ", preselection);
    // callback function for when request completes
    request.onload = () => {
      // because I'm posting through ajax, need to load page here... that's how ajax works apparently
      var url = '/prebasket';
      //var url = "{% url 'prebasket' arg1=12345 %}".replace(/12345/, preselection.toString());
      data.append('csrfmiddlewaretoken', csrftoken);
      // fetch(url, {
      //             method : "POST",
      //             body: data,
      //             credentials: 'same-origin',
      //             headers: { "X-CSRFToken": csrftoken },
      //             // -- or --
      //             // body : JSON.stringify({
      //                 // user : document.getElementById('user').value,
      //                 // ...
      //             // })
      //         }).then(
      //             response => response.text() // .json(), etc.
      //             // same as function(response) {return response.text();}
      //         ).then(
      //             html => console.log(html)
      //         );
      // window.location.href can't do POST
      //window.location.href = url;

    };
    return false;
  }
}

previous_selection();


document.addEventListener('DOMContentLoaded', () => {


  document.querySelector('#preselect').onsubmit = () => {
    // add data to send to server with request - FormData object holds user input

    const data = new FormData();
    const inputs = document.querySelectorAll('input:valid');
    console.log(inputs); // prints node list OK
    var json = {};

    inputs.forEach(
      function(input) {
        console.log(input.value);
        console.log(input.id);
        json[input.id]=input.value;

        console.log(json);
      });

    console.log("GOT THRU TO: ", json);
    //const json = '{"result":true, "count":42}';
    //var test = JSON.parse(json); // parses data received as JSON, deserializes it into JS object

    preselection = JSON.stringify(json); // CREATES JSON string out of object or array
    //console.log("just ORIGINAL string:", json);

    //localStorage.setItem('preselection', preselection);
    data.append("preselection", preselection); // this not working. json.parse for dict maybe not needed or not right
    // Initialise new AJAX request object
    const request = new XMLHttpRequest();
    request.open('POST', '/prebasket');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); // DOESNT GET DONE
    request.send(data);
    localStorage.setItem('preselection', preselection);

    // callback function for when request completes
    request.onload = () => {
      // because I'm posting through ajax, need to load page here... that's how ajax works apparently
    //  var url = '/prebasket';
      //window.location.href = url;

    };
    return false;


  };

});
