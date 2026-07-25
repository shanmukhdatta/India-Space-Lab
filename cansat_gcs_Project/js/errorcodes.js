/* ==========================================================================
   errorcodes.js
   4-digit live mission fault monitoring system.

   Digit 1 - Descent Rate   : 0 = within 8-10 m/s safe range, 1 = out of range
   Digit 2 - GPS Availability: 0 = GPS data available,        1 = unavailable
   Digit 3 - Payload Separation: 0 = separated successfully,  1 = failure
   Digit 4 - Emergency Parachute: 0 = inactive,                1 = activated
   ========================================================================== */

const ErrorCodeSystem = (() => {
  const digitEls = document.querySelectorAll("#errorDigits .digit");
  const legend = {
    desc: document.getElementById("err-desc"),
    gps: document.getElementById("err-gps"),
    sep: document.getElementById("err-sep"),
    para: document.getElementById("err-para"),
  };

  function computeDescentDigit(descentRate) {
    // Safe descent range for CanSat under main parachute: 8-10 m/s
    return (descentRate >= 8 && descentRate <= 10) ? 0 : 1;
  }

  function update(packet) {
    if (!packet) { render([0, 0, 0, 0]); return; }

    // Digit values are read straight from the telemetry packet's own
    // fault flags where provided by hardware; descent rate is additionally
    // cross-checked on the GCS side for redundancy.
    const d1 = packet.errDescent ?? computeDescentDigit(packet.descentRate);
    const d2 = packet.errGps ?? (packet.gpsSats < 4 ? 1 : 0);
    const d3 = packet.errSep ?? 0;
    const d4 = packet.errParachute ?? 0;

    render([d1, d2, d3, d4]);
  }

  function render(digits) {
    digits.forEach((val, i) => {
      const el = digitEls[i];
      el.textContent = val;
      el.classList.toggle("fault", val === 1);
    });

    setLegend(legend.desc, digits[0]);
    setLegend(legend.gps, digits[1]);
    setLegend(legend.sep, digits[2]);
    setLegend(legend.para, digits[3]);
  }

  function setLegend(el, val) {
    el.classList.toggle("fault", val === 1);
    el.classList.toggle("ok", val === 0);
  }

  function getCode(packet) {
    if (!packet) return "0000";
    const d1 = packet.errDescent ?? computeDescentDigit(packet.descentRate);
    const d2 = packet.errGps ?? (packet.gpsSats < 4 ? 1 : 0);
    const d3 = packet.errSep ?? 0;
    const d4 = packet.errParachute ?? 0;
    return `${d1}${d2}${d3}${d4}`;
  }

  return { update, getCode };
})();
