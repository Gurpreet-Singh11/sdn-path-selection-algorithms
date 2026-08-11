#!/usr/bin/env python3
"""
Project: Comparative Evaluation of Path-Selection Algorithms in SDN
File: analyze.py
Description: Generates comparison graphs from real experiment results
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os

# ─────────────────────────────────────────
# YOUR REAL EXPERIMENTAL RESULTS
# ─────────────────────────────────────────

results = {
    'Round-Robin': {
        'path_switches': [23, 25, 25],
    },
    'Least-Utilized': {
        'path_switches': [1, 1, 1],
    },
    'ECMP': {
        'path_switches': [0, 0, 0],
    },
    'Weighted-History': {
        'path_switches': [1, 1, 1],
    }
}

# Calculate averages and standard deviations
methods = list(results.keys())
avg_switches = [
    np.mean(results[m]['path_switches']) for m in methods
]
std_switches = [
    np.std(results[m]['path_switches']) for m in methods
]

# Colors for each method
colors = ['#E74C3C', '#2ECC71', '#3498DB', '#9B59B6']

# Output directory
GRAPHS_DIR = os.path.expanduser('~/networking_project/graphs')
os.makedirs(GRAPHS_DIR, exist_ok=True)

# ─────────────────────────────────────────
# GRAPH 1 — Average Path Switches
# ─────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(methods, avg_switches,
              color=colors,
              width=0.5,
              edgecolor='black',
              linewidth=0.8)

# Add error bars
ax.errorbar(methods, avg_switches,
            yerr=std_switches,
            fmt='none',
            color='black',
            capsize=5,
            linewidth=1.5)

# Add value labels on bars
for bar, val in zip(bars, avg_switches):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.3,
            f'{val:.1f}',
            ha='center', va='bottom',
            fontsize=12, fontweight='bold')

ax.set_xlabel('Path Selection Algorithm', fontsize=13)
ax.set_ylabel('Average Path Switches', fontsize=13)
ax.set_title(
    'Average Path Switches per Algorithm\n'
    '(Lower = More Stable)',
    fontsize=14, fontweight='bold'
)
ax.set_ylim(0, max(avg_switches) * 1.3)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
path1 = f'{GRAPHS_DIR}/graph1_path_switches.png'
plt.savefig(path1, dpi=150, bbox_inches='tight')
plt.close()
print(f'Graph 1 saved: {path1}')

# ─────────────────────────────────────────
# GRAPH 2 — Stability Comparison
# (inverted switches — higher = more stable)
# ─────────────────────────────────────────

max_switches = max(avg_switches)
stability_scores = [
    round((1 - (s / (max_switches + 1))) * 100, 1)
    for s in avg_switches
]

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(methods, stability_scores,
              color=colors,
              width=0.5,
              edgecolor='black',
              linewidth=0.8)

for bar, val in zip(bars, stability_scores):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{val:.1f}%',
            ha='center', va='bottom',
            fontsize=12, fontweight='bold')

ax.set_xlabel('Path Selection Algorithm', fontsize=13)
ax.set_ylabel('Stability Score (%)', fontsize=13)
ax.set_title(
    'Routing Stability Score per Algorithm\n'
    '(Higher = More Stable)',
    fontsize=14, fontweight='bold'
)
ax.set_ylim(0, 115)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
path2 = f'{GRAPHS_DIR}/graph2_stability.png'
plt.savefig(path2, dpi=150, bbox_inches='tight')
plt.close()
print(f'Graph 2 saved: {path2}')

# ─────────────────────────────────────────
# GRAPH 3 — Individual Run Results
# (shows consistency across runs)
# ─────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(methods))
width = 0.25
runs = ['Run 1', 'Run 2', 'Run 3']
run_colors = ['#2C3E50', '#7F8C8D', '#BDC3C7']

for i, (run, rcolor) in enumerate(zip(runs, run_colors)):
    run_data = [
        results[m]['path_switches'][i] for m in methods
    ]
    bars = ax.bar(x + i * width, run_data,
                  width, label=run,
                  color=rcolor,
                  edgecolor='black',
                  linewidth=0.8)

ax.set_xlabel('Path Selection Algorithm', fontsize=13)
ax.set_ylabel('Path Switches', fontsize=13)
ax.set_title(
    'Path Switches per Run — All Algorithms\n'
    '(Consistency across 3 runs)',
    fontsize=14, fontweight='bold'
)
ax.set_xticks(x + width)
ax.set_xticklabels(methods)
ax.legend(fontsize=11)
ax.set_ylim(0, max(avg_switches) * 1.4)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
path3 = f'{GRAPHS_DIR}/graph3_per_run.png'
plt.savefig(path3, dpi=150, bbox_inches='tight')
plt.close()
print(f'Graph 3 saved: {path3}')

# ─────────────────────────────────────────
# PRINT SUMMARY TABLE
# ─────────────────────────────────────────

print('\n' + '='*55)
print('  FINAL RESULTS SUMMARY')
print('='*55)
print(f"  {'Method':<20} {'Avg Switches':<15} {'Stability'}")
print('  ' + '-'*50)
for m, avg, stab in zip(methods, avg_switches, stability_scores):
    print(f"  {m:<20} {avg:<15.1f} {stab:.1f}%")
print('='*55)
print(f'\n  Graphs saved to: {GRAPHS_DIR}')
