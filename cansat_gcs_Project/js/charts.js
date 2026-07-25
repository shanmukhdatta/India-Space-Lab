/* ==========================================================================
   charts.js
   Real-time updating graphs for altitude, pressure, temperature,
   descent rate and battery voltage using Chart.js.
   ========================================================================== */

const Charts = (() => {
  const MAX_POINTS = 60;
  const commonOptions = (label, color) => ({
    type: "line",
    data: { labels: [], datasets: [{
      label, data: [],
      borderColor: color, backgroundColor: color + "22",
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true
    }]},
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: {
        legend: { display: true, labels: { color: "#8fa0bd", font: { size: 10 } } },
        title: { display: false }
      },
      scales: {
        x: { ticks: { color: "#5b6b87", maxTicksLimit: 6, font: { size: 9 } }, grid: { color: "#1a2436" } },
        y: { ticks: { color: "#5b6b87", font: { size: 9 } }, grid: { color: "#1a2436" } }
      }
    }
  });

  let charts = {};

  function init() {
    charts.alt = new Chart(document.getElementById("chartAlt"), commonOptions("Altitude (m)", "#3ddcff"));
    charts.press = new Chart(document.getElementById("chartPress"), commonOptions("Pressure (kPa)", "#9b8bff"));
    charts.temp = new Chart(document.getElementById("chartTemp"), commonOptions("Temperature (°C)", "#ffb020"));
    charts.desc = new Chart(document.getElementById("chartDesc"), commonOptions("Descent Rate (m/s)", "#ff4d4d"));
    charts.batt = new Chart(document.getElementById("chartBatt"), commonOptions("Battery Voltage (V)", "#34e0a1"));
  }

  function pushPoint(chart, label, value) {
    const d = chart.data;
    d.labels.push(label);
    d.datasets[0].data.push(value);
    if (d.labels.length > MAX_POINTS) {
      d.labels.shift();
      d.datasets[0].data.shift();
    }
    chart.update("none");
  }

  function update(packet) {
    if (!packet) return;
    const t = packet.missionTime || packet.packetNo;
    pushPoint(charts.alt, t, packet.altitude);
    pushPoint(charts.press, t, packet.pressure);
    pushPoint(charts.temp, t, packet.temp);
    pushPoint(charts.desc, t, packet.descentRate);
    pushPoint(charts.batt, t, packet.voltage);
  }

  function reset() {
    Object.values(charts).forEach(c => {
      c.data.labels = [];
      c.data.datasets[0].data = [];
      c.update("none");
    });
  }

  function exportAsImages() {
    const zipParts = [];
    Object.entries(charts).forEach(([key, chart]) => {
      const url = chart.toBase64Image();
      const a = document.createElement("a");
      a.href = url;
      a.download = `graph_${key}_${Date.now()}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  }

  return { init, update, reset, exportAsImages };
})();
