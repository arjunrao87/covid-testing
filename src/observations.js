const _ = require("underscore")
export const observations = (results, metrics) => {
    const data = results['data'];
    console.log(data)
    const showDatasets = metrics.map(metric => {
        return {
            label: metric.name,
            data: data[metric.label],
            backgroundColor: _.range(data[metric.label].length).map(function () { return metric.color }),
            borderWidth: 3,
        }
    })
    console.log(showDatasets)
    return {
        type: 'line',
        data: {
            labels: data['row_date'],
            datasets: showDatasets,
        },
        options: {
            responsive: true,
            lineTension: 1,
            legend:{
                position: 'top',
            },
            scales: {
                yAxes: [{
                ticks: {
                    beginAtZero: true,
                    padding: 25,
                }
                }]
            }
        }
    }
}

export default observations;