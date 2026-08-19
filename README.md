# SDN Path-Selection Algorithm Comparison

## Project Title
Comparative Evaluation of Congestion-Aware Path-Selection
Algorithms in Software-Defined Networks

## Course
COSC5906 — Advanced Topics of Computer Networks
Algoma University — 2026

## Student
Gurpreet Singh

---

## Overview

This project implements and compares four path-selection
algorithms in a Software-Defined Networking environment
emulated using Mininet. A Python-based SDN controller
manages an OpenFlow four-switch dual-path topology and
makes real routing decisions based on live traffic stats.


---

## Network Topology

H1 (10.0.0.1)
     |
 S1 (Entry Switch)
    /  \
   S2    S3
(Path A) (Path B)
    \  /
 S4 (Exit Switch)
     |
H2 (10.0.0.2)

---

## Four Algorithms Compared

Round-Robin — alternates paths blindly — no traffic check
Least-Utilized — picks less busy path right now
ECMP — hash formula assigns path permanently
Weighted-History — picks by rolling average of last 5 reads

---

## Experimental Results

12 runs total — 3 runs per algorithm
60 seconds per run — 9 Mbps iperf3 TCP traffic

Method           Run1  Run2  Run3  Average  Stability
Round-Robin        23    25    25     24.3       3.9%
Least-Utilized      1     1     1      1.0      96.1%
ECMP                0     0     0      0.0     100.0%
Weighted-History    1     1     1      1.0      96.1%


---

## Key Finding

Round-Robin — 24.3 average switches — 3.9% stability
Worst performer — completely blind to traffic conditions

ECMP — 0.0 average switches — 100% stability
Most stable — deterministic hash never changes path

Least-Utilized — 1.0 average switches — 96.1% stability
Traffic aware — reacts instantly to congestion

Weighted-History — 1.0 average switches — 96.1% stability
Best overall — smart and stable — RECOMMENDED

---

## Wireshark Evidence

Path A capture: 1.3 GB — 22,385,107 packets
Path B capture: 621 MB
Source: 10.0.0.1 to Destination: 10.0.0.2
Protocol: TCP Port 5201 (iperf3)
Confirms real traffic flowed through real virtual switches

---

## Tools Used

Mininet 2.3.0 — network emulation
Open vSwitch 2.17.9 — virtual switches
Python 3.10.12 — controller programming
iperf3 3.9 — traffic generation
Wireshark — packet capture and analysis
matplotlib — graph generation
numpy — numerical calculations

---

## Project Files

topology.py — creates 4-switch dual-path network
controller.py — four routing algorithms
analyze.py — generates comparison graphs
algorithms/ — documentation for each algorithm
results/ — experiment data and captures
graphs/ — three comparison bar charts

---

## Documentation Files

SETUP.md — installation and environment guide
TOPOLOGY.md — network design and flow rules
CONTROLLER.md — controller design and algorithms
RESULTS.md — all experiment results and analysis
EXPERIMENTS.md — experiment procedure documentation
CHALLENGES.md — five technical problems and solutions
WIRESHARK.md — packet capture evidence
TEXTBOOK.md — connection to Kurose and Ross chapters
DEMO.md — complete live demo guide
algorithms/ — individual algorithm documentation

---

## How to Run

Step 1 — Install requirements:
sudo apt install mininet iperf3 wireshark -y
pip3 install matplotlib numpy

Step 2 — Start topology:
sudo mn -c && sudo python3 topology.py

Step 3 — Start traffic at mininet prompt:
h2 iperf3 -s &
h1 iperf3 -c 10.0.0.2 -b 9M -t 120 &

Step 4 — Run an algorithm:
sed -i 's/ROUTING_MODE = .*/ROUTING_MODE = "ecmp"/' controller.py
python3 controller.py

Step 5 — Generate graphs:
python3 analyze.py

---

## Connection to Textbook — Kurose and Ross

OVS flow tables — Chapter 4 match-plus-action forwarding
controller.py — Chapter 5.5 SDN control plane
Four algorithms — Chapter 5.2 routing algorithms
Wireshark captures — Chapter 3 transport layer TCP
Two-path topology — Chapter 4 network layer

---

## Challenges Overcome

1. Ryu incompatible with Python 3.10
   Solution: replaced with direct ovs-ofctl calls

2. Mininet pingall 100% packet loss
   Solution: failMode=standalone with install_flows()

3. OVS stats always returning zero
   Solution: regex DOTALL parser with port number search

4. tcpdump no such device error
   Solution: ran inside Mininet network namespace

5. Cumulative stats blocking congestion detection
   Solution: rate-of-change bytes per second measurement
