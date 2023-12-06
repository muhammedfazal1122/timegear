(function ($) {
    "use strict";

    // Initialize the chart data with empty arrays
    let initialData = {
        labels: [],
        datasets: [
            {
                label: 'Sales',
                tension: 0.2,
                fill: true,
                backgroundColor: 'rgba(44,220,185,0.2)',
                borderColor: 'rgb(44,217,220)',
                data: []
            }
        ]
    };
    let ctx = document.getElementById('myChart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'line',
        data: initialData,
        options: {
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true,
                    },
                }
            },
            scales: {
                y: {
                    suggestedMin: 0,
                    suggestedMax: 10,
                    beginAtZero: true,
                }
            }
        }
    });

    function updateChart(newData) {
        chart.data.labels = Object.keys(newData);
        chart.data.datasets[0].data = Object.values(newData);
        chart.update();
    }

    function fetchData(url, successCallback) {
        $.ajax({
            type: 'GET',
            url: url,
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            } ,
            // crossDomain : true,
            success: successCallback,
            error: function (error) {
                console.log('Error:', error);
            }
        });
    }

    // Make an initial AJAX request to get the default data (monthly data)
    fetchData('fetchData/month/', function (monthlyData) {

        updateChart(monthlyData);
    });

    $('#dailyButton').on('click', function () {
        fetchData('fetchData/week/' , function (dailyData) {
            updateChart(dailyData);
        });
    });

    $('#MonthlyButton').on('click', function () {
        fetchData('fetchData/month/', function (monthlyData) {
            updateChart(monthlyData);
        });
    });

    $('#YearlyButton').on('click', function () {
        fetchData('fetchData/year/', function (yearlyData) {
            const monthOrder = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

            // Sort the month names based on the desired order
            const sortedLabels = Object.keys(yearlyData).sort((a, b) => monthOrder.indexOf(a) - monthOrder.indexOf(b));
            updateChart(yearlyData);
        });
    });
})(jQuery);