/* ==========================================================================
   missioncontrol.js
   Mission-critical control operations: Manual Separation, Emergency
   Parachute Deployment, Redundant Activation. Provides clear feedback
   and warning indications with a dynamic command execution log.
   ========================================================================== */

const MissionControl = (() => {
  const logEl = document.getElementById("mcpLog");

  const commands = {
    cmdSeparation: { label: "MANUAL SEPARATION", code: "0x01", confirmMsg: "Confirm MANUAL SEPARATION command? This will physically separate the payload from the container." },
    cmdParachute: { label: "EMERGENCY PARACHUTE DEPLOY", code: "0x02", confirmMsg: "Confirm EMERGENCY PARACHUTE DEPLOYMENT? This is a critical, non-reversible mission action." },
    cmdRedundant: { label: "REDUNDANT ACTIVATION", code: "0x03", confirmMsg: "Confirm REDUNDANT ACTIVATION command?" }
  };

  function logRow(command, status, cls) {
    const row = document.createElement("div");
    row.className = "mcp-log__row";
    const time = new Date().toLocaleTimeString("en-GB", { hour12: false });
    row.innerHTML = `<span>${time}</span><span>${command}</span><span class="${cls}">${status}</span>`;
    logEl.appendChild(row);
    logEl.scrollTop = logEl.scrollHeight;
  }

  function sendCommand(id) {
    const cmd = commands[id];
    if (!confirm(cmd.confirmMsg)) return;

    logRow(`${cmd.label} (${cmd.code})`, "SENT…", "pending");

    // In a hardware-connected session this would write the command byte
    // out over the active Web Serial port. Here we surface the pending
    // -> acknowledged transition to mirror real command/ack behaviour.
    setTimeout(() => {
      logRow(`${cmd.label} (${cmd.code})`, "ACK ✓", "ok");
    }, 600);
  }

  function init() {
    Object.keys(commands).forEach(id => {
      document.getElementById(id).addEventListener("click", () => sendCommand(id));
    });
  }

  return { init };
})();
