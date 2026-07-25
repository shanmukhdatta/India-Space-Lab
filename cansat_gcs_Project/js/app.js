/* ==========================================================================
   app.js
   Application bootstrap: initializes all modules, drives the mission /
   UTC clocks, and wires the remaining top-bar controls (Sync PC Time,
   Reset Packet, Export CSV, Export Graph).
   ========================================================================== */

(function () {
  function pad(n) { return String(n).padStart(2, "0"); }

  function tickClocks() {
    const now = new Date();
    document.getElementById("utcClock").textContent =
      now.toISOString().substring(11, 19) + " UTC";

    const start = SerialLink.getMissionStartTime();
    if (start) {
      const elapsed = Math.max(0, Math.floor((Date.now() - start) / 1000));
      const h = pad(Math.floor(elapsed / 3600));
      const m = pad(Math.floor((elapsed % 3600) / 60));
      const s = pad(elapsed % 60);
      document.getElementById("missionClock").textContent = `T+${h}:${m}:${s}`;
    }
  }

  function wireTopBar() {
    document.getElementById("btnSyncTime").addEventListener("click", () => {
      SerialLink.syncTime();
      alert("PC time synced as mission T+00:00:00 reference.");
    });

    document.getElementById("btnResetPacket").addEventListener("click", () => {
      if (!confirm("Reset all telemetry, graphs, map path and packet counters?")) return;
      SerialLink.resetPacketCounter();
      DataManager.resetAll();
    });

    document.getElementById("btnExportCsv").addEventListener("click", DataManager.exportCsv);
    document.getElementById("btnExportGraph").addEventListener("click", Charts.exportAsImages);
  }

  function init() {
    Charts.init();
    TrackingMap.init();
    OrientationView.init();
    VideoStream.init();
    SerialLink.init();
    MissionControl.init();
    wireTopBar();

    Telemetry.onUpdate((packet, meta) => {
      if (meta.reset) return; // resetAll() handles UI clearing directly
    });

    setInterval(tickClocks, 1000);
    tickClocks();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
