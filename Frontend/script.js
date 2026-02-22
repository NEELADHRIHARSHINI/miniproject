async function checkURL() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert("Please enter a URL!");
        return;
    }

    try {
        // Send URL to backend
        const response = await fetch('http://127.0.0.1:5000/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();

        // Show results
        const statusEl = document.getElementById('statusText');
        const riskEl = document.getElementById('riskText');
        const adviceEl = document.getElementById('adviceText');

        statusEl.innerText = "Status: " + data.status;
        riskEl.innerText = "Risk: " + data.risk_percentage + "%";
        adviceEl.innerText = "Advice: " + (data.advice || "No advice available");

        // Color code status
        if (data.status === "PHISHING") {
            statusEl.style.color = "red";
        } else if (data.status === "SUSPICIOUS") {
            statusEl.style.color = "orange";
        } else {
            statusEl.style.color = "green";
        }

        // Draw chart with dynamic colors
        drawChart(data.risk_percentage, data.status);

    } catch (error) {
        alert("Error connecting to backend. Make sure Flask server is running.");
        console.error(error);
    }
}

function drawChart(risk, status) {
    const ctx = document.getElementById('riskChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.riskChartInstance) window.riskChartInstance.destroy();

    let riskColor = '#e74c3c';   // red
    let safeColor = '#2ecc71';   // green

    if (status === "SUSPICIOUS") {
        riskColor = '#f39c12';  // orange
    }

    window.riskChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Risk', 'Safe'],
            datasets: [{
                data: [risk, 100 - risk],
                backgroundColor: [riskColor, safeColor]
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
