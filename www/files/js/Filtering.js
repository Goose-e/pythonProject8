function create_str(jsonData) {
  var table = document.querySelector("table");

  jsonData.Message.forEach(item => {
        var tr = document.createElement("tr");
        tr.setAttribute("class", "stoka_2");
        table.appendChild(tr);

        var button = document.createElement("button");
        button.setAttribute("type", "submit");
        button.setAttribute("class", "button-filter");
        button.setAttribute("name","button")

        button.innerHTML = "Del";

        const regul =/'/g;

        item = item.replace(regul,'\"');
        console.log(item);

        var json_file = JSON.parse(item)

        // Предполагаем, что у каждого объекта 'item' есть ключи 'SupportLevel', 'Timestamp', 'Endpoint' и 'Message'
        var tdNumer = document.createElement("td");
        tdNumer.innerText = json_file.Numer|| 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdNumer);

        var tdExpression_name = document.createElement("td");
        tdExpression_name.innerText = json_file.Expression_name || 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdExpression_name);

        var tdDate = document.createElement("td");
        tdDate.innerText = json_file.Date || 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdDate);

        var tdButton = document.createElement("td");
        tdButton.appendChild(button);
        tr.appendChild(tdButton);
    });
}

fetch('data_filter.json')
    .then(response => response.json()) // Преобразуем ответ в JSON
    .then(jsonData => {
    console.log(jsonData);
        create_str(jsonData);  // Вызов функции create_str с данными jsonData
    })
    .catch(error => console.error('Ошибка при получении данных:', error));