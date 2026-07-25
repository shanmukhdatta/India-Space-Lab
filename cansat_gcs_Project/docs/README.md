# CANSAT-GCS — Ground Control Software

**Student:** Boda Shanmukha Datta &nbsp;|&nbsp; **ISL Enrolment No.:** ISL-177115
**Institution:** NIT Jalandhar &nbsp;|&nbsp; **Email:** bodasd.ic.24@nitj.ac.in

Single-page CanSat Ground Control Software built for the India Space Lab
CanSat & CubeSat Satellite project assignment.

## 1. How to run it

1. Unzip this package anywhere on your computer.
2. Open `index.html` directly in **Google Chrome** or **Microsoft Edge**
   (required for the Web Serial API and camera access). Double‑click the
   file, or right‑click → Open With → Chrome.
3. No installation or build step is required — all libraries (Chart.js,
   Leaflet.js, Three.js) are bundled locally in `assets/vendor/`, so the
   dashboard also works fully offline. If you have an internet connection,
   the map tiles (OpenStreetMap) and the display fonts will additionally
   load online.

### Executable / application file note

This is a browser-based static web app — there is no compiled binary or
build step. `index.html` **is** the executable entry point: opening it in
Chrome/Edge launches the full application. If your submission portal
literally asks for "Executable/Application Files," point to `index.html`
(or submit the zipped project folder, e.g. `CanSat-GCS-v1.0.zip`) as that
deliverable.

## 2. Testing without hardware (Demo Sim mode)

Click **"Demo Sim: OFF"** in the top bar to turn it **ON**, then click
**"▶ Start Telemetry"**. This streams realistic simulated CanSat telemetry
(descending altitude, drifting GPS, rotating attitude, live faults) into
every panel — telemetry tables, error code display, graphs, map and 3D
orientation model — without any microcontroller connected. This is the
fastest way to demo or screenshot the full dashboard.

## 3. Testing with real hardware (WeGyanik Kit)

1. Flash `arduino/dummy_telemetry.ino` to the microcontroller in the
   WeGyanik Kit using the Arduino IDE (Baud rate: **9600**).
2. Connect the microcontroller to your PC over USB.
3. In the GCS, click **Connect Serial**, select the microcontroller's COM
   port in the browser prompt, then click **▶ Start Telemetry**.
4. Telemetry packets will stream in continuously and populate every panel.

## 4. UI Screenshots (Captured & Verified)

All 5 required high-resolution UI screenshots have been captured live from the running dashboard telemetry feed and saved in the `screenshots/` directory:

1. `01_full_dashboard.png` — Full Ground Control Station view showing all 6 telemetry and visualization panels.
2. `02_error_codes_fault.png` — Close-up of the Error Code module displaying live 7-segment fault indicators.
3. `03_tracking_map.png` — Leaflet.js GPS tracking map displaying live telemetry path trail.
4. `04_orientation_3d.png` — Three.js 3D attitude canvas rendering roll, pitch, and yaw mid-rotation.
5. `05_mission_control_log.png` — Mission Control panel displaying critical command execution log (`SENT → ACK ✓`).

## 5. Demonstration Video (Recorded & Saved)

A 1080p MP4 demonstration video walkthrough has been recorded and saved at:
- **Path:** `demonstration_video.mp4` (in the project root)
- **Format:** H.264 MP4 (1920x1080 @ 25 fps)
- **Walkthrough Actions:** Shows live telemetry streaming, command execution, CSV data export, graph image export, and packet reset workflow.

## 6. Package contents

```
index.html                      Main single-page application
css/style.css                   All styling (aerospace HUD theme)
js/telemetry.js                 Packet parsing + telemetry store
js/errorcodes.js                4-digit error code logic
js/charts.js                    Real-time Chart.js graphs
js/map.js                       Leaflet.js tracking map
js/orientation.js               Three.js 3D orientation model
js/video.js                     Live video streaming (MediaDevices API)
js/serial.js                    Web Serial link + demo telemetry simulator
js/datamanager.js               CSV/graph export, packet reset, logging
js/missioncontrol.js            Mission-critical command panel
js/app.js                       App bootstrap, clocks, top-bar wiring
assets/vendor/                  Locally bundled Chart.js, Leaflet.js, Three.js
arduino/dummy_telemetry.ino     WeGyanik Kit test sketch (Section 11)
samples/telemetry_log_sample.csv       Sample full telemetry log
samples/exported_telemetry_sample.csv  Sample CSV export
samples/graph_export_sample.png        Sample graph export
docs/CanSat_GCS_Project_Report.docx    Full project report (submit this)
docs/README.md                  This file
```

## 7. Telemetry packet format

One CSV line per packet, newline-terminated, 9600 baud:

```
TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,
DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,
ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE
```

Example: `ISL177115,0001,00:00:12,142.5,98.2,24.3,7.62,9.1,8,30.908200,75.851600,150.2,1.2,-0.8,44.5,0,0,0,0`
