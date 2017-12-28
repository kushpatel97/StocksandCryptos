var ctx = document.getElementById("myChart").getContext('2d');
       var myChart = new Chart(ctx, {
           type: 'line',
           data: {
               labels:[{% for item in date %}
                           "{{item}}",
                       {% endfor %}],
               datasets: [{
                  label: 'Open',
                  data: {{openData}},
                  borderColor: "rgba(75,192,192,0.7)",
                  backgroundColor: "rgba(75,192,192,1)",
                  lineTension: 0,
                  fill: false
               }, {
                  label: 'Close',
                  data: {{closeData}},
                  borderColor: "rgba(255,99,132,0.7)",
                  backgroundColor: "rgba(255,99,132,1)",
                  lineTension: 0,
                  fill: false
               }
               ]
           },
           options: {}
       });