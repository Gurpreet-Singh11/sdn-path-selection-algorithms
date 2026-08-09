# SDN Controller

## Overview
Python program that reads traffic stats from switches
every 2 seconds and makes path selection decisions.

## Four Algorithms

### Round-Robin
Alternates paths blindly. No traffic checking.
Result: 24.3 average switches. Stability 3.9%

### Least-Utilized
Picks less busy path right now.
Result: 1.0 average switches. Stability 96.1%

### ECMP - Equal Cost Multi Path
Uses hash formula. Never changes path.
Result: 0.0 average switches. Stability 100%

### Weighted-History
Picks based on average of last 5 readings.
Result: 1.0 average switches. Stability 96.1%

## How to Run

Change mode in controller.py:
ROUTING_MODE = "round_robin"
ROUTING_MODE = "least_utilized"
ROUTING_MODE = "ecmp"
ROUTING_MODE = "weighted_history"

Run controller:
python3 controller.py

## Output Example
[2.1s] Mode=round_robin | Path=A | Switches=0
[4.2s] Mode=round_robin | Path=B | Switches=1
Total decisions: 26
Total path switches: 24
