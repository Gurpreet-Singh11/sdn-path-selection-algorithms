# Wireshark Packet Capture Evidence

## Overview
Packet captures were taken simultaneously on Switch S2 (Path A)
and Switch S3 (Path B) using tcpdump inside Mininet network
namespaces. Captures confirm real TCP traffic flowed through
the experimental topology during all experiments.

---

## Capture Details

| Capture | Switch | Interface | File Size | Packets |
|---|---|---|---|---|
| Path A | S2 | s2-eth1 | 1.3 GB | 22,385,107 |
| Path B | S3 | s3-eth1 | 621 MB | Fewer than Path A |

---

## How Captures Were Taken

Step 1 — Start topology in Terminal 1:
sudo python3 topology.py

Step 2 — Start tcpdump inside Mininet namespaces:
s2 tcpdump -i s2-eth1 -w /home/gurpreet/networking_project/results/path_a_capture.pcap &
s3 tcpdump -i s3-eth1 -w /home/gurpreet/networking_project/results/path_b_capture.pcap &

Step 3 — Generate traffic:
h2 iperf3 -s &
h1 iperf3 -c 10.0.0.2 -b 9M -t 65 &

Step 4 — Run controller in Terminal 2:
python3 controller.py

Step 5 — Stop captures after controller finishes:
s2 pkill tcpdump
s3 pkill tcpdump

---

## Why tcpdump Runs Inside Mininet Namespace

Mininet creates virtual interfaces inside Linux network
namespaces. Running tcpdump from outside these namespaces
returns: s2-eth1: No such device exists

Solution: use Mininet CLI switch prefix to run commands
inside the correct namespace:
s2 tcpdump -i s2-eth1   means run inside Switch S2 namespace

---

## What Wireshark Shows

### Screenshot 1 — TCP Packet List
Filter: ip.src == 10.0.0.1 && tcp
Shows real TCP packets from H1 to H2 on port 5201 (iperf3)
Total: 22,385,107 packets on Path A alone

### Screenshot 2 — Protocol Stack
Shows complete network layers:
- Frame (physical layer)
- Ethernet II — MAC 00:00:00:00:00:01 to 00:00:00:00:00:02
- Internet Protocol — IP 10.0.0.1 to 10.0.0.2
- Transmission Control Protocol — Port 47502 to 5201

### Screenshot 3 — IO Graph
Statistics — IO Graph in Wireshark
Shows steady traffic rate for 60 seconds then drops to zero
Confirms controlled experiment duration

### Screenshot 4 — TCP SYN Handshake
Filter: tcp.flags.syn == 1
Shows SYN and SYN-ACK packets
Confirms proper TCP three-way handshake between hosts

### Screenshot 5 — Path A vs Path B Comparison
Path A: 22,385,107 packets (1.3 GB)
Path B: significantly fewer packets (621 MB)
Confirms controller successfully directed different
amounts of traffic to each path

---

## Connection to Textbook

| Evidence | Kurose and Ross Chapter |
|---|---|
| TCP three-way handshake (SYN/SYN-ACK) | Chapter 3 — Transport layer |
| TCP ports and sequence numbers | Chapter 3 — TCP segment structure |
| Complete protocol stack | Chapter 1 — Layered architecture |
| IP addresses in packet headers | Chapter 4 — Network layer |
| Traffic flowing through switches | Chapter 4 — Data plane forwarding |

---

## How to Open Captures

Open Path A capture in Wireshark:
sudo wireshark ~/networking_project/results/path_a_capture.pcap &

Apply filter to see only iperf3 traffic:
ip.src == 10.0.0.1 && tcp

See TCP handshake:
tcp.flags.syn == 1

See IO Graph:
Statistics — IO Graph

---

## Key Finding from Wireshark

Path A captured 1.3 GB vs Path B captured 621 MB.
This difference confirms the controller was making real
routing decisions and installing real OpenFlow flow rules
that successfully directed traffic between the two paths.
This is physical packet-level proof that the experimental
system worked correctly.
