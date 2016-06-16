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
        var tableHtml = "<thead><tr>";
        var headers = lines[0].split(",");
        for (var i = 0; i < headers.length; i++) {
            tableHtml += ("<th>" + headers[i].split('"').join("") + "</th>");
        }
        tableHtml += "</tr></thead>\n";
        tableHtml += "<tbody>";
        for (var i = 1; i < lines.length; i++) {
            if (lines[i].length == 0) continue;
            cols = lines[i].split(",");
            tableHtml += "<tr>";
            for (var j = 0; j < cols.length; j++) {
                tableHtml += ("<td>" + cols[j].split('"').join("") + "</td>");
            }
            tableHtml += "</tr>"
        }
        tableHtml += "</tbody>";
        table.html(tableHtml);
    }).fail(function (xhr, status, error) {
        console.log(status);
    }).always(function() {
        callback();
    });
}
