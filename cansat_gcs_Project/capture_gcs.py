import os
import time
import shutil
import subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

SCREENSHOT_DIR = r"c:\Users\shanm\ISL\India-Space-Lab-main\cansat_gcs_Project\screenshots"
VIDEO_TARGET = r"c:\Users\shanm\ISL\India-Space-Lab-main\cansat_gcs_Project\demonstration_video.mp4"
TEMP_VIDEO_DIR = r"c:\Users\shanm\ISL\India-Space-Lab-main\cansat_gcs_Project\screenshots\temp_video"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(TEMP_VIDEO_DIR, exist_ok=True)

with sync_playwright() as p:
    print("Launching Chromium browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=TEMP_VIDEO_DIR,
        record_video_size={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    # Handle dialog auto-accept (e.g. for Reset Packet confirm)
    page.on("dialog", lambda dialog: dialog.accept())

    print("Navigating to local CanSat GCS server...")
    page.goto("http://localhost:8080/index.html")
    page.wait_for_load_state("networkidle")

    # 1. Turn Demo Sim ON
    print("Toggling Demo Sim ON...")
    page.click("#btnSimToggle")
    time.sleep(1)

    # 2. Click Start Telemetry
    print("Starting Telemetry...")
    page.click("#btnStart")
    time.sleep(2)

    # Let telemetry run for ~25 seconds to populate map path, charts, 3D model orientation
    print("Running telemetry feed for live visuals...")
    time.sleep(25)

    # 3. Send Mission Control Command (Manual Separation CMD 0x01)
    print("Sending Mission Control Command 0x01...")
    page.click("#cmdSeparation")
    time.sleep(2)  # Wait for ACK log

    # Take Screenshot 05: Mission Control Log
    print("Capturing 05_mission_control_log.png...")
    mcp_panel = page.query_selector(".panel--mcp")
    if mcp_panel:
        mcp_panel.screenshot(path=os.path.join(SCREENSHOT_DIR, "05_mission_control_log.png"))

    # Take Screenshot 02: Error codes module
    print("Capturing 02_error_codes_fault.png...")
    err_module = page.query_selector(".error-module")
    if err_module:
        err_module.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_error_codes_fault.png"))

    # Take Screenshot 03: Tracking Map
    print("Capturing 03_tracking_map.png...")
    map_panel = page.query_selector(".panel--map")
    if map_panel:
        map_panel.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_tracking_map.png"))

    # Take Screenshot 04: Orientation 3D
    print("Capturing 04_orientation_3d.png...")
    orient_panel = page.query_selector(".panel--orientation")
    if orient_panel:
        orient_panel.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_orientation_3d.png"))

    # Let telemetry run another 10s for full dashboard view
    time.sleep(10)

    # Take Screenshot 01: Full Dashboard
    print("Capturing 01_full_dashboard.png...")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_full_dashboard.png"), full_page=True)

    # Additional Demo Video Script steps:
    # - Click Export CSV
    print("Clicking Export CSV...")
    page.click("#btnExportCsv")
    time.sleep(2)

    # - Click Export Graph
    print("Clicking Export Graph...")
    page.click("#btnExportGraph")
    time.sleep(2)

    # - Click Reset Packet
    print("Clicking Reset Packet...")
    page.click("#btnResetPacket")
    time.sleep(3)

    print("Closing browser context...")
    context.close()
    browser.close()

# Convert video to demonstration_video.mp4
print("Converting recorded video to demonstration_video.mp4...")
files = [os.path.join(TEMP_VIDEO_DIR, f) for f in os.listdir(TEMP_VIDEO_DIR) if f.endswith(".webm")]
if files:
    webm_file = files[0]
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-y", "-i", webm_file, "-c:v", "libx264", "-pix_fmt", "yuv420p", VIDEO_TARGET]
    subprocess.run(cmd, check=True)
    print(f"Successfully generated {VIDEO_TARGET}!")

# Clean up temp video folder
if os.path.exists(TEMP_VIDEO_DIR):
    shutil.rmtree(TEMP_VIDEO_DIR, ignore_errors=True)
print("Automation complete!")
