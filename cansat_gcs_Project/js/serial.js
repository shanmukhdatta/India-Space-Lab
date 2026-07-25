/* ==========================================================================
   serial.js
   Handles the real hardware link (Web Serial API, used with the WeGyanik
   Kit microcontroller running arduino/dummy_telemetry.ino) AND ships a
   built-in software telemetry simulator so the full GCS can be demonstrated
   and screenshotted without physical hardware connected.
   ========================================================================== */

const SerialLink = (() => {
  let port = null;
  let reader = null;
  let keepReading = false;
  let lineBuffer = "";
  let simTimer = null;
  let simPacketNo = 0;
  let missionStartTime = null;

  const linkStatusEl = document.getElementById("linkStatus");
  const btnPort = document.getElementById("btnPort");
  const btnStart = document.getElementById("btnStart");
  const btnStop = document.getElementById("btnStop");
  const btnSim = document.getElementById("btnSimToggle");

  function setStatus(state, text) {
    linkStatusEl.dataset.state = state;
    linkStatusEl.querySelector(".status-text").textContent = text;
  }

  /* ---------------- Web Serial (real hardware) ---------------- */

  async function connectPort() {
    if (!("serial" in navigator)) {
      alert("Web Serial API is not supported in this browser. Use Chrome/Edge, or use Demo Sim mode instead.");
      return;
    }
    try {
      port = await navigator.serial.requestPort();
      await port.open({ baudRate: 9600 });
      setStatus("connected", "LINK: CONNECTED");
      btnStart.disabled = false;
      btnPort.textContent = "Disconnect";
    } catch (err) {
      console.error("Serial connection failed:", err);
    }
  }

  async function readLoop() {
    const textDecoder = new TextDecoderStream();
    const readableClosed = port.readable.pipeTo(textDecoder.writable);
    reader = textDecoder.readable.getReader();
    keepReading = true;

    try {
      while (keepReading) {
        const { value, done } = await reader.read();
        if (done) break;
        if (value) {
          lineBuffer += value;
          let idx;
          while ((idx = lineBuffer.indexOf("\n")) >= 0) {
            const line = lineBuffer.slice(0, idx);
            lineBuffer = lineBuffer.slice(idx + 1);
            handleIncomingLine(line);
          }
        }
      }
    } catch (err) {
      console.error("Serial read error:", err);
    } finally {
      reader.releaseLock();
    }
  }

  function handleIncomingLine(line) {
    const packet = Telemetry.ingest(line);
    if (packet) DataManager.onPacket(packet);
  }

  async function startTelemetry() {
    if (!missionStartTime) missionStartTime = Date.now();
    setStatus("live", "LINK: LIVE");
    btnStart.disabled = true;
    btnStop.disabled = false;
    if (port) readLoop();
  }

  async function stopTelemetry() {
    keepReading = false;
    if (reader) { try { await reader.cancel(); } catch (e) {} }
    stopSimulator();
    setStatus(port ? "connected" : "idle", port ? "LINK: CONNECTED" : "LINK: IDLE");
    btnStart.disabled = !port && !simActive;
    btnStop.disabled = true;
  }

  /* ---------------- Demo simulator (no hardware required) ---------------- */

  let simActive = false;
  let simPhase = 0;

  function genDummyPacket() {
    simPacketNo++;
    simPhase += 0.05;
    const elapsedSec = Math.floor((Date.now() - missionStartTime) / 1000);
    const h = String(Math.floor(elapsedSec / 3600)).padStart(2, "0");
    const m = String(Math.floor((elapsedSec % 3600) / 60)).padStart(2, "0");
    const s = String(elapsedSec % 60).padStart(2, "0");

    const altitude = Math.max(0, 400 - elapsedSec * 3.2 + Math.sin(simPhase) * 5);
    const descentRate = 8.5 + Math.sin(simPhase * 2) * 1.8;
    const pressure = 101.3 - altitude * 0.012;
    const temp = 24 + Math.sin(simPhase) * 3;
    const voltage = 7.6 - elapsedSec * 0.0008;
    const roll = Math.sin(simPhase * 1.3) * 18;
    const pitch = Math.cos(simPhase * 1.1) * 12;
    const yaw = (elapsedSec * 6) % 360;
    const gpsSats = 6 + Math.round(Math.sin(simPhase) * 2);

    // Base near NIT Jalandhar, drifting slightly to simulate descent drift
    const gpsLat = 31.3970 + Math.sin(simPhase * 0.3) * 0.002 + elapsedSec * 0.00002;
    const gpsLon = 75.5354 + Math.cos(simPhase * 0.3) * 0.002 + elapsedSec * 0.00001;

    const errDescent = (descentRate < 8 || descentRate > 10) ? 1 : 0;
    const errGps = gpsSats < 4 ? 1 : 0;
    const errSep = altitude < 50 ? 0 : 0;
    const errParachute = altitude < 100 && altitude > 5 ? 1 : 0;

    return [
      "ISL177115", String(simPacketNo).padStart(4, "0"), `${h}:${m}:${s}`,
      altitude.toFixed(1), pressure.toFixed(2), temp.toFixed(1), voltage.toFixed(2),
      descentRate.toFixed(1), gpsSats, gpsLat.toFixed(6), gpsLon.toFixed(6), altitude.toFixed(1),
      roll.toFixed(1), pitch.toFixed(1), yaw.toFixed(1),
      errDescent, errGps, errSep, errParachute
    ].join(",");
  }

  function startSimulator() {
    simActive = true;
    if (!missionStartTime) missionStartTime = Date.now();
    btnSim.textContent = "Demo Sim: ON";
    btnStart.disabled = false;
  }

  function stopSimulator() {
    simActive = false;
    if (simTimer) { clearInterval(simTimer); simTimer = null; }
    btnSim.textContent = "Demo Sim: OFF";
  }

  function toggleSimulator() {
    simActive ? stopSimulator() : startSimulator();
  }

  function startSimFeed() {
    if (!simActive) return;
    simTimer = setInterval(() => {
      const line = genDummyPacket();
      handleIncomingLine(line);
    }, 1000);
  }

  function stopSimFeed() {
    if (simTimer) { clearInterval(simTimer); simTimer = null; }
  }

  function init() {
    btnPort.addEventListener("click", connectPort);
    btnStart.addEventListener("click", () => {
      startTelemetry();
      if (simActive) startSimFeed();
    });
    btnStop.addEventListener("click", () => {
      stopTelemetry();
      stopSimFeed();
    });
    btnSim.addEventListener("click", toggleSimulator);
  }

  function getMissionStartTime() { return missionStartTime; }
  function syncTime() { missionStartTime = Date.now(); }
  function resetPacketCounter() { simPacketNo = 0; }

  return { init, getMissionStartTime, syncTime, resetPacketCounter };
})();
