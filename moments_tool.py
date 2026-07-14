"""
moments_tool.py  --  M2 and M4 restricted moments for the variance method
==========================================================================
You give it: a peak text file (two columns: q  I) and A0.
It gives   : a table (q'  M2  M4  M4/q'^2) ready to paste into Excel.

A0 options:
  - type a number  -> uses that (e.g. the fitted "Area Intg" from Origin)
  - press Enter     -> computes trapezoid A0 = sum(I*dq) from the data

q' range:
  - press Enter          -> all positive q up to the symmetric max
  - type "0.0004 0.0095" -> only q' in that range
"""
import numpy as np, sys, os

# ---- pick the file ----
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = input("Peak file name (e.g. peak7.txt): ").strip().strip('"')

q, I = np.loadtxt(fname, unpack=True)
order = np.argsort(q); q, I = q[order], I[order]
dq = np.median(np.diff(q))
A0_trap = np.sum(I) * dq
qsym = min(abs(q.min()), q.max())

print(f"\nLoaded {len(q)} points | dq = {dq:.6f}")
print(f"q from {q.min():.6f} to {q.max():.6f} | symmetric max = {qsym:.6f}")
print(f"peak top at q = {q[np.argmax(I)]:.6f}  (I = {I.max():.2f})")
print(f"trapezoid A0 (from data) = {A0_trap:.4f}")

# ---- A0 ----
a0_in = input(f"\nEnter A0 (or press Enter to use trapezoid {A0_trap:.4f}): ").strip()
A0 = float(a0_in) if a0_in else A0_trap
print(f"Using A0 = {A0:.4f}")

# ---- q' range ----
rng = input("q' range as 'low high' (or Enter for all up to symmetric max): ").strip()
if rng:
    lo, hi = map(float, rng.split())
else:
    lo, hi = 0.0, qsym
qprimes = q[(q > 0) & (q >= lo - dq/5) & (q <= hi + dq/5)]

# ---- compute ----
print("\n" + "="*60)
print("q'\tM2\tM4\tM4/q'^2")
rows = []
for qp in qprimes:
    m = np.abs(q) <= qp + dq/5
    M2 = np.sum(q[m]**2 * I[m]) * dq / A0
    M4 = np.sum(q[m]**4 * I[m]) * dq / A0
    rows.append((qp, M2, M4, M4/qp**2))
    print(f"{qp:.9f}\t{M2:.6E}\t{M4:.6E}\t{M4/qp**2:.6E}")

# ---- save a tab file you can double-click / import ----
out = os.path.splitext(fname)[0] + "_moments.txt"
with open(out, "w") as f:
    f.write("q'\tM2\tM4\tM4/q'^2\n")
    for r in rows:
        f.write(f"{r[0]:.9f}\t{r[1]:.6E}\t{r[2]:.6E}\t{r[3]:.6E}\n")
print("="*60)
print(f"Saved -> {out}   (open in Excel, or copy the printed table above)")