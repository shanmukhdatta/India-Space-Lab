# CanSat Ground Control Software (GCS) — Detailed Project Report

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 1. What Is This Project?

A **CanSat** (Can-Satellite) is a small satellite that fits inside a soda can. It is launched inside a rocket or balloon, performs a mission (collects data, descends with a parachute), and sends information back to Earth.

The **Ground Control Software (GCS)** is the computer program on the ground that:
- Receives live data (telemetry) from the CanSat
- Shows altitude, temperature, GPS position, battery level, etc.
- Displays graphs, maps, and a 3D model of the CanSat's orientation
- Monitors errors and faults during the mission
- Sends critical commands (like deploying a parachute)

Think of it like **mission control for NASA**, but built as a web dashboard for a student CanSat project.

---

## 2. Theoretical Background (Beginner Explanation)

### 2.1 What Is Telemetry?

**Telemetry** means "remote measurement." The CanSat measures things using sensors and sends numbers to the ground station as text packets over a serial (USB) connection.

Example data the CanSat sends:
- Altitude (how high it is)
- Pressure and temperature (from barometer)
- GPS latitude/longitude (where it is on Earth)
- Roll, pitch, yaw (how it is tilted/rotated)
- Battery voltage
- Error flags (is something wrong?)

### 2.2 Serial Communication

The CanSat microcontroller (like Arduino in the WeGyanik Kit) sends data through **USB serial** at **9600 baud** (9600 bits per second). Each line of data is one "packet" in CSV format (comma-separated values).

```
TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,...
```

The GCS reads these lines, splits them by commas, and updates the dashboard.

### 2.3 Web Serial API

Modern browsers (Chrome, Edge) support the **Web Serial API**, which lets a web page talk directly to a USB device without installing extra software. This is how the GCS connects to the WeGyanik Kit microcontroller.

### 2.4 Attitude (Roll, Pitch, Yaw)

- **Roll** — rotation around the front-to-back axis (like an airplane banking left/right)
- **Pitch** — rotation around the side-to-side axis (nose up or down)
- **Yaw** — rotation around the vertical axis (turning left/right like a compass)

These three angles describe the CanSat's **orientation** in 3D space.

### 2.5 Error Code System

The GCS uses a **4-digit error code** to quickly show mission health:

| Digit | Meaning | 0 = OK | 1 = Fault |
|-------|---------|--------|-----------|
| D1 | Descent Rate | 8–10 m/s (safe range) | Out of safe range |
| D2 | GPS Availability | GPS working (≥4 satellites) | GPS lost |
| D3 | Payload Separation | Separated successfully | Separation failed |
| D4 | Emergency Parachute | Not activated | Parachute deployed |

Example: `0100` means descent rate is out of range, but GPS, separation, and parachute are OK.

### 2.6 Mission Control Commands

Critical commands sent from GCS to CanSat:
- **Manual Separation (0x01)** — physically separate payload from container
- **Emergency Parachute Deploy (0x02)** — deploy backup parachute
- **Redundant Activation (0x03)** — activate backup systems

---

## 3. Tasks Given (Assignment Requirements)

Based on the India Space Lab CanSat & CubeSat assignment, the following deliverables were required:

| # | Task | Description |
|---|------|-------------|
| 1 | Build GCS Dashboard | Single-page web application with aerospace HUD-style UI |
| 2 | Telemetry Display | Show container and payload telemetry fields in real time |
| 3 | Error Code Module | 4-digit live fault monitoring with visual indicators |
| 4 | Real-Time Graphs | Plot altitude, pressure, temperature, descent rate, battery |
| 5 | GPS Tracking Map | Show live position and path trail on a map |
| 6 | 3D Orientation Model | Visualize roll, pitch, yaw using Three.js |
| 7 | Live Video Stream | Camera feed from payload using MediaDevices API |
| 8 | Serial Communication | Connect to WeGyanik Kit via Web Serial at 9600 baud |
| 9 | Mission Control Panel | Send critical commands with SENT → ACK logging |
| 10 | Data Export | Export telemetry to CSV and save graph images |
| 11 | Hardware Testing | Arduino sketch to generate dummy telemetry for testing |
| 12 | Demo Mode | Software simulator to test without hardware |
| 13 | Documentation | README, project report, UI screenshots, demo video |

---

## 4. How I Executed the Project (Step by Step)

### Step 1 — Project Structure Setup

I created a modular folder structure so each feature is in its own JavaScript file:

