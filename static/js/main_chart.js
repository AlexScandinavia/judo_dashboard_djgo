var dataOptions = {chart: {
                            type: 'area'
                          },
                      xAxis: {
                        categories: [],
                        tickmarkPlacement: 'on',
                        title: {enabled: true}
                        },
                      yAxis: {title: ''},
                      tooltip: {split: true, },

                      plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#666666',
                            lineWidth: 3,
                            marker: {
                                lineWidth: 1,
                                lineColor: '#666666'
                                }
                            }
                        },
                        credits: {enabled: false},
                        series: []

                    };

// function to get the JSON data and update Chart
function RequestData_Update(url_input) {
$.ajax({
    url: url_input,
    type: 'get',
    dataType: 'json',
    success: function(data) {
        dataOptions.series = data.series
        dataOptions.xAxis = data.xAxis
        dataOptions.yAxis = data.yAxis
        Highcharts.chart('container', dataOptions)
     }

 })

}