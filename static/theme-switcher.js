document.getElementById("theme-switcher").addEventListener("click", function() {
  var body = document.body;
  var theme = body.getAttribute("data-theme");
  if (theme && theme === "dark") {
    body.setAttribute("data-theme", "light");
  } else {
    body.setAttribute("data-theme", "dark");
  }
});
