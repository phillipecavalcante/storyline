

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


function line(id, d, t){

    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(drawChart);
    
    function drawChart() {
    
        var data = google.visualization.arrayToDataTable(d);

        var options = {
            title: t,
            'width':500,
            'height':300
        };

        var chart = new google.visualization.LineChart(document.getElementById(id));
        chart.draw(data, options);
    }
}

function candlestick(id, d, t){

    function drawVisualization() {
        var data = google.visualization.arrayToDataTable(d, true);

        var options = {
          title : t,
          legend:'none'
        };

        var chart = new google.visualization.CandlestickChart(document.getElementById(id));
        chart.draw(data, options);
      }

      google.setOnLoadCallback(drawVisualization);
}

function barchart(id, d, t){
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(drawChart);
  function drawChart() {
    var data = google.visualization.arrayToDataTable(d);

    var options = {
      title: t,
      //vAxis: {title: 'Story',  titleTextStyle: {color: 'black'}}
    };

    var chart = new google.visualization.BarChart(document.getElementById(id));
    chart.draw(data, options);
  }
}