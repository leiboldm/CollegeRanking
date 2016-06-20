// WHAT: function to load a csv file and create an html table out of it
// PARAMS: csvurl is the address of a csv file with headers
//         table is an jquery table element the csv will be loaded into
// REQUIRES: jquery
function csv2table(csvurl, table, callback) {
    $.ajax({
        url: csvurl,
        beforeSend: function(xhr) {
            xhr.overrideMimeType("text/plain; charset=x-user-defined");
        }
    }).done(function(data, status) {
        console.log(status); 
        var lines = data.split("\n");
        var headerHtml = "<thead><tr>";
        var headers = lines[0].split(",");
        for (var i = 0; i < headers.length; i++) {
            headerHtml += ("<th>" + headers[i].split('"').join("") + "</th>");
        }
        headerHtml += "</tr></thead>\n";
        table.append(headerHtml);
        tableBody = table.append("<tbody></tbody>");
        for (var i = 1; i < lines.length; i++) {
            if (lines[i].length == 0) continue;
            cols = lines[i].split(",");
            tableHtml = "<tr>";
            for (var j = 0; j < cols.length; j++) {
                tableHtml += ("<td>" + cols[j].split('"').join("") + "</td>");
            }
            tableHtml += "</tr>";
            tableBody.append(tableHtml);
        }
        tableBody.append(tableHtml);
    }).fail(function (xhr, status, error) {
        console.log(status);
        table.html("Failed to load data");
    }).always(function() {
        callback();
    });
}
