/* ============================================================================
   dummy_telemetry.ino
   CANSAT-GCS — Hardware Testing Sketch (Section 11: Testing Strategy)

   Target: Microcontroller supplied in the WeGyanik Kit (Arduino-compatible)
   Purpose: Generates simulated CanSat telemetry packets and streams them
   continuously over USB serial to the Ground Control Software so that
   telemetry reception, graph updates, error-code logic, map tracking and
   orientation visualization can all be tested end-to-end without needing
   flight hardware or a real descent.

   Packet format (CSV, one packet per line, newline terminated):
   TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,
   DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,
   ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE

   Baud rate: 9600  (must match the rate used by the GCS Web Serial connect)
   ============================================================================ */

#define TEAM_ID   "ISL177115"
#define BAUD_RATE 9600
#define SEND_INTERVAL_MS 1000

unsigned long packetCount = 0;
unsigned long missionStartMillis = 0;

float altitude   = 400.0;   // starts high, simulates descent
float baseLat     = 31.397000;
float baseLon     = 75.535400;

void setup() {
  Serial.begin(BAUD_RATE);
  missionStartMillis = millis();
  randomSeed(analogRead(A0));
}

void loop() {
  sendDummyPacket();
  delay(SEND_INTERVAL_MS);
}

void sendDummyPacket() {
  packetCount++;

  unsigned long elapsedSec = (millis() - missionStartMillis) / 1000;
  int hh = (elapsedSec / 3600) % 24;
  int mm = (elapsedSec / 60) % 60;
  int ss = elapsedSec % 60;

  // ---- Simulated descent physics (very simplified) ----
  float descentRate = 8.5 + randFloat(-1.5, 1.5);
  altitude -= descentRate * (SEND_INTERVAL_MS / 1000.0);
  if (altitude < 0) altitude = 0;

  float pressure = 101.3 - altitude * 0.012;
  float temp     = 24.0 + randFloat(-2.0, 2.0);
  float voltage  = 7.6 - (elapsedSec * 0.0008);

  int gpsSats = 6 + random(-2, 3);
  float gpsLat = baseLat + randFloat(-0.0015, 0.0015);
  float gpsLon = baseLon + randFloat(-0.0015, 0.0015);
  float gpsAlt = altitude;

  float roll  = randFloat(-20, 20);
  float pitch = randFloat(-15, 15);
  float yaw   = fmod(elapsedSec * 6.0, 360.0);

  // ---- Fault flags (4-digit error code source data) ----
  int errDescent  = (descentRate < 8 || descentRate > 10) ? 1 : 0;
  int errGps      = (gpsSats < 4) ? 1 : 0;
  int errSep      = 0;                                   // toggled by ground command in real ops
  int errChute    = (altitude < 100 && altitude > 5) ? 1 : 0;

  // ---- Build and transmit CSV line ----
  Serial.print(TEAM_ID);              Serial.print(",");
  Serial.print(packetCount);          Serial.print(",");
  printTime(hh, mm, ss);              Serial.print(",");
  Serial.print(altitude, 1);          Serial.print(",");
  Serial.print(pressure, 2);          Serial.print(",");
  Serial.print(temp, 1);              Serial.print(",");
  Serial.print(voltage, 2);           Serial.print(",");
  Serial.print(descentRate, 1);       Serial.print(",");
  Serial.print(gpsSats);              Serial.print(",");
  Serial.print(gpsLat, 6);            Serial.print(",");
  Serial.print(gpsLon, 6);            Serial.print(",");
  Serial.print(gpsAlt, 1);            Serial.print(",");
  Serial.print(roll, 1);              Serial.print(",");
  Serial.print(pitch, 1);             Serial.print(",");
  Serial.print(yaw, 1);               Serial.print(",");
  Serial.print(errDescent);           Serial.print(",");
  Serial.print(errGps);               Serial.print(",");
  Serial.print(errSep);               Serial.print(",");
  Serial.println(errChute);
}

void printTime(int h, int m, int s) {
  if (h < 10) Serial.print("0"); Serial.print(h); Serial.print(":");
  if (m < 10) Serial.print("0"); Serial.print(m); Serial.print(":");
  if (s < 10) Serial.print("0"); Serial.print(s);
}

float randFloat(float minV, float maxV) {
  return minV + (float)random(0, 10000) / 10000.0 * (maxV - minV);
}
