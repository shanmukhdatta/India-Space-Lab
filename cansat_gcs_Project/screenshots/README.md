# CanSat GCS — Captured UI Screenshots & Demonstration Video

This folder contains all 5 required high-resolution UI screenshots captured live from the running **Ground Control Station (GCS)** telemetry feed, along with the demonstration video located in `cansat_gcs_Project/demonstration_video.mp4`.

---

## 📷 Included Screenshots

| File | Description | Status |
|------|-------------|--------|
| `01_full_dashboard.png` | Complete Ground Control Station single-page view showing all 6 telemetry and visualization panels in real-time operation. | ✅ Verified |
| `02_error_codes_fault.png` | Close-up of the Error Code module displaying live 7-segment digital fault indicators (D1: Descent, D2: GPS, D3: Separation, D4: Parachute). | ✅ Verified |
| `03_tracking_map.png` | Leaflet.js GPS tracking map displaying live telemetry latitude/longitude coordinates and path trail. | ✅ Verified |
| `04_orientation_3d.png` | Three.js 3D attitude canvas rendering the CanSat's roll, pitch, and yaw mid-rotation. | ✅ Verified |
| `05_mission_control_log.png` | Mission Control panel displaying critical command execution log (`MANUAL SEPARATION 0x01` showing `SENT → ACK ✓` transition). | ✅ Verified |

---

## 🎥 Demonstration Video

- **Path:** `../demonstration_video.mp4`
- **Format:** H.264 MP4 (1920x1080 @ 25 fps)
- **Contents:** Live 50-second walkthrough showing telemetry streaming, command execution, CSV export, graph export, and packet reset.
