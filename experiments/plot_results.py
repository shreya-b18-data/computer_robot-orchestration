"""Plot results/results.csv: success rates and path efficiency.

Usage (from the project root, after run_experiment.py):
    python experiments/plot_results.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "results" / "results.csv")
n = len(df)

# 1. Success rate (with 95% normal-approximation error bars)
methods = {"Greedy": "greedy_success", "Q-learning": "q_success"}
rates = [df[col].mean() for col in methods.values()]
errors = [1.96 * (r * (1 - r) / n) ** 0.5 for r in rates]

fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(list(methods), rates, yerr=errors, capsize=6, color=["#999999", "#4c78a8"])
ax.set_ylim(0, 1.05)
ax.set_ylabel("Success rate")
ax.set_title(f"Reached the goal ({n} random grids)")
fig.tight_layout()
fig.savefig(ROOT / "results" / "success_rate.png", dpi=150)
plt.close(fig)

# 2. Path efficiency: extra steps over the A* optimum, on trials where the method succeeded
fig, ax = plt.subplots(figsize=(5, 4))
data, labels = [], []
for label, steps_col, ok_col in [("Greedy", "greedy_steps", "greedy_success"),
                                 ("Q-learning", "q_steps", "q_success")]:
    ok = df[df[ok_col] == 1]
    data.append((ok[steps_col] - ok["optimal_steps"]).tolist())
    labels.append(f"{label}\n(n={len(ok)})")
ax.boxplot(data)
ax.set_xticklabels(labels)
ax.set_ylabel("Extra steps vs. A* optimal")
ax.set_title("Path efficiency (successful trials only)")
fig.tight_layout()
fig.savefig(ROOT / "results" / "path_efficiency.png", dpi=150)
plt.close(fig)

print("Saved results/success_rate.png and results/path_efficiency.png")