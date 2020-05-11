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

      // if item is (a) pizza(s) - I check this via topping_count property
      // can naw also do if (e.dish_type == PIZZA) {}
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

      // if Sub, add 1 line per sub amount, and use AJAX to update price depending on # extra boxes ticked
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



document.addEventListener('DOMContentLoaded', () => {
  load_basket();
})
