# Experiment Documentation

## Setup
- Platform: Mininet 2.3 on Ubuntu 22.04
- Traffic tool: iperf3 at 9 Mbps for 60 seconds
- Controller polling: every 2 seconds
- Runs per method: 3
- Total runs: 12

## Experiment Procedure

Step 1: sudo mn -c
Step 2: sudo python3 topology.py
Step 3: pingall (verify 0% dropped)
Step 4: h2 iperf3 -s &
Step 5: h1 iperf3 -c 10.0.0.2 -b 9M -t 120 &
Step 6: Wait 5 seconds
Step 7: python3 controller.py
Step 8: Record Total path switches
Step 9: exit then sudo mn -c
Step 10: Repeat

## Results by Method

### Round-Robin
Run 1: 23 path switches
Run 2: 25 path switches
Run 3: 25 path switches
Average: 24.3
Stability: 3.9%

### Least-Utilized
Run 1: 1 path switch
Run 2: 1 path switch
Run 3: 1 path switch
Average: 1.0
Stability: 96.1%

### ECMP
Run 1: 0 path switches
Run 2: 0 path switches
Run 3: 0 path switches
Average: 0.0
Stability: 100.0%

### Weighted-History
Run 1: 1 path switch
Run 2: 1 path switch
Run 3: 1 path switch
Average: 1.0
Stability: 96.1%

## Wireshark Evidence

Path A capture: 1.3 GB — 22,385,107 packets
Path B capture: 621 MB
Source: 10.0.0.1 (H1)
Destination: 10.0.0.2 (H2)
Protocol: TCP Port 5201 (iperf3)
