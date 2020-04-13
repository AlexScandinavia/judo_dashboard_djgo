const dataOptions = {chart: {type: 'area',
                             backgroundColor: {
                                linearGradient: { x1: 1, y1: 0, x2: 1, y2: 1 },
                                stops: [
                                    [0, '#2a2a2b'],
                                    [1, '#3e3e40']
                                ]
                            }},
                    colors: ['#0900ff', '#00008b ', '#003366'],
                    title: {text: '',
                            style : {color: '#E0E0E3',
                                    textTransform: 'uppercase'}
                            },
                    xAxis: {
                        labels: {style: {color: '#E0E0E3'}},
                        categories: [],
                        tickmarkPlacement: 'on',
                        minorGridLineColor: '#505053',
                        title: {style: {color: '#A0A0A3'}}
                        },
                    yAxis: {
                        gridLineColor: '#707073',
                        labels: {style: {color: '#E0E0E3'}},
                        title: {text: '',
                                style: {color: '#E0E0E3'}}
                        },

                    tooltip: {split: true},

                    plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#E0E0E3',
                            lineWidth: 3,
                            marker: {
                                lineWidth: 1,
                                lineColor: '#E0E0E3',
                                symbol: 'circle'}
                            }
                        },
                    credits: {enabled: false},
                    series: [],
                    legend: {
                        backgroundColor: 'rgba(0, 0, 0, 0.5)',
                        itemStyle:  {color: '#E0E0E3'},
                        itemHoverStyle: {color: '#FFF'},
                        itemHiddenStyle: {color: '#606063'},
                        title: {style: {color: '#C0C0C0'}}
                    },
                    };

// function to get the JSON data and update Chart
function RequestData_Update(url_input) {
$.ajax({
    url: url_input,
    type: 'get',
    dataType: 'json',
    success: function(data) {
        dataOptions.series = data.series
        dataOptions.xAxis.categories = data.xAxis.categories
        dataOptions.yAxis.title.text = data.yAxis.title.text
        dataOptions.yAxis.title.text = data.yAxis.title.text
        dataOptions.title.text = data.title.text

        Highcharts.chart('container', dataOptions)
     }

 })

}