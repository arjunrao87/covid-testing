const _ = require("underscore")
export const observations = (results) => {
    const data = results['data'];
    return {
        type: 'line',
        data: {
            labels: data['row_date'],
            datasets: [
                {
                    label: 'cumulative_total',
                    data: data['cumulative_total'],
                    backgroundColor: _.range(data['cumulative_total'].length).map(function () { return 'rgba(165, 107, 223,0.4)' }),
                    borderWidth: 3,
                },
                {
                    label: 'daily_change_cumulative_total',
                    data: data['daily_change_cumulative_total'],
                    backgroundColor: _.range(data['daily_change_cumulative_total'].length).map(function () { return 'rgba(223, 107, 107,0.4)' }),
                    borderWidth: 3, 
                },
                {
                    label: 'cumulative_total_per_thousand',
                    data: data['cumulative_total_per_thousand'],
                    backgroundColor: _.range(data['cumulative_total_per_thousand'].length).map(function () { return 'rgba(17, 96, 186, 0.2)' }),
                    borderWidth: 3, 
                },
                {
                    label: 'daily_change_in_cumulative_total_per_thousand',
                    data: data['daily_change_in_cumulative_total_per_thousand'],
                    backgroundColor: _.range(data['daily_change_in_cumulative_total_per_thousand'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                    borderWidth: 3, 
                },
                {
                    label: 'seven_day_smoothed_daily_change',
                    data: data['seven_day_smoothed_daily_change'],
                    backgroundColor: _.range(data['seven_day_smoothed_daily_change'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                    borderWidth: 3, 
                },
                {
                    label: 'seven_day_smoothed_daily_change_per_thousand',
                    data: data['seven_day_smoothed_daily_change_per_thousand'],
                    backgroundColor: _.range(data['seven_day_smoothed_daily_change_per_thousand'].length).map(function () { return 'rgba(255,153,0,0.4)' }),
                    borderWidth: 3, 
                },
            ]
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