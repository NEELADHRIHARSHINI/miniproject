async function checkUrl() {
  const url = document.getElementById("url").value;
  const res = await fetch("http://127.0.0.1:5000/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  const data = await res.json();

  const statusEl = document.getElementById("status");
  const riskEl = document.getElementById("risk");
  const adviceEl = document.getElementById("advice");

  statusEl.innerText = "Status: " + data.status;
  riskEl.innerText = "Risk: " + data.risk_percentage + "%";
  adviceEl.innerText = "Advice: " + data.advice;

  if (data.status === "SAFE") {
    statusEl.style.color = "green";
  } else if (data.status === "SUSPICIOUS") {
    statusEl.style.color = "orange";
  } else {
    statusEl.style.color = "red";
  }
}
