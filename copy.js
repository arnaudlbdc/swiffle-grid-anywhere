document.querySelectorAll('button.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var t = document.getElementById(b.dataset.target).textContent;
    navigator.clipboard.writeText(t).then(function () {
      var old = b.textContent; b.textContent = 'Copied'; setTimeout(function () { b.textContent = old; }, 1500);
    });
  });
});
// Show or hide the grid settings panel.
(function () {
  var t = document.getElementById('toggle');
  if (!t) return;
  t.addEventListener('click', function () {
    var open = document.body.classList.toggle('panel-open');
    t.textContent = open ? '\u2715 Hide settings' : '\u2699 Customize this grid';
  });
})();
