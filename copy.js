document.querySelectorAll('button.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var t = document.getElementById(b.dataset.target).textContent;
    navigator.clipboard.writeText(t).then(function () {
      var old = b.textContent; b.textContent = 'Copied'; setTimeout(function () { b.textContent = old; }, 1500);
    });
  });
});
