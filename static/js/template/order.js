 Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';

    Chart.defaults.global.defaultFontColor = '#292b2c';

    var ctx = document.getElementById("myBarChart");
    var construction = '{{ data.CON }}'
    var real = '{{ data.REAL }}'
    var plan = '{{ data.PLAN }}'
    var other = '{{ data.OTHER }}'
    var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["Construction", "Real Estates", "Project Planning", "Other"],
        datasets: [{
          label: "Revenue",
          backgroundColor: "rgba(2,117,216,1)",
          borderColor: "rgba(2,117,216,1)",
          data: [construction, real, plan, other],
        }],
      },
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: ''
            },
            gridLines: {
              display: false
            },
            ticks: {
              maxTicksLimit: 6
            }
          }],
        },
        legend: {
          display: false
        }
      }
    });

    // Configure Pusher instance
    // var pusher = new Pusher('a0e97466cb155b48d6b7', {
    //     cluster: 'us2',
    // });

    // Subscribe to poll trigger
    // var orderChannel = pusher.subscribe('order');
    //
    // // Listen to 'order placed' event
    // var order = document.getElementById('order-count')
    // orderChannel.bind('place', function(data) {
    //   myLineChart.data.datasets.forEach((dataset) => {
    //       dataset.data.fill(parseInt(data.units),-1);
    //   });
    //   myLineChart.update();
    //   order.innerText = parseInt(order.innerText)+1
    // });