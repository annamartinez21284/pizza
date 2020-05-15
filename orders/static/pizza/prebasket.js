//CSRFTOKEN SETUP NOT NEEDED - ONLY FOR AJAX, BUT ENDED UP NOT USING

// // Acquiring the token that will on each XHRequest be set un the X-CSRFToken header
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');
//
// // Set the header on your AJAX request, while protecting the CSRF token from being sent to other domains
// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
// $.ajaxSetup({
//     // beforeSend is a function which is to be run before the request is being sent, a pre-request callback function that can be used to modify the jqXHR object before it's sent
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });


function load_basket () {
  if (localStorage.getItem("preselection") != null) {
    preselection = localStorage.getItem("preselection");
    // preselection is (or at least it should be) a string in JSON notation

    var json = JSON.parse(preselection);
    console.log("THIS IS PARSED BASKET: ", json);
    json.forEach(function(e) {
      const tr = document.createElement('tr');
      const name = document.createElement('td');
      const size = document.createElement('td');
      const price = document.createElement('td');
      const amount = document.createElement('td');
      const subtotal = document.createElement('td');
      name.setAttribute("style", "font-size:18px");
      size.setAttribute("style", "font-size:18px");
      price.setAttribute("style", "font-size:16px");
      amount.setAttribute("style", "font-size:16px");

      name.innerHTML = e.name;
      // display size if item has size
      if (e.size != null) {size.innerHTML = e.size;};
      price.innerHTML = e.price;
      //price.setAttribute("class", "price"); - don't do this because otherwise calculate_total will pick these up and add to total
      amount.innerHTML = e.amount.concat(" x");
      // display subtotal with 2 decimal places
      subtotal.innerHTML = (e.amount * e.price).toFixed(2);
      // set class attribute to price so calculate_total picks up these
      subtotal.setAttribute("class", "price");
      subtotal.setAttribute("id", ("subtotal_"+e.id)) // needs THE SIZE TOO, otherwise may not be unique - used anywhere?

      tr.appendChild(name);
      tr.appendChild(size);
      tr.appendChild(price);
      tr.appendChild(amount);
      tr.appendChild(subtotal);
      document.querySelector('#items').appendChild(tr);

      // if item is a pizza with n>0 toppings, add extra line per pizza with n topping select menus
      if (e.topping_count > 0) {
        // add e.amount rows
        for (let i = 0; i< e.amount; i++) {
          const tr = document.createElement('tr'); // make sure no scope issue here
          tr.setAttribute("class", "toppingline");
          document.querySelector('#items').appendChild(tr);
          const td = document.createElement('td');
          td.innerHTML = "Choose topping(s) for Pizza #" + (i+1);
          tr.appendChild(td);
          // in that row add 1 td containing 1 select menu each for each pizza (i)
          for (let j = 0; j < e.topping_count; j++) {
            const td = document.createElement('td');
            td.setAttribute("id", ("toppings_"+e.id+"_"+(i+1)));
            const toppings = document.querySelector('select');
            const select = toppings.cloneNode(true);
            select.removeAttribute("hidden");
            select.setAttribute("id", ("toppings_"+e.id+"_"+(i+1)+"_"+(j+1)));
            const st = document.createElement('option');
            st.setAttribute("selected", "true");
            st.setAttribute("disabled", "true");
            st.setAttribute("value", ""); // n>ecessary so user is forced to select topping due to required HTML attribute in <select>
            st.innerHTML = "Select Topping " + (j+1) + ":";
            select.prepend(st);
            if (j == 4) {
              //add None (optional) to topping selection
            }
            td.appendChild(select);
            tr.appendChild(td);

          }
        }
      };

      // if Sub, add 1 line per sub, and use AJAX to update price depending on # extra boxes ticked
      if (e.dish_type == "SUB") {
        for (let i=0; i < e.amount; i++){
          const tr = document.createElement('tr');
          tr.setAttribute("class", "toppingline");
          document.querySelector('#items').appendChild(tr);
          const td1 = document.createElement('td');
          const td2 = document.createElement('td');
          td2.setAttribute("colspan", "5");
          td1.innerHTML = "Extra(s) ($0.50) for Sub #" + (i+1);
          const extra_div = document.querySelector('#extras');
          // checkboxes is a hidden div tag in prebasket.html. Using it as template: copy, unhide, set ID & name
          const checkboxes = extra_div.cloneNode(true);
          checkboxes.removeAttribute("hidden"); // unhide it
          checkboxes.setAttribute("id", ("extras_"+e.id+"_"+(i+1))); // this needed to record upon submission in JSON object
          checkboxes.setAttribute("name", "checkboxes");

          td2.appendChild(checkboxes);
          tr.appendChild(td1);
          tr.appendChild(td2);
        }
      }


    });
  }

  // if nothing is in basket (i.e. in localStorage)
  else {
    window.location.href = '/';
  }

}

function calculate_total () {

  var prices = document.querySelectorAll('.price');
  console.log(prices);
  var total = 0;
  for (let i = 0; i < prices.length; i++) {
    console.log(parseFloat(prices[i].innerText));
    total = total + parseFloat(prices[i].innerText);
  }
  console.log("TOTAL is: ", total);
  const td = document.querySelector('#total');
  //td.setAttribute("class", "price");
  td.innerHTML = total.toFixed(2);
}


