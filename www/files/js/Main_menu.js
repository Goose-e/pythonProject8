for (var i = 0; i < 5; i++) {
  let myTr = document.createElement("td");
  myTr.setAttribute("class", "chetni");

  table = document.querySelector('table')
  table.appendChild(myTr);

  for (var i = 0; i < 5; i++) {
    let myTd = document.createElement("td");
    myTd.setAttribute("class", "piece");
    myTd.innerText='Тут будет текст';
    myTr.appendChild(myTd);
  }
}
