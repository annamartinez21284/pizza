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
      subtotal.setAttribute("id", ("subtotal_"+e.name)) // needs THE SIZE TOO!

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
          // in that row add 1 td containing 1 select menu each
          for (let j = 0; j < e.topping_count; j++) {
            const td = document.createElement('td');
            const toppings = document.querySelector('select');
            const select = toppings.cloneNode(true);
            select.removeAttribute("hidden");
            const st = document.createElement('option');
            st.setAttribute("selected", "true");
            st.setAttribute("disabled", "true");
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
          const tr = document.createElement('tr'); // make sure no scope issue here
          tr.setAttribute("class", "toppingline"); // MAKE CSS for toppingline stay inside big frame margin when shrunk!!
          document.querySelector('#items').appendChild(tr);
          const td1 = document.createElement('td');
          const td2 = document.createElement('td');
          td2.setAttribute("colspan", "5");
          td1.innerHTML = "Extra(s) ($0.50) for Sub #" + (i+1);
          const extras = document.querySelector('#extras');
          const checkboxes = extras.cloneNode(true);
          checkboxes.removeAttribute("hidden");
          checkboxes.setAttribute("id", ("extras_"+e.name+"_"+(i+1))) // why did I set this?
          checkboxes.setAttribute("name", "checkboxes")
          // set attribute id to something other than extras so can be identified with AJAX onselect or something
          td2.appendChild(checkboxes);
          tr.appendChild(td1);
          tr.appendChild(td2);
        }
      }


    });
  }

  // if nothing is in basket
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

  //var checkboxes = document.querySelectorAll("input[type=checkbox]");
  // select all divs (name=checkboxes) with checkbox menu
  var divs = document.getElementsByName("checkboxes");
  divs.forEach(function(div) {
    // move up to parent element (a div with unique id) and again to parent td2 and again to parent tr, then to previousneighbor tr into price
    var str = div.id.substring(7); // returns "extras_"+e.name+"_"+(i+1)
    var position = str.search("_");
    var dish_name = str.substring(0, position);
    console.log("dish_name is: ", dish_name);
    var subtotal_id = "subtotal_" + dish_name;
    console.log("subtotal_id is ", subtotal_id); // NEEDS THE SIZE TOO, but is correct!
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
          else { // make sure only if UNticked, i.e. price never below original
            document.getElementById(subtotal_id).innerHTML = (old_subtotal-0.5).toFixed(2);
            calculate_total();
          }
        }
      );

    });
  });
})
