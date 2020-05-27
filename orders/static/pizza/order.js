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

    const inputs = document.querySelectorAll('input[type="number"]'); // for some reason selects bunch of blank input fields...
    console.log(inputs); // prints node list OK

    // ensure at least one menu item selected by customer, else stay on this site (return false)
    var i = 0;
    inputs.forEach(
      function(input) {
        i = i + input.value;
      }
    )
    if (i <=0) {
      alert("Please select at least one item.");
      return false;
    }

    var obj = [];

    inputs.forEach(
      function(input) {
        // make sure input.value, which is the selected amount, is numeric and only those inputs are selected, not the NEXT button
        if (! (isNaN(input.value)) ) {
          if (input.value > 0) {
            var price = document.querySelector('#p-'.concat(input.id)).innerHTML;
            // below only pizzas have toppings...
            try{
              topping_count = document.querySelector('#tc-'.concat(input.id)).innerHTML;
            }
            catch (err) {
              topping_count = 0;
            }

            var sid = '#s-'.concat(input.id);
            console.log(sid);
            var size;
            try{
              size = document.querySelector(sid).innerHTML;
            }
            catch {
              size = null;
            }
            //var size = document.querySelector('#s-'.concat(input.id)).innerHTML;
            console.log(size);
            var total = price * input.value;
            var dish_type = document.querySelector('#d-'.concat(input.id)).innerHTML;
            console.log(dish_type)
            obj.push({"amount": input.value, "id": input.id, "name": input.name, "size": size, "topping_count": topping_count, "price": price, "total": total, "dish_type": dish_type});
            console.log(obj);
          }

        }
      });

    var sub_orders = [];
    var pizza_orders = [];
    // go through elements
    obj.forEach((e) => {
      console.log("Dish type: ", e.dish_type);
      // if element is sub with amount = n:
      if (e.dish_type == "SUB") {
        for (var i=0; i < e.amount; i++ ) {
          // create n sub orders, each with extras (and final price) and extra count, "order" here is [dish_ID_i], e.g. [119_1], [119_2]
          sub_orders.push({"sub_order": (e.id+"_"+(i+1)), "id": e.id, "name": e.name, "size": e.size, "price": e.price, "dish_type": e.dish_type, "extras": []});
        }
      };
      if (e.dish_type == "PIZZA") {
        for (var i=0; i < e.amount; i++) {
          pizza_orders.push({"pizza_order": (e.id+"_"+(i+1)), "id": e.id, "name": e.name, "size": e.size, "price": e.price, "dish_type": e.dish_type, "toppings": []});
        }
      };
    });

    // convert native JavaScript object ot JSON-string (notation)
    var jsonStr = JSON.stringify(obj);
    var jsonStr_subs = JSON.stringify(sub_orders);
    var jsonStr_pizzas = JSON.stringify(pizza_orders);
    localStorage.setItem('preselection', jsonStr);
    localStorage.setItem('sub_orders', jsonStr_subs);
    localStorage.setItem('pizza_orders', jsonStr_pizzas);
    console.log("local storage pizza", localStorage.getItem('pizza_orders'));
    console.log("local storage subs", localStorage.getItem('sub_orders'));
    window.location.href = '/prebasket';
    return false;


    console.log("GOT THRU TO: ", jsonStr);

    return false;
  };

});
