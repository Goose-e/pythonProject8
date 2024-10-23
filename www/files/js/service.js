function create_str() {
    var table = document.querySelector("table");
    var tr = document.createElement("tr");
    tr.setAttribute("class", "stoka_2");
    table.appendChild(tr);
    for (var i = 0; i < 5; i++) {
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
          td.innerText = getJsonField(i);
          break;
        case 4:
          td.innerText = getJsonField(i);
          break;
      }
      tr.appendChild(td);
    }
  }
  
  for (var i = 0; i < 100; i++) create_str();
  
  function getJsonField(el) {
    return el;
  }