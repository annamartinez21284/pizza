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
  if (preselection != null) {
    console.log("PRESELECTION IS: ", preselection);
    window.location.href = '/prebasket';
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

    var obj = [];

    inputs.forEach(
      function(input) {
        // make sure input.value, which is the selected amount, is numeric and only those inputs are selected, not the NEXT button
        if (! (isNaN(input.value))) {
          if (input.value > 0) {
            var price = document.querySelector('#p-'.concat(input.id)).innerHTML;
            var topping_count = document.querySelector('#tc-'.concat(input.id)).innerHTML;
            var sid = '#s-'.concat(input.id);
            console.log(sid);
            var size = document.querySelector(sid).innerHTML; // not working... werid
            //var size = document.querySelector('#s-'.concat(input.id)).innerHTML;
            console.log(size);
            total = price * input.value;
            obj.push({"amount": input.value, "id": input.id, "name": input.name, "size": size, "topping_count": topping_count, "price": price, "total": total});
            console.log(obj);
          }
        }
      });

    // convert native JavaScript object ot JSON-string (notation)
    var jsonStr = JSON.stringify(obj);


    console.log("GOT THRU TO: ", jsonStr);

    data.append("preselection", jsonStr);
    // Initialise new AJAX request object
    const request = new XMLHttpRequest();
    request.open('POST', '/prebasket');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.send(data);
    localStorage.setItem('preselection', jsonStr);

    // callback function for when request completes
    request.onload = () => {
      // because I'm posting through ajax, need to load page here... that's how ajax works apparently
      window.location.href = '/prebasket';
    };
    return false;
  };

});