```
cansat_gcs_Project/
├── index.html              ← Main page (all panels)
├── css/style.css           ← Aerospace HUD dark theme
├── js/                     ← One file per feature
├── assets/vendor/          ← Chart.js, Leaflet, Three.js (offline)
├── arduino/                ← Hardware test sketch
├── samples/                ← Sample CSV exports
└── docs/                   ← Detailed README
```

### Step 2 — Built the Main Dashboard (`index.html`)

I designed a **6-panel grid layout**:

```
┌─────────────────────────────────────────────────────────┐
│  TOP BAR: Connect | Start | Stop | Export | Demo Sim   │
├──────────────┬──────────────────┬───────────────────────┤
│  Telemetry   │  Tracking Map    │  Real-Time Graphs     │
│  + Error     │  + Orientation   │  + Video              │
│  Codes       │  (3D Model)      │  + Mission Control    │
└──────────────┴──────────────────┴───────────────────────┘
```

### Step 3 — Telemetry Parsing (`js/telemetry.js`)

**What I did:**
- Created a central `Telemetry` module that parses incoming CSV lines
- Each line is split into 19 fields (team ID, altitude, GPS, errors, etc.)
- Parsed packets are stored in a history array for CSV export
- Other modules subscribe to updates via `onUpdate()` listener pattern

**Key code logic:**
```javascript
// Parse: "ISL177115,0001,00:00:12,142.5,98.2,..." into structured object
const parts = line.split(",");
const packet = {
  altitude: parseFloat(parts[3]),
  roll: parseFloat(parts[12]),
  // ... all 19 fields
};
```

### Step 4 — Error Code System (`js/errorcodes.js`)

**What I did:**
- Built a 7-segment-style 4-digit display
- Each digit turns red when fault = 1
- Cross-checks descent rate on GCS side (8–10 m/s safe range)
- Cross-checks GPS (needs ≥4 satellites)

### Step 5 — Real-Time Graphs (`js/charts.js`)

**What I did:**
- Used **Chart.js** to create 5 live updating charts
- Charts: Altitude, Pressure, Temperature, Descent Rate, Battery
- Each new telemetry packet appends a data point
- Rolling window keeps last ~120 points for performance

### Step 6 — GPS Tracking Map (`js/map.js`)

**What I did:**
- Used **Leaflet.js** with OpenStreetMap tiles
- Plots current GPS position as a marker
- Draws a polyline path trail showing where the CanSat has been
- Updates lat/lon readout in real time

### Step 7 — 3D Orientation Model (`js/orientation.js`)

**What I did:**
- Used **Three.js** to render a 3D box representing the CanSat
- Applies roll, pitch, yaw rotations from telemetry
- Auto-rotates slowly for visual effect when idle

### Step 8 — Serial Link + Demo Simulator (`js/serial.js`)

**What I did:**
- **Hardware mode:** Uses Web Serial API to connect at 9600 baud, reads lines, passes to Telemetry parser
- **Demo Sim mode:** Built-in software simulator that generates realistic fake telemetry (descending altitude, drifting GPS, rotating attitude, occasional faults) — no hardware needed

This was critical because it allows full dashboard testing and screenshot capture without the WeGyanik Kit connected.

### Step 9 — Data Manager (`js/datamanager.js`)

**What I did:**
- Central hub that receives each parsed packet and updates ALL panels
- **CSV Export:** Downloads full telemetry history as `.csv` file
- **Graph Export:** Saves chart as PNG image
- **Packet Reset:** Clears all data and resets counters

### Step 10 — Mission Control Panel (`js/missioncontrol.js`)

**What I did:**
- Three critical command buttons with confirmation dialogs
- Command log shows: TIME | COMMAND | STATUS (SENT → ACK)
- Simulates ACK response after 600ms (mirrors real hardware behavior)

### Step 11 — Arduino Test Sketch (`arduino/dummy_telemetry.ino`)

**What I did:**
- Wrote an Arduino sketch for the WeGyanik Kit microcontroller
- Generates realistic simulated CanSat descent data
- Sends CSV packets every 1 second at 9600 baud
- Includes simulated GPS drift, attitude rotation, and occasional error flags

### Step 12 — Styling (`css/style.css`)

**What I did:**
- Dark aerospace HUD theme (inspired by real mission control screens)
- Color-coded status chips (idle/connected/streaming)
- Monospace fonts for telemetry values
- Responsive grid layout for all panels

---

## 5. What I Built — Feature Summary

