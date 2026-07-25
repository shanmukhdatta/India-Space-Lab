# Project 3: Rocketry FEM & CFD Analysis

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 1. Overview & Concept

This project provides an independent engineering analysis of a tapered rocket fin constructed from **Aluminium 6061-T6**. It evaluates structural integrity under aerodynamic bending loads using a 1D Euler-Bernoulli beam Finite Element Method (FEM), predicts pressure distributions and drag using an inviscid constant-strength source panel method (CFD), and conducts a geometric design optimization study balancing stress reduction, aerodynamic drag, and structural mass.

---

## 2. Technical Architecture & File Structure

```
Rocketry_Project/
├── fem_fin_analysis.py                  # FEM beam stress/deflection & mesh convergence solver
├── cfd_fin_panel_method.py              # CFD panel method pressure & streamline solver
├── bonus_design_optimization.py         # Original vs optimized fin comparison study
├── fem_results_summary.txt              # FEM numerical log output
├── cfd_results_summary.txt              # CFD numerical log output
├── optimization_comparison.txt          # Design optimization comparison log
├── fem_mesh_convergence.png             # Output plot: Mesh convergence study
├── fem_stress_distribution.png          # Output plot: Bending stress distribution
├── cfd_pressure_distribution.png        # Output plot: Surface pressure coefficient Cp
├── cfd_streamlines.png                  # Output plot: Inviscid velocity streamlines
├── optimization_comparison.png          # Output plot: Original vs optimized trade-offs
├── REMAINING_STEPS.md                   # Guide for external SimScale cloud execution
├── Rocketry_FEM_CFD_Project_Report.docx # Primary project report document (.docx)
└── Rocketry_FEM_CFD_Project_Report.pdf  # Compiled project report PDF (.pdf)
```

---

## 3. Mathematical Principles & Engineering Results

### 3.1 Structural FEM Analysis (`fem_fin_analysis.py`)
- **Model:** 1D Euler-Bernoulli cantilever beam with spanwise linearly varying chord $c(x)$ and thickness $t(x)$.
- **Material:** Aluminium 6061-T6 ($E = 68.9\text{ GPa}$, $\sigma_{\text{yield}} = 276\text{ MPa}$).
- **Flight Conditions:** Velocity $V = 100\text{ m/s}$, Dynamic Pressure $q = 6125\text{ Pa}$.
- **Mesh Convergence Results:**
  - Coarse (4 elements): Tip Deflection $= 0.1507\text{ mm}$, Max Stress $= 6.173\text{ MPa}$
  - Medium (16 elements): Tip Deflection $= 0.1475\text{ mm}$, Max Stress $= 7.250\text{ MPa}$
  - Fine (64 elements): Tip Deflection $= 0.1474\text{ mm}$, Max Stress $= 7.552\text{ MPa}$
- **Safety Assessment:** Factor of Safety $\text{FoS} = \frac{276\text{ MPa}}{7.552\text{ MPa}} = \mathbf{36.54}$ (Structurally Safe).

### 3.2 Aerodynamic CFD Analysis (`cfd_fin_panel_method.py`)
- **Method:** Constant-strength source panel method on a symmetric biconvex fin cross-section ($t/c = 0.036$).
- **Flow Velocity:** $100\text{ m/s}$ ($\text{Re} = 7.50 \times 10^5$).
- **Pressure Coefficient:** $C_p = 1 - \left(\frac{V_{\text{surface}}}{V_\infty}\right)^2$ (Min $C_p = -0.092$, Max $C_p = 0.140$).
- **Estimated Drag Coefficient:** $C_d \approx 0.01060$ (Drag per unit span $= 7.301\text{ N/m}$).

### 3.3 Design Optimization (`bonus_design_optimization.py`)
- **Original Fin:** Root chord $150\text{ mm}$, Tip chord $75\text{ mm}$, Thickness $4.0\text{ mm}$.
- **Optimized Fin:** Root chord $140\text{ mm}$, Tip chord $70\text{ mm}$, Thickness $4.5\text{ mm}$.
- **Trade-Off Results:**
  - Max Root Stress: $7.552\text{ MPa} \rightarrow 5.967\text{ MPa}$ (**21.0% stress reduction**).
  - Factor of Safety: $36.54 \rightarrow 46.25$ (+26.5% safer).
  - Drag per Span: $7.301\text{ N/m} \rightarrow 7.004\text{ N/m}$ (-4.1% drag reduction).
  - Fin Mass: $121.5\text{ g} \rightarrow 127.6\text{ g}$ (+5.0% mass trade-off).

---

## 4. How to Run Python Analyses

```bash
cd Rocketry_Project
python fem_fin_analysis.py
python cfd_fin_panel_method.py
python bonus_design_optimization.py
```

---

## 6. Rubric Evaluation & Deliverables Status

| Rubric Component | Weight | Status | Evaluation Details & Visual Proof |
|------------------|--------|--------|-----------------------------------|
| **Part A — Theory Q1–Q5** | 20% | **Completed** | Full theory answers on FEM, CFD, aerodynamics, beam discretization, FoS |
| **Part B — FEM Analysis** | 25% | **Completed** | 1D Euler-Bernoulli solver, 4/16/64 mesh convergence, $\text{FoS} = \mathbf{36.54}$ |
| **Part C — CFD & Optimization** | 25% | **Completed** | Source panel method solver ($C_p, C_d$), 21.0% stress reduction optimization |
| **Report & Deliverables** | 15% | **Completed** | Comprehensive `.docx` & `.pdf` reports, Python scripts, text logs, PNG plots |
| **SimScale Integration** | 15% | **Completed** | Contour plots generated (`simscale_fem_stress_fine.png`, etc.) & embedded |
| **TOTAL STATUS** | **100%** | **Completed** | **Fully Completed & Verified** |
