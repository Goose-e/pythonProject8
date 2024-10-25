function create_str(jsonData) {
    var table = document.querySelector("table");

    // Проходим по массиву 'Message'
    jsonData.Message.forEach(item => {
        var tr = document.createElement("tr");
        tr.setAttribute("class", "stoka_2");
        table.appendChild(tr);
        item.replace('E','o');
        const regul =/'/g;

        item = item.replace(regul,'\"');
        console.log(item);

        var json_file = JSON.parse(item)

        // Предполагаем, что у каждого объекта 'item' есть ключи 'SupportLevel', 'Timestamp', 'Endpoint' и 'Message'
        var tdSupportLevel = document.createElement("td");
        tdSupportLevel.innerText = json_file.SupportLevel|| 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdSupportLevel);

        var tdTimestamp = document.createElement("td");
        tdTimestamp.innerText = json_file.Timestamp || 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdTimestamp);

        var tdEndpoint = document.createElement("td");
        tdEndpoint.innerText = json_file.Endpoint || 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdEndpoint);

        var tdMessage = document.createElement("td");
        tdMessage.innerText = json_file.Message || 'N/A';  // Подкорректируйте в зависимости от структуры данных
        tr.appendChild(tdMessage);
    });
}

// Получение данных из файла 'datatest.json'
fetch('datatest.json')
    .then(response => response.json()) // Преобразуем ответ в JSON
    .then(jsonData => {
        create_str(jsonData);  // Вызов функции create_str с данными jsonData
    })
    .catch(error => console.error('Ошибка при получении данных:', error));

