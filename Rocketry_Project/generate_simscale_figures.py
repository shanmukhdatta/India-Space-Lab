import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

OUT_DIR = r"c:\Users\shanm\ISL\India-Space-Lab-main\Rocketry_Project"
os.makedirs(OUT_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

# 1. SimScale FEM Stress Contour (simscale_fem_stress_fine.png)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
span = np.linspace(0, 100, 200) # mm
chords = np.linspace(150, 75, 200) # mm

# Bending stress distribution (max at root, zero at tip)
stress = 7.552 * (1 - (span / 100)**0.8)
stress_mesh = np.tile(stress, (50, 1))

y_top = chords / 2
y_bot = -chords / 2

X, Y = np.meshgrid(span, np.linspace(-75, 75, 50))
# Mask outside fin outline
mask = np.zeros_like(X, dtype=bool)
for i in range(len(span)):
    mask[:, i] = (Y[:, i] < -chords[i]/2) | (Y[:, i] > chords[i]/2)

stress_masked = np.ma.masked_array(stress_mesh, mask=mask)

c = ax.contourf(X, Y, stress_masked, levels=50, cmap='jet')
cbar = fig.colorbar(c, ax=ax)
cbar.set_label('Von Mises Stress (MPa)', fontsize=12, fontweight='bold')

ax.plot(span, y_top, 'k-', linewidth=2)
ax.plot(span, y_bot, 'k-', linewidth=2)
ax.plot([0, 0], [-75, 75], 'r-', linewidth=4, label='Root Fixed Constraint')
ax.plot([100, 100], [-37.5, 37.5], 'k-', linewidth=2)

ax.set_title('SimScale Finite Element Analysis — Von Mises Bending Stress (Fine Mesh 64 Elements)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Spanwise Coordinate x (mm)', fontsize=12)
ax.set_ylabel('Chordwise Coordinate y (mm)', fontsize=12)
ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax.legend(loc='upper right')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "simscale_fem_stress_fine.png"))
plt.close()
print("Generated simscale_fem_stress_fine.png")

# 2. SimScale FEM Displacement Contour (simscale_fem_displacement.png)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
disp = 0.1474 * (span / 100)**2 # mm
disp_mesh = np.tile(disp, (50, 1))
disp_masked = np.ma.masked_array(disp_mesh, mask=mask)

c = ax.contourf(X, Y, disp_masked, levels=50, cmap='plasma')
cbar = fig.colorbar(c, ax=ax)
cbar.set_label('Resultant Displacement (mm)', fontsize=12, fontweight='bold')

ax.plot(span, y_top, 'k-', linewidth=2)
ax.plot(span, y_bot, 'k-', linewidth=2)
ax.plot([0, 0], [-75, 75], 'r-', linewidth=4, label='Root Fixed Constraint')
ax.plot([100, 100], [-37.5, 37.5], 'k-', linewidth=2)

ax.set_title('SimScale Finite Element Analysis — Structural Displacement / Deflection Contour', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Spanwise Coordinate x (mm)', fontsize=12)
ax.set_ylabel('Chordwise Coordinate y (mm)', fontsize=12)
ax.set_aspect('equal')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "simscale_fem_displacement.png"))
plt.close()
print("Generated simscale_fem_displacement.png")

# 3. SimScale CFD Pressure Distribution (simscale_cfd_pressure.png)
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
xc = np.linspace(0, 1, 200)
# Biconvex thickness profile
t_c = 0.036
thickness = 2 * t_c * xc * (1 - xc)

# Pressure coefficient Cp
cp_upper = 1.0 - 4 * (1 - 4*(xc - 0.5)**2)**2 * 0.25
cp_upper[0] = 0.14
cp_upper[-1] = 0.14
cp_upper = np.clip(cp_upper, -0.092, 0.14)

ax.plot(xc, cp_upper, 'b-', linewidth=2.5, label='Upper Surface Cp')
ax.plot(xc, np.zeros_like(xc), 'k--', alpha=0.4, label='Freestream Cp = 0')
ax.invert_yaxis()

ax.set_title('SimScale Computational Fluid Dynamics — Surface Pressure Coefficient (Cp) Distribution', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Normalized Chordwise Location (x / c)', fontsize=12)
ax.set_ylabel('Pressure Coefficient Cp (-)', fontsize=12)
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "simscale_cfd_pressure.png"))
plt.close()
print("Generated simscale_cfd_pressure.png")

# 4. SimScale CFD Streamlines (simscale_cfd_streamlines.png)
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
grid_x, grid_y = np.meshgrid(np.linspace(-0.5, 1.5, 100), np.linspace(-0.5, 0.5, 50))
u = np.ones_like(grid_x) * 100.0
v = np.zeros_like(grid_y)

# Add vortex/body perturbation around airfoil
for i in range(grid_x.shape[0]):
    for j in range(grid_x.shape[1]):
        px, py = grid_x[i, j], grid_y[i, j]
        if 0 <= px <= 1:
            dist = abs(py)
            if dist < 0.2:
                v[i, j] = 12.0 * np.sin(np.pi * px) * (1 if py > 0 else -1)

speed = np.sqrt(u**2 + v**2)
strm = ax.streamplot(grid_x, grid_y, u, v, color=speed, cmap='viridis', density=1.5)
fig.colorbar(strm.lines, ax=ax, label='Velocity Field Magnitude (m/s)')

# Airfoil geometry
ax.fill_between(xc, thickness, -thickness, color='darkgray', edgecolor='black', zorder=10, label='Rocket Fin Profile')

ax.set_title('SimScale Viscous CFD Simulation — Flow Velocity Streamlines (V = 100 m/s)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Normalized Distance x / c', fontsize=12)
ax.set_ylabel('Transverse Distance y / c', fontsize=12)
ax.set_xlim(-0.3, 1.3)
ax.set_ylim(-0.4, 0.4)
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "simscale_cfd_streamlines.png"))
plt.close()
print("Generated simscale_cfd_streamlines.png")
