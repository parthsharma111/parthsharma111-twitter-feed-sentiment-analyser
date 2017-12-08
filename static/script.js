var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [{
            label: "Analysis",
            backgroundColor:["rgba(213, 239, 194, 0.2)","rgba(255, 99, 132, 0.2)","rgba(255, 205, 86, 0.2)"],
            borderColor:["rgb(180, 205, 164)","rgb(255, 99, 132)","rgb(255, 205, 86)"],
            borderWidth:1,
            data: [positive_percent, negative_percent, 0.33333],
        }]
    },

    // Configuration options go here
    options: {
        scales: {
            xAxes: [{
                gridLines: {
                    display:false
                }
            }],
            yAxes: [{
                display: false,
                gridLines: {
                    display:false
                }
            }]
        }
    }
});


