document.addEventListener('DOMContentLoadad', () => {


  document.querySelector('logout').onclick = () => {
    localStorage.clear();
  }
});
