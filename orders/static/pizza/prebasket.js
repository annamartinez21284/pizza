function load_basket () {
  if (localStorage.getItem("preselection") != null) {
    preselection = localStorage.getItem("preselection");
    // preselection is (or at least it should be) a string in JSON notation

    var json = JSON.parse(preselection);
    console.log("THIS IS PARSED BASKET: ", json);
    //document.querySelector('#test').innerHTML = preselection;
    json.forEach(function(e) {
      const tr = document.createElement('tr');
      const td1 = document.createElement('td');
      const td2 = document.createElement('td');
      const td3 = document.createElement('td');

      td1.innerHTML = e.name;
      if (e.size != null) {td2.innerHTML = e.size;};
      td2.innerHTML = e.size;
      td3.innerHTML = e.price;
      // display size if item has size

      tr.appendChild(td1);
      tr.appendChild(td2);
      tr.appendChild(td3);
      document.querySelector('#items').appendChild(tr);
    });
    // do properly - looping thru preselection and building HTML elements 1 by 1
    // have a [hidden HTML element] on prebasket.html with all the Toppings - have Django render that from DB with template context
    // check toppingcount...
    // if pizza (= if toppingcount), add dropdown(s) for each topping in element created
    // check for cheese, 0top, 1top etc to determine # of topping dropdown lists
  }

  // if nothing is in basket
  else {
    window.location.href = '/';
  }

}



document.addEventListener('DOMContentLoaded', () => {
  load_basket();
})
