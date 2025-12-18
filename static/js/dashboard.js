document.addEventListener("DOMContentLoaded", function() {
    
    // Fetch data from our Flask API
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            renderTrendChart(data.trends);
            renderEmissionChart(data.emissions);
        });

    function renderTrendChart(trends) {
        const ctx = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: trends.years,
                datasets: [
                    {
                        label: 'Solar (GW)',
                        data: trends.solar,
                        borderColor: '#f1c40f',
                        fill: false
                    },
                    {
                        label: 'Wind (GW)',
                        data: trends.wind,
                        borderColor: '#3498db',
                        fill: false
                    },
                    {
                        label: 'Coal (GW)',
                        data: trends.coal,
                        borderColor: '#e74c3c',
                        borderDash: [5, 5], // Dashed line for declining fossil fuel
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                }
            }
        });
    }

    function renderEmissionChart(emissions) {
        const ctx = document.getElementById('emissionChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: emissions.labels,
                datasets: [{
                    label: 'CO2 Emissions (Million Tonnes)',
                    data: emissions.values,
                    backgroundColor: [
                        '#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
});