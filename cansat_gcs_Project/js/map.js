/* ==========================================================================
   map.js
   Live payload GPS tracking map using Leaflet.js + OpenStreetMap tiles.
   Renders current position marker and full mission trajectory/path history.
   ========================================================================== */

const TrackingMap = (() => {
  let map, marker, pathLine;
  const pathPoints = [];
  // Default center: NIT Jalandhar campus, used until first GPS fix arrives
  const DEFAULT_CENTER = [31.3970, 75.5354];

  function init() {
    map = L.map("map", { zoomControl: true, attributionControl: true })
      .setView(DEFAULT_CENTER, 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    const icon = L.divIcon({
      className: "cansat-marker",
      html: '<div style="width:14px;height:14px;border-radius:50%;background:#3ddcff;border:2px solid #fff;box-shadow:0 0 10px #3ddcff;"></div>',
      iconSize: [14, 14]
    });

    marker = L.marker(DEFAULT_CENTER, { icon }).addTo(map);
    pathLine = L.polyline([], { color: "#3ddcff", weight: 3, opacity: 0.8 }).addTo(map);
  }

  function update(packet) {
    if (!packet || !packet.gpsLat || !packet.gpsLon) return;
    const latlng = [packet.gpsLat, packet.gpsLon];
    marker.setLatLng(latlng);
    pathPoints.push(latlng);
    pathLine.setLatLngs(pathPoints);
    map.panTo(latlng, { animate: true });

    document.getElementById("map-lat").textContent = packet.gpsLat.toFixed(6);
    document.getElementById("map-lon").textContent = packet.gpsLon.toFixed(6);
    document.getElementById("map-pts").textContent = pathPoints.length;
  }

  function reset() {
    pathPoints.length = 0;
    pathLine.setLatLngs([]);
    marker.setLatLng(DEFAULT_CENTER);
    map.setView(DEFAULT_CENTER, 15);
    document.getElementById("map-lat").textContent = "0.000000";
    document.getElementById("map-lon").textContent = "0.000000";
    document.getElementById("map-pts").textContent = "0";
  }

  return { init, update, reset };
})();
