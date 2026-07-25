/* ==========================================================================
   telemetry.js
   Central telemetry state + packet parsing.

   Expected CSV packet format from the CanSat/microcontroller (WeGyanik Kit):
   TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,
   DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,
   ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE

   Example line:
   ISL177115,0001,00:00:12,142.5,98.2,24.3,7.62,9.1,8,30.908200,75.851600,150.2,1.2,-0.8,44.5,0,0,0,0
   ========================================================================== */

const Telemetry = (() => {
  let packetCount = 0;
  let listeners = [];
  const history = []; // full log of parsed packets, used for CSV export

  function onUpdate(fn) { listeners.push(fn); }

  function reset() {
    packetCount = 0;
    history.length = 0;
    listeners.forEach(fn => fn(null, { reset: true }));
  }

  /**
   * Parses a single raw line of telemetry (comma separated) into a
   * structured packet object. Returns null if the line is malformed.
   */
  function parseLine(raw) {
    const line = raw.trim();
    if (!line) return null;
    const parts = line.split(",").map(s => s.trim());
    if (parts.length < 19) return null;

    const [
      teamId, packetNo, missionTime, altitude, pressure, temp, voltage,
      descentRate, gpsSats, gpsLat, gpsLon, gpsAlt, roll, pitch, yaw,
      errDescent, errGps, errSep, errParachute
    ] = parts;

    const packet = {
      teamId,
      packetNo: parseInt(packetNo, 10) || 0,
      missionTime,
      altitude: parseFloat(altitude) || 0,
      pressure: parseFloat(pressure) || 0,
      temp: parseFloat(temp) || 0,
      voltage: parseFloat(voltage) || 0,
      descentRate: parseFloat(descentRate) || 0,
      gpsSats: parseInt(gpsSats, 10) || 0,
      gpsLat: parseFloat(gpsLat) || 0,
      gpsLon: parseFloat(gpsLon) || 0,
      gpsAlt: parseFloat(gpsAlt) || 0,
      roll: parseFloat(roll) || 0,
      pitch: parseFloat(pitch) || 0,
      yaw: parseFloat(yaw) || 0,
      errDescent: errDescent === "1" ? 1 : 0,
      errGps: errGps === "1" ? 1 : 0,
      errSep: errSep === "1" ? 1 : 0,
      errParachute: errParachute === "1" ? 1 : 0,
      receivedAt: new Date().toISOString()
    };
    return packet;
  }

  function ingest(raw) {
    const packet = parseLine(raw);
    if (!packet) return null;
    packetCount++;
    history.push(packet);
    listeners.forEach(fn => fn(packet, { reset: false }));
    return packet;
  }

  function getHistory() { return history; }
  function getCount() { return packetCount; }

  return { onUpdate, ingest, parseLine, reset, getHistory, getCount };
})();
