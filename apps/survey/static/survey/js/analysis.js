

function pizza(id, d, t) {

    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(drawChart);
    
    function drawChart() {
        
        var data = google.visualization.arrayToDataTable(d);

        var options = {
          title: t,
          'width':500,
          'height':300
        };

        var chart = new google.visualization.PieChart(document.getElementById(id));
        chart.draw(data, options);
    }
}
