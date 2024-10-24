function create_str() {
  var table = document.querySelector("table");
  var tr = document.createElement("tr");
  tr.setAttribute("class", "stoka_2");
  table.appendChild(tr);

  var button = document.createElement("button");
  button.setAttribute("type", "button");
  button.setAttribute("class", "button-filter");
  button.innerHTML = "Del";

  var chekbox = document.createElement("input");
  chekbox.setAttribute("type", "checkbox");
  chekbox.setAttribute("class", "check-filter");

  for (var i = 0; i < 4; i++) {
    var td = document.createElement("td");
    switch (i) {
      case 0:
        td.innerText = getJsonField(i);
        break;
      case 1:
        td.innerText = getJsonField(i);
        break;
      case 2:
        td.innerText = getJsonField(i);
        break;
      case 3:
        td.appendChild(chekbox);
        td.appendChild(button);
        break;
    }
    tr.appendChild(td);
  }
}

for (var i = 0; i < 100; i++) create_str();

function getJsonField(el) {
  return el;
}
