/* ==========================================================================
   datamanager.js
   Telemetry logging, CSV export, graph export trigger, and packet
   reset/storage functionality using the Blob API and File download links.
   ========================================================================== */

const DataManager = (() => {
  const CSV_HEADER = [
    "TEAM_ID", "PACKET_COUNT", "MISSION_TIME", "ALTITUDE_M", "PRESSURE_KPA",
    "TEMP_C", "VOLTAGE_V", "DESCENT_RATE_MS", "GPS_SATS", "GPS_LAT", "GPS_LON",
    "GPS_ALT_M", "ROLL_DEG", "PITCH_DEG", "YAW_DEG",
    "ERR_DESCENT", "ERR_GPS", "ERR_SEP", "ERR_PARACHUTE", "RECEIVED_AT"
  ].join(",");

  function onPacket(packet) {
    // Update every visualization module with the freshly parsed packet
    updateTelemetryDisplay(packet);
    ErrorCodeSystem.update(packet);
    Charts.update(packet);
    TrackingMap.update(packet);
    OrientationView.update(packet);

    document.getElementById("footerPacketCount").textContent =
      `Packets received: ${Telemetry.getCount()}`;
  }

  function updateTelemetryDisplay(p) {
    document.getElementById("t-packet").textContent = String(p.packetNo).padStart(4, "0");
    document.getElementById("t-mtime").textContent = p.missionTime;
    document.getElementById("t-alt").textContent = p.altitude.toFixed(1);
    document.getElementById("t-press").textContent = p.pressure.toFixed(1);
    document.getElementById("t-temp").textContent = p.temp.toFixed(1);
    document.getElementById("t-batt").textContent = p.voltage.toFixed(2);
    document.getElementById("t-desc").textContent = p.descentRate.toFixed(1);
    document.getElementById("t-sats").textContent = p.gpsSats;

    document.getElementById("p-roll").textContent = p.roll.toFixed(1);
    document.getElementById("p-pitch").textContent = p.pitch.toFixed(1);
    document.getElementById("p-yaw").textContent = p.yaw.toFixed(1);
    document.getElementById("p-lat").textContent = p.gpsLat.toFixed(6);
    document.getElementById("p-lon").textContent = p.gpsLon.toFixed(6);
    document.getElementById("p-galt").textContent = p.gpsAlt.toFixed(1);
  }

  function exportCsv() {
    const rows = Telemetry.getHistory().map(p => [
      p.teamId, p.packetNo, p.missionTime, p.altitude, p.pressure, p.temp,
      p.voltage, p.descentRate, p.gpsSats, p.gpsLat, p.gpsLon, p.gpsAlt,
      p.roll, p.pitch, p.yaw, p.errDescent, p.errGps, p.errSep, p.errParachute,
      p.receivedAt
    ].join(","));

    const csvContent = [CSV_HEADER, ...rows].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    downloadBlob(blob, `telemetry_log_${timestamp()}.csv`);
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function timestamp() {
    return new Date().toISOString().replace(/[:.]/g, "-");
  }

  function resetAll() {
    Telemetry.reset();
    Charts.reset();
    TrackingMap.reset();
    OrientationView.reset();
    ErrorCodeSystem.update(null);
    document.getElementById("footerPacketCount").textContent = "Packets received: 0";
    ["t-packet","t-mtime","t-alt","t-press","t-temp","t-batt","t-desc","t-sats",
     "p-roll","p-pitch","p-yaw","p-lat","p-lon","p-galt"].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.textContent = id.includes("lat") || id.includes("lon") ? "0.000000" : "0.0";
    });
    document.getElementById("t-packet").textContent = "0000";
  }

  return { onPacket, exportCsv, resetAll };
})();
