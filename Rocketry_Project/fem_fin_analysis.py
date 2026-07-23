"""
PART B - FEM Project (independent Python engineering check)
------------------------------------------------------------
This script performs a simplified 1D Euler-Bernoulli beam FEM analysis of a
tapered rocket fin, treated as a cantilever fixed at the root and loaded by
a distributed aerodynamic pressure along its span. It is NOT a substitute
for the full 3D FEM you must run in SimScale, but gives a genuine,
independently computed engineering estimate (stress, deflection, factor of
safety) and demonstrates the mesh-convergence concept (coarse/medium/fine)
required by Task 3 of the assignment.

Run: python fem_fin_analysis.py
Outputs:
    fem_mesh_convergence.png
    fem_stress_distribution.png
    fem_results_summary.txt
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. Geometry (Task 1: Rocket Fin Geometry)
# ---------------------------------------------------------------
root_chord = 0.150      # m
tip_chord = 0.075       # m
span = 0.100            # m  (fin height from root to tip)
thickness = 0.004        # m  (uniform fin thickness)

# ---------------------------------------------------------------
# 2. Material properties (Task 1: Material) - Aluminium 6061-T6
# ---------------------------------------------------------------
E = 68.9e9               # Pa, Young's modulus
yield_strength = 276e6    # Pa
density = 2700            # kg/m^3

# ---------------------------------------------------------------
# 3. Aerodynamic load (Task 2: Boundary Conditions)
# ---------------------------------------------------------------
rho_air = 1.225           # kg/m^3, sea-level air density
V = 100.0                 # m/s, assumed rocket velocity at max-Q-ish phase
q_dynamic = 0.5 * rho_air * V ** 2   # dynamic pressure, Pa

# Assumption: aerodynamic pressure acts uniformly (as an approximation)
# perpendicular to the fin surface, giving a distributed transverse load
# per unit span of w(x) = q_dynamic * chord(x)


def chord_at(x):
    """Linear taper from root_chord at x=0 to tip_chord at x=span."""
    return root_chord + (tip_chord - root_chord) * (x / span)


def I_at(x):
    """Second moment of area of the rectangular (chord x thickness) section
    about the bending (span-wise) neutral axis."""
    return chord_at(x) * thickness ** 3 / 12.0


def w_at(x):
    """Distributed transverse load per unit span (N/m)."""
    return q_dynamic * chord_at(x)


# ---------------------------------------------------------------
# 4. Beam FEM solver (2-node Euler-Bernoulli elements, cantilever)
# ---------------------------------------------------------------
def solve_beam_fem(n_elements):
    n_nodes = n_elements + 1
    le = span / n_elements
    ndof = 2 * n_nodes

    K = np.zeros((ndof, ndof))
    F = np.zeros(ndof)
    x_nodes = np.linspace(0, span, n_nodes)

    for e in range(n_elements):
        x_mid = 0.5 * (x_nodes[e] + x_nodes[e + 1])
        EI = E * I_at(x_mid)
        w = w_at(x_mid)

        # standard Euler-Bernoulli element stiffness matrix
        ke = (EI / le ** 3) * np.array([
            [12,      6 * le,   -12,      6 * le],
            [6 * le,  4 * le**2, -6 * le, 2 * le**2],
            [-12,    -6 * le,    12,     -6 * le],
            [6 * le,  2 * le**2, -6 * le, 4 * le**2],
        ])

        # consistent nodal load vector for a uniformly distributed load w
        fe = w * le * np.array([0.5, le / 12, 0.5, -le / 12])

        dofs = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        for i in range(4):
            F[dofs[i]] += fe[i]
            for j in range(4):
                K[dofs[i], dofs[j]] += ke[i, j]

    # Boundary condition: fixed at root -> v0 = 0, theta0 = 0
    free_dofs = list(range(2, ndof))
    Kff = K[np.ix_(free_dofs, free_dofs)]
    Ff = F[free_dofs]
    d_free = np.linalg.solve(Kff, Ff)

    d = np.zeros(ndof)
    d[free_dofs] = d_free

    deflections = d[0::2]

    # recover bending moment at each node using curvature * EI (central
    # differences on the rotation field, which is d[1::2])
    thetas = d[1::2]
    moments = np.zeros(n_nodes)
    for i in range(n_nodes):
        x_i = x_nodes[i]
        EI_i = E * I_at(x_i)
        if i == 0:
            dtheta_dx = (thetas[1] - thetas[0]) / le
        elif i == n_nodes - 1:
            dtheta_dx = (thetas[i] - thetas[i - 1]) / le
        else:
            dtheta_dx = (thetas[i + 1] - thetas[i - 1]) / (2 * le)
        moments[i] = EI_i * dtheta_dx

    stresses = np.abs(moments) * (thickness / 2) / (E * 0 + np.array([I_at(x) for x in x_nodes]))

    return x_nodes, deflections, moments, stresses


# ---------------------------------------------------------------
# 5. Mesh study (Task 3): coarse, medium, fine
# ---------------------------------------------------------------
mesh_levels = {"Coarse (4 elements)": 4, "Medium (16 elements)": 16, "Fine (64 elements)": 64}
results = {}

for label, n in mesh_levels.items():
    x_nodes, deflections, moments, stresses = solve_beam_fem(n)
    results[label] = {
        "x": x_nodes,
        "deflection": deflections,
        "stress": stresses,
        "tip_deflection": deflections[-1],
        "max_stress": np.max(stresses),
    }

print("Mesh Convergence Study")
print("-" * 60)
for label, r in results.items():
    print(f"{label:28s} | Tip deflection = {r['tip_deflection']*1000:7.4f} mm | "
          f"Max root stress = {r['max_stress']/1e6:7.3f} MPa")

# ---------------------------------------------------------------
# 6. Plot: mesh convergence
# ---------------------------------------------------------------
n_list = list(mesh_levels.values())
tip_defl_list = [results[l]["tip_deflection"] * 1000 for l in mesh_levels]
max_stress_list = [results[l]["max_stress"] / 1e6 for l in mesh_levels]

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(n_list, tip_defl_list, "o-", color="tab:blue", label="Tip deflection (mm)")
ax1.set_xlabel("Number of elements (mesh refinement)")
ax1.set_ylabel("Tip deflection (mm)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(n_list, max_stress_list, "s--", color="tab:red", label="Max root stress (MPa)")
ax2.set_ylabel("Max root Von Mises-equivalent stress (MPa)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.title("Mesh Convergence Study - Tapered Fin Cantilever Beam FEM")
fig.tight_layout()
plt.savefig("fem_mesh_convergence.png", dpi=150)
print("Saved fem_mesh_convergence.png")

# ---------------------------------------------------------------
# 7. Plot: stress distribution along span (finest mesh)
# ---------------------------------------------------------------
finest = results["Fine (64 elements)"]
plt.figure(figsize=(8, 5))
plt.plot(finest["x"] * 1000, finest["stress"] / 1e6, color="tab:red", linewidth=2)
plt.axhline(yield_strength / 1e6, color="black", linestyle="--", label=f"Yield strength ({yield_strength/1e6:.0f} MPa)")
plt.xlabel("Distance from root (mm)")
plt.ylabel("Bending stress (MPa)")
plt.title("Bending Stress Distribution Along Fin Span (fine mesh)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("fem_stress_distribution.png", dpi=150)
print("Saved fem_stress_distribution.png")

# ---------------------------------------------------------------
# 8. Factor of safety (Task 5)
# ---------------------------------------------------------------
max_stress_fine = finest["max_stress"]
FoS = yield_strength / max_stress_fine

with open("fem_results_summary.txt", "w") as f:
    f.write("FEM Fin Analysis Summary\n")
    f.write("=" * 40 + "\n")
    f.write(f"Dynamic pressure q = {q_dynamic:.2f} Pa (V = {V} m/s)\n")
    f.write(f"Root chord = {root_chord*1000:.1f} mm, Tip chord = {tip_chord*1000:.1f} mm\n")
    f.write(f"Span = {span*1000:.1f} mm, Thickness = {thickness*1000:.1f} mm\n")
    f.write(f"Material: Aluminium 6061-T6 (E={E/1e9:.1f} GPa, Yield={yield_strength/1e6:.0f} MPa)\n\n")
    f.write("Mesh Convergence:\n")
    for label, r in results.items():
        f.write(f"  {label:28s} Tip defl = {r['tip_deflection']*1000:.4f} mm, "
                f"Max stress = {r['max_stress']/1e6:.3f} MPa\n")
    f.write(f"\nMax root stress (finest mesh) = {max_stress_fine/1e6:.3f} MPa\n")
    f.write(f"Factor of Safety = Yield / Max Stress = {FoS:.2f}\n")
    f.write("Structural status: " + ("SAFE" if FoS > 1.5 else "UNSAFE / MARGINAL") + "\n")

print(f"\nFactor of Safety = {FoS:.2f} -> {'SAFE' if FoS > 1.5 else 'UNSAFE/MARGINAL'}")
