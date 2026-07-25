/* ==========================================================================
   orientation.js
   Dynamic 3D orientation visualization driven by Roll / Pitch / Yaw
   telemetry using Three.js. Renders a simplified CanSat body with axis
   indicators reacting live to attitude data.
   ========================================================================== */

const OrientationView = (() => {
  let scene, camera, renderer, cansatGroup;
  let targetRoll = 0, targetPitch = 0, targetYaw = 0;
  let curRoll = 0, curPitch = 0, curYaw = 0;

  function init() {
    const container = document.getElementById("orientation3d");
    const w = container.clientWidth, h = container.clientHeight;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.set(3.2, 2.2, 3.2);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    container.appendChild(renderer.domElement);

    // Lighting
    scene.add(new THREE.AmbientLight(0x8899aa, 0.8));
    const dir = new THREE.DirectionalLight(0x3ddcff, 1.2);
    dir.position.set(3, 5, 2);
    scene.add(dir);

    // Reference grid (artificial horizon floor)
    const grid = new THREE.GridHelper(6, 12, 0x223047, 0x1a2436);
    scene.add(grid);

    // CanSat body group
    cansatGroup = new THREE.Group();

    const bodyGeo = new THREE.CylinderGeometry(0.6, 0.6, 1.4, 24);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x161f30, metalness: 0.3, roughness: 0.5 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    cansatGroup.add(body);

    // Nose indicator (points +Z, marks "forward")
    const noseGeo = new THREE.ConeGeometry(0.18, 0.4, 16);
    const noseMat = new THREE.MeshStandardMaterial({ color: 0xff4d4d, emissive: 0x330000 });
    const nose = new THREE.Mesh(noseGeo, noseMat);
    nose.position.set(0, 0, 0.9);
    nose.rotation.x = Math.PI / 2;
    cansatGroup.add(nose);

    // Axis helper
    cansatGroup.add(new THREE.AxesHelper(1.2));

    scene.add(cansatGroup);
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    // Smooth interpolation toward target attitude for a "live" feel
    curRoll += (targetRoll - curRoll) * 0.12;
    curPitch += (targetPitch - curPitch) * 0.12;
    curYaw += (targetYaw - curYaw) * 0.12;

    cansatGroup.rotation.z = THREE.MathUtils.degToRad(curRoll);
    cansatGroup.rotation.x = THREE.MathUtils.degToRad(curPitch);
    cansatGroup.rotation.y = THREE.MathUtils.degToRad(curYaw);

    renderer.render(scene, camera);
  }

  function update(packet) {
    if (!packet) return;
    targetRoll = packet.roll;
    targetPitch = packet.pitch;
    targetYaw = packet.yaw;

    document.getElementById("o-roll").textContent = packet.roll.toFixed(1) + "°";
    document.getElementById("o-pitch").textContent = packet.pitch.toFixed(1) + "°";
    document.getElementById("o-yaw").textContent = packet.yaw.toFixed(1) + "°";
  }

  function reset() {
    targetRoll = targetPitch = targetYaw = 0;
    document.getElementById("o-roll").textContent = "0.0°";
    document.getElementById("o-pitch").textContent = "0.0°";
    document.getElementById("o-yaw").textContent = "0.0°";
  }

  function onResize() {
    const container = document.getElementById("orientation3d");
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }

  window.addEventListener("resize", () => { if (renderer) onResize(); });

  return { init, update, reset };
})();
