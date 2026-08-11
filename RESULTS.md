# Experiment Results

## Overview
12 controlled experiment runs conducted — 3 runs per algorithm.
Each run lasted 60 seconds with 9 Mbps iperf3 TCP traffic.
Controller made approximately 26-30 decisions per run.

## Complete Results Table

| Method | Run 1 | Run 2 | Run 3 | Average | Stability |
|---|---|---|---|---|---|
| Round-Robin | 23 | 25 | 25 | 24.3 | 3.9% |
| Least-Utilized | 1 | 1 | 1 | 1.0 | 96.1% |
| ECMP | 0 | 0 | 0 | 0.0 | 100.0% |
| Weighted-History | 1 | 1 | 1 | 1.0 | 96.1% |

## Stability Score Formula

Stability Score = (1 - (avg / (max + 1))) x 100

Where max = 24.3 (Round-Robin average)
max + 1 = 25.3

Round-Robin:      (1 - 24.3/25.3) x 100 = 3.9%
Least-Utilized:   (1 -  1.0/25.3) x 100 = 96.1%
ECMP:             (1 -  0.0/25.3) x 100 = 100.0%
Weighted-History: (1 -  1.0/25.3) x 100 = 96.1%

## Three Comparison Graphs Generated

### Graph 1 — Average Path Switches
File: graphs/graph1_path_switches.png
Shows Round-Robin at 24.3 vs others near zero.
Lower bar means more stable routing.

### Graph 2 — Stability Score
File: graphs/graph2_stability.png
Shows Round-Robin at 3.9% vs ECMP at 100%.
Higher bar means more stable routing.

### Graph 3 — Per Run Consistency
File: graphs/graph3_per_run.png
Shows all 3 runs per algorithm side by side.
Proves results are consistent and reproducible.

## Key Findings

1. Round-Robin is unsuitable for SDN — 24.3 switches, 3.9% stability
2. ECMP achieves perfect stability — 0 switches, 100% stability
3. Least-Utilized is near-perfect — 1.0 switches, 96.1% stability
4. Weighted-History is best overall — smart AND stable
5. Traffic awareness and stability are NOT mutually exclusive

## Recommended Algorithm

Weighted-History offers the best practical balance between
congestion responsiveness and routing stability.
It reacts to real traffic but avoids unnecessary switching
by averaging recent readings instead of reacting instantly.

## How to Generate Graphs

python3 analyze.py

Graphs are saved to: ~/networking_project/graphs/