| Feature | File | Technology | Status |
|---------|------|------------|--------|
| Telemetry parsing | `js/telemetry.js` | Vanilla JS | ✅ Complete |
| Error codes | `js/errorcodes.js` | Vanilla JS | ✅ Complete |
| Live graphs | `js/charts.js` | Chart.js | ✅ Complete |
| GPS map | `js/map.js` | Leaflet.js | ✅ Complete |
| 3D orientation | `js/orientation.js` | Three.js | ✅ Complete |
| Video stream | `js/video.js` | MediaDevices API | ✅ Complete |
| Serial + demo sim | `js/serial.js` | Web Serial API | ✅ Complete |
| Data export | `js/datamanager.js` | Blob API | ✅ Complete |
| Mission control | `js/missioncontrol.js` | Vanilla JS | ✅ Complete |
| Hardware test | `arduino/dummy_telemetry.ino` | Arduino C++ | ✅ Complete |

---

## 6. Telemetry Packet Format

One CSV line per packet, sent at 9600 baud:

```
TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,
DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,
ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE
```

**Example packet:**
```
ISL177115,0001,00:00:12,142.5,98.2,24.3,7.62,9.1,8,30.908200,75.851600,150.2,1.2,-0.8,44.5,0,0,0,0
```

| Field | Example | Unit | Description |
|-------|---------|------|-------------|
| TEAM_ID | ISL177115 | — | Team identifier |
| PACKET_COUNT | 0001 | — | Sequential packet number |
| MISSION_TIME | 00:00:12 | HH:MM:SS | Elapsed mission time |
| ALTITUDE | 142.5 | meters | Current altitude |
| PRESSURE | 98.2 | kPa | Barometric pressure |
| TEMP | 24.3 | °C | Temperature |
| VOLTAGE | 7.62 | V | Battery voltage |
| DESCENT_RATE | 9.1 | m/s | Vertical descent speed |
| GPS_SATS | 8 | count | Number of GPS satellites |
| GPS_LAT | 30.908200 | degrees | Latitude |
| GPS_LON | 75.851600 | degrees | Longitude |
| GPS_ALT | 150.2 | meters | GPS altitude |
| ROLL | 1.2 | degrees | Roll angle |
| PITCH | -0.8 | degrees | Pitch angle |
| YAW | 44.5 | degrees | Yaw angle |
| ERR_DESCENT | 0 | 0/1 | Descent rate fault |
| ERR_GPS | 0 | 0/1 | GPS fault |
| ERR_SEP | 0 | 0/1 | Separation fault |
| ERR_PARACHUTE | 0 | 0/1 | Parachute fault |

---

## 7. How to Run and Test

### Option A — Demo Mode (No Hardware)

1. Open `cansat_gcs_Project/index.html` in **Chrome** or **Edge**
2. Click **"Demo Sim: OFF"** to turn it **ON**
3. Click **"▶ Start Telemetry"**
4. Watch all panels update with simulated data

### Option B — With WeGyanik Kit Hardware

1. Flash `arduino/dummy_telemetry.ino` to the microcontroller (Arduino IDE, 9600 baud)
2. Connect microcontroller to PC via USB
3. Open `index.html` in Chrome/Edge
4. Click **"Connect Serial"** → select COM port
5. Click **"▶ Start Telemetry"**

### Testing Checklist

- [ ] Telemetry values update every second
- [ ] Graphs show live scrolling data
- [ ] Map marker moves and path trail grows
- [ ] 3D model rotates with roll/pitch/yaw
- [ ] Error digits turn red when fault occurs
- [ ] CSV export downloads valid file
- [ ] Mission control command shows SENT → ACK in log

---

## 8. Key Design Decisions

1. **No build step** — Pure HTML/CSS/JS, open directly in browser
2. **Offline-capable** — All libraries bundled locally in `assets/vendor/`
3. **Modular architecture** — Each feature in separate JS file for maintainability
4. **Demo simulator** — Essential for testing without hardware
5. **Beginner-friendly UI** — Clear labels, color-coded status, aerospace theme

---

## 9. Conclusion

This CanSat GCS is a fully functional ground control station that meets all India Space Lab assignment requirements. It demonstrates understanding of:

- Serial communication and packet parsing
- Real-time data visualization (graphs, maps, 3D models)
- Error monitoring and fault detection
- Mission-critical command interfaces
- Web technologies (Web Serial API, Chart.js, Leaflet, Three.js)

The software works both with real hardware (WeGyanik Kit) and in standalone demo mode, making it easy to test, demonstrate, and submit.

---

*For quick setup instructions, see [`cansat_gcs_Project/docs/README.md`](cansat_gcs_Project/docs/README.md).*
