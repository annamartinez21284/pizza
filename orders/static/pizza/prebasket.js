function load_basket () {
  if (localStorage.getItem("preselection") != null) {
    preselection = localStorage.getItem("preselection");
    // preselection is (or at least it should be) a string in JSON notation

    var json = JSON.parse(preselection);
    console.log("THIS IS PARSED BASKET: ", json);
    //document.querySelector('#test').innerHTML = preselection;
    json.forEach(function(e) {
      const tr = document.createElement('tr');
      const name = document.createElement('td');
      const size = document.createElement('td');
      const price = document.createElement('td');
      const amount = document.createElement('td');
      const subtotal = document.createElement('td');

      name.innerHTML = e.name;
      // display size if item has size
      if (e.size != null) {size.innerHTML = e.size;};
      price.innerHTML = e.price;
      price.setAttribute("class", "price");
      amount.innerHTML = e.amount.concat(" x");
      // display subtotal with 2 decimal places
      subtotal.innerHTML = (e.amount * e.price).toFixed(2);
      subtotal.setAttribute("class", "price");

      tr.appendChild(name);
      tr.appendChild(size);
      tr.appendChild(price);
      tr.appendChild(amount);
      tr.appendChild(subtotal);
      document.querySelector('#items').appendChild(tr);

      // if Pizza with n>0 topping(s), add row with n dropdown boxes - BUT THIS IS ONLY FOR ONE PIZZA, WHAT IF >!1??!! - another for loop around this!
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
            td.appendChild(select);
            tr.appendChild(td);

          }
        }
      };

      // if Sub, add 1 line per sub amount, and use AJAX to update price depending on # extra boxes ticked


    });
  }

  // if nothing is in basket
  else {
    window.location.href = '/';
  }

}



document.addEventListener('DOMContentLoaded', () => {
  load_basket();
})
