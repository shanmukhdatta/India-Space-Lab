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

## 4. Taking the required UI screenshots

For your submission's **UI Screenshots** deliverable, run the app (Demo
Sim or real hardware) for at least 60 seconds so the graphs and map path
have visible history, then capture:

1. Full dashboard view (all six panels visible)
2. Close-up of the Error Code 7-segment module showing at least one fault
   digit lit (you can wait for the simulated parachute-altitude fault, or
   briefly disconnect the antenna/GPS on real hardware)
3. Tracking map with a visible path trail
4. Orientation model mid-rotation
5. Mission Control Panel after sending a command (showing the SENT → ACK log)

Use your OS screenshot tool (Windows: `Win+Shift+S`, Mac: `Cmd+Shift+4`)
and save the images into a `screenshots/` folder for your final submission.

## 5. Recording the demonstration video

Screen-record (OBS Studio, or Windows Xbox Game Bar `Win+G`) a 2–4 minute
walkthrough: connect/start telemetry → show each panel updating live →
send one mission control command → export CSV → export graphs → reset
packet. Save as `demonstration_video.mp4`.

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
