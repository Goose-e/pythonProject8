function create_str(jsonData) {
    var table = document.querySelector("table");
    // Iterate over the 'Message' array
    jsonData.Message.forEach(item => {
        var tr = document.createElement("tr");
        tr.setAttribute("class", "stoka_2");
        table.appendChild(tr);

        // Accessing properties from the item object
        var tdSupportLevel = document.createElement("td");
        tdSupportLevel.innerText = item.Message;  // Adjust based on actual structure
        tr.appendChild(tdSupportLevel);

        var tdTimestamp = document.createElement("td");
        tdTimestamp.innerText = item.Message;  // Adjust based on actual structure
        tr.appendChild(tdTimestamp);

        var tdEndpoint = document.createElement("td");
        tdEndpoint.innerText = item.Message;  // Adjust based on actual structure
        tr.appendChild(tdEndpoint);

        var tdMessage = document.createElement("td");
        tdMessage.innerText = item.Message;  // Adjust based on actual structure
        tr.appendChild(tdMessage);
    });
}

fetch('datatest.json')
    .then(response => response.json())
    .then(jsonData => {
        create_str(jsonData); // Call create_str with the full jsonData
    })
    .catch(error => console.error('Error fetching data:', error));
