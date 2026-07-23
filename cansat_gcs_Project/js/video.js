/* ==========================================================================
   video.js
   Live video streaming support via browser MediaDevices getUserMedia API.
   Supports camera selection, start/stop controls and stream status display.
   ========================================================================== */

const VideoStream = (() => {
  const videoEl = document.getElementById("videoFeed");
  const statusEl = document.getElementById("videoStatus");
  const selectEl = document.getElementById("cameraSelect");
  const startBtn = document.getElementById("btnVideoStart");
  const stopBtn = document.getElementById("btnVideoStop");

  let currentStream = null;

  async function listCameras() {
    try {
      // Request a throwaway permission first so device labels are populated
      const temp = await navigator.mediaDevices.getUserMedia({ video: true });
      temp.getTracks().forEach(t => t.stop());
    } catch (e) {
      // Permission may be denied; camera list will still be attempted below
    }
    const devices = await navigator.mediaDevices.enumerateDevices();
    const cams = devices.filter(d => d.kind === "videoinput");
    selectEl.innerHTML = "";
    cams.forEach((cam, i) => {
      const opt = document.createElement("option");
      opt.value = cam.deviceId;
      opt.textContent = cam.label || `Camera ${i + 1}`;
      selectEl.appendChild(opt);
    });
    if (cams.length === 0) {
      const opt = document.createElement("option");
      opt.textContent = "No camera detected";
      selectEl.appendChild(opt);
    }
  }

  async function start() {
    try {
      const deviceId = selectEl.value;
      const constraints = { video: deviceId ? { deviceId: { exact: deviceId } } : true };
      currentStream = await navigator.mediaDevices.getUserMedia(constraints);
      videoEl.srcObject = currentStream;
      statusEl.textContent = "STREAM: LIVE";
      statusEl.classList.add("live");
      startBtn.disabled = true;
      stopBtn.disabled = false;
    } catch (err) {
      statusEl.textContent = "STREAM: ERROR";
      console.error("Video stream error:", err);
    }
  }

  function stop() {
    if (currentStream) {
      currentStream.getTracks().forEach(t => t.stop());
      currentStream = null;
    }
    videoEl.srcObject = null;
    statusEl.textContent = "STREAM: OFF";
    statusEl.classList.remove("live");
    startBtn.disabled = false;
    stopBtn.disabled = true;
  }

  function init() {
    listCameras();
    startBtn.addEventListener("click", start);
    stopBtn.addEventListener("click", stop);
    navigator.mediaDevices?.addEventListener?.("devicechange", listCameras);
  }

  return { init, start, stop };
})();
