let vendasChart; 

function loadChartData(start_date = '', end_date = '') {
  const baseUrl = "{{ url_for('dados_vendas') }}";    
  let url = baseUrl;

  if (start_date && end_date) {
    const params = new URLSearchParams({ start_date: start_date, end_date: end_date });
    url = `${baseUrl}?${params.toString()}`;
  }
  console.log("URL requisitada:", url);  // Debug para conferir o URL

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById('vendasChart').getContext('2d');
      if(vendasChart) {
        vendasChart.destroy();
      }
      vendasChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels, // espera-se formato YYYY-MM-DD vindo do backend
          datasets: [{
            label: 'Total de Vendas',
            data: data.sales, // valores numéricos
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: true
          }]
        },
        options: {
          responsive: true,
          scales: {
            xAxes: [{
              type: 'time',
              time: {
                unit: 'day',
                tooltipFormat: 'DD/MM/YYYY',
                displayFormats: {
                  day: 'DD/MM/YYYY'
                }
              },
              ticks: {
                autoSkip: true,
                maxTicksLimit: 10
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
      });
    })
    .catch(error => console.error('Erro ao carregar os dados das vendas:', error));
}

loadChartData();

document.getElementById("btnFiltrar").addEventListener("click", function(){
  const dataInicio = document.getElementById("dataInicio").value;
  const dataFim = document.getElementById("dataFim").value;
  // Verifica se as datas foram informadas
  if(!dataInicio || !dataFim){
    alert('Por favor, informe a data inicial e final para filtrar.');
    return;
  }
  loadChartData(dataInicio, dataFim);
});