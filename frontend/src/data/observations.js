const _ = require("underscore")

export const observations = (results) => {
    //const borderColor = [].fill("#A99DE3", 0, results['data']['cumulative_total'].length-1)
    const backgroundColor1 = _.range(results['data']['cumulative_total'].length).map(function () { return 'rgba(255,153,0,0.4)' })
    return {
        type: 'line',
        data: {
        labels: results['data']['row_date'],
        datasets: [
            { // one line graph
            label: 'cumulative_total',
            data: results['data']['cumulative_total'],
            backgroundColor: _.range(results['data']['cumulative_total'].length).map(function () { return 'rgba(165, 107, 223,0.4)' }),
            borderWidth: 3,
            // fill: false  
            },
            { // one line graph
                label: 'daily_change_cumulative_total',
                data: results['data']['daily_change_cumulative_total'],
                backgroundColor: _.range(results['data']['daily_change_cumulative_total'].length).map(function () { return 'rgba(223, 107, 107,0.4)' }),
                borderWidth: 3,
                // fill: false  
            },
            { // one line graph
                label: 'cumulative_total_per_thousand',
                data: results['data']['cumulative_total_per_thousand'],
                backgroundColor: _.range(results['data']['cumulative_total_per_thousand'].length).map(function () { return 'rgba(17, 96, 186, 0.2)' }),
                borderWidth: 3,
                // fill: false  
            },
            { // one line graph
                label: 'daily_change_in_cumulative_total_per_thousand',
                data: results['data']['daily_change_in_cumulative_total_per_thousand'],
                backgroundColor: _.range(results['data']['daily_change_in_cumulative_total_per_thousand'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                borderWidth: 3,
                // fill: false  
            },
            { // one line graph
                label: 'seven_day_smoothed_daily_change',
                data: results['data']['seven_day_smoothed_daily_change'],
                backgroundColor: _.range(results['data']['seven_day_smoothed_daily_change'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                borderWidth: 3,
                // fill: false  
            },
            { // one line graph
                label: 'seven_day_smoothed_daily_change_per_thousand',
                data: results['data']['seven_day_smoothed_daily_change_per_thousand'],
                backgroundColor: _.range(results['data']['seven_day_smoothed_daily_change_per_thousand'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                borderWidth: 3,
                // fill: false  
            },
        ]
        },
        options: {
        responsive: true,
        lineTension: 1,
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