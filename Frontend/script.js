async function checkURL() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert("Please enter a URL!");
        return;
    }

    // Send URL to backend
    const response = await fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    // Show results
    document.getElementById('statusText').innerText = "Status: " + data.status;
    document.getElementById('riskText').innerText = "Risk: " + data.risk_percentage + "%";

    // Draw chart
    drawChart(data.risk_percentage);
}

function drawChart(risk) {
    const ctx = document.getElementById('riskChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.riskChartInstance) window.riskChartInstance.destroy();

    window.riskChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Risk', 'Safe'],
            datasets: [{
                data: [risk, 100 - risk],
                backgroundColor: ['#e74c3c', '#2ecc71']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}
