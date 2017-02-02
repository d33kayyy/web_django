// var barChartData = {
//     labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
//         "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"],
//     datasets: [{
//         fillColor: "#3B5897",
//         strokeColor: "none",
//         borderColor: "transparent",
//         data: [80000, 60000, 40000, 40000, 80000, 50000, 75000, 20000, 60000, 35000, 20000, 60000, 40000, 80000, 50000, 75000, 40000, 60000, 10000, 25500, 35000, 40000, 30000, 85000, 75000, 80000, 60000, 20000, 40000, 80000]
//     }]
// }
//
// var index = 11;
// var ctx = document.getElementById("canvas").getContext("2d");
// var barChartDemo = new Chart(ctx).Bar(barChartData, {
//     responsive: true,
//     barValueSpacing: 1,
// });
function displayLineChart() {
    var data = {
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        datasets: [
            {
                label: "My Second dataset",
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: [80000, 60000, 40000, 40000, 80000, 50000, 75000, 40000, 60000, 35000, 80000, 60000, 40000, 80000, 50000, 75000, 40000, 60000, 60000, 25500, 35000, 40000, 30000, 85000, 75000, 80000, 60000, 70000, 40000, 80000]
            }
        ]
    };
    var ctx = document.getElementById("lineChart").getContext("2d");
    var lineChart = new Chart(ctx).Line(data, {
        responsive: true,
    });
}

$(document).ready(function () {
    var ctx = $(".mycanvas").get(0).getContext("2d");

    var data = [
        {
            value: 95,
            color: "cornflowerblue",
            highlight: "lightskyblue",
            label: "Product1"
        },
        {
            value: 105,
            color: "#B5E57D",
            highlight: "#DFFFBB",
            label: "Product2"
        },
        {
            value: 70,
            color: "#D7858F",
            highlight: "#FF9BA8",
            label: "Product3"
        },
        {
            value: 50,
            color: "lightgreen",
            highlight: "yellowgreen",
            label: "Product4"
        },
        {
            value: 40,
            color: "orange",
            highlight: "darkorange",
            label: "Product5"
        }
    ];

    //draw
    var piechart = new Chart(ctx).Pie(data);
});

$(document).ready(function () {
    var ctx = $(".mycanvas2").get(0).getContext("2d");

    var data = [
        {
            value: 140,
            color: "cornflowerblue",
            highlight: "lightskyblue",
            label: "4 stars",

        },
        {
            value: 180,
            color: "#FFFF00",
            highlight: "#FFFF9A",
            label: "5 stars"
        },
        {
            value: 20,
            color: "#D7858F",
            highlight: "#FF9BA8",
            label: "3 stars"
        },
        {
            value: 18,
            color: "red",
            highlight: "#FF8F8F",
            label: "2 stars"
        },
        {
            value: 2,
            color: "black",
            highlight: "grey",
            label: "1 star"
        }
    ];

    //draw
    var piechart = new Chart(ctx).Pie(data);
});