document.addEventListener('DOMContentLoaded', () => {
  load_basket();
  console.log("basket loaded, now calc total?");
  calculate_total();

  // select all divs (name=checkboxes) with checkbox menu
  var divs = document.getElementsByName("checkboxes");
  divs.forEach(function(div) {
    // construct subtotal ID to be updated with sub extras (checkboxes) from corresponding div-id (div tag that contains checkboxes)
    var str = div.id.substring(7); // returns e.id"_"+(i+1)
    var position = str.search("_");
    var dish_id = str.substring(0, position);
    console.log("dish_id is: ", dish_id);
    var subtotal_id = "subtotal_" + dish_id;
    console.log("subtotal_id is ", subtotal_id);
    // now define checkboxes that are inside div
    var checkboxes = [].slice.call(div.children);
    console.log(checkboxes);
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', function () {
          console.log(document.getElementById(subtotal_id));
          console.log(parseFloat(document.getElementById(subtotal_id).innerText));
          var old_subtotal = parseFloat(document.getElementById(subtotal_id).innerText);

          if (this.checked) {
            // get the subtotal of the Sub-Dish(es)
            document.getElementById(subtotal_id).innerHTML = (old_subtotal+0.5).toFixed(2);
            calculate_total();
          }
          else {
            document.getElementById(subtotal_id).innerHTML = (old_subtotal-0.5).toFixed(2);
            calculate_total();
          }
        }
      );

    });
  });


  // on submit button
  document.querySelector('#basket').onsubmit = () => {

    // save localStorage preselection to native JS object
    var obj = JSON.parse(localStorage.getItem("preselection"));
    console.log("preselection is ", obj);

    // REGISTER SUB EXTRAS
    var sub_orders = JSON.parse(localStorage.getItem("sub_orders"));
    // get extras for each Sub
    if (sub_orders != null) {
      // forEach doesn't work for sub_orders because it iterates over indexes, not properties
      sub_orders.forEach((s) => {
        // div id of checkboxes corresponding to sub_order [dish_id_i] is: ("extras_"+e.id+"_"+(i+1))
        // construct string to get id for <div> with each Sub's checkboxes forextras
        var div_id = "#extras_"+s.sub_order; //sub_orders.sub_order: (input.id+"_"+(i+1))
        var div = document.querySelector(div_id);
        var checkboxes = [].slice.call(div.children); // gets the set of cehckboxes, should be an array

        for (var i=0; i < checkboxes.length; i++) {
          if (checkboxes[i].checked) {
            s.extras.push(checkboxes[i].value);
            console.log("Pushed: ", checkboxes[i].value);
          }
        }
        // push only works into anarray. s is an object itself so can't be 'pushed' into

      });
      console.log("Sub_orders to be passed as JSON to DJango via hidden form: ", sub_orders);
      //obj.push(sub_orders); // wait I think I need 3 pats... selection sub_orders and pizza_orders
      var jsonStr = JSON.stringify(sub_orders);
      localStorage.setItem("sub_orders", jsonStr);
    };


    // REGISTER PIZZA TOPPINGS
    var pizza_orders = JSON.parse(localStorage.getItem("pizza_orders")); // why are sub orders stored in here??
    if (pizza_orders != null) {
      for (var i=0; i<pizza_orders.length; i++) { // construct tr's id string
        // get toppings
        var td_id = "toppings_"+pizza_orders[i].pizza_order;
        var td = document.getElementById(td_id); // this is the <td> element containng set of topping dropdowns for 1 pizza (pizza_order)
        var toppings = [].slice.call(td.children);
        console.log("TOPPINGS ", toppings);
        toppings.forEach((topping) => { // for each select menu, i.e. each topping
          //var toppings = [];
          var sel = topping.options[topping.selectedIndex].value;
          pizza_orders[i].toppings.push(sel);
        });

      };
      //obj.push(pizza_orders);
      console.log("Pizza_orders to be passed as JSON to DJango via hidden form: ", pizza_orders);
      var jsonStr = JSON.stringify(pizza_orders);
      localStorage.setItem("pizza_orders", jsonStr);
    };

    var input_pizzas = document.querySelector("#pizza_orders");
    var input_subs = document.querySelector("#sub_orders");
    var input_preselection = document.querySelector("#preselection");
    input_pizzas.value = JSON.stringify(pizza_orders);
    input_subs.value = JSON.stringify(sub_orders);
    input_preselection.value = JSON.stringify(obj);
    localStorage.clear();
    document.getElementById("hiddenbasket").submit();

    // AJAX ATTEMPT - NOT FUNCTIONAL HERE, SOLVED WITH HIDDEN FORM SUBMISSION INSTEAD
    // const r = new XMLHttpRequest();
    // r.open('POST', '/basket');
    // const data = new FormData();
    // data.append('selection', jsonStr);
    // r.onload = () => {
    //   //location = "/basket"; // or window.location.href
    //   //localStorage.clear(); // ensure really cleared
    // };
    // r.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    // r.send(data);

    return false;
  };
})
