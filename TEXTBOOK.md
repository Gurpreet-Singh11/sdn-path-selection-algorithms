# Connection to Kurose and Ross Textbook

## Overview
Every component of this project maps directly to concepts
from Computer Networking: A Top-Down Approach by
Kurose and Ross (8th Edition).

This project makes textbook theory real and measurable.
Instead of reading about how networks work, we built a
working network and proved the concepts with real data.

---

## Chapter 1 — Introduction and Performance Metrics

### What the textbook says
Chapter 1 introduces network performance metrics including
throughput (how much data flows per second) and delay
(how long packets take to travel). It also introduces
packet switching — data broken into small chunks called
packets that travel independently through the network.

### How our project connects
- iperf3 generates 9 Mbps traffic — throughput measurement
- Path switch count measures routing stability — affects delay
- All traffic broken into TCP/IP packets through 4 switches
- Comparing Round-Robin vs ECMP is evaluating performance
  using quantifiable metrics exactly as Chapter 1 describes

---

## Chapter 3 — Transport Layer and TCP

### What the textbook says
Chapter 3 explains TCP including:
- Three-way handshake (SYN, SYN-ACK, ACK)
- Port numbers identifying applications
- Sequence numbers for ordering packets
- Flow control using window size

### How our project connects
- Wireshark Screenshot 3 shows real SYN and SYN-ACK packets
- Port 5201 (iperf3) visible in all packet captures
- Sequence numbers visible in Wireshark packet details
- TCP window size shown in packet inspection
- All iperf3 traffic uses TCP — every Chapter 3 concept
  is visible in our real Wireshark captures

---

## Chapter 4 — Network Layer and Data Plane

### What the textbook says
Chapter 4 explains:
- Forwarding — switch looks at destination and decides port
- Match-plus-action — if packet matches this, do this action
- Flow tables — collection of all match-plus-action rules
- Data plane — the part that actually moves packets

### How our project connects
- Each OVS switch has a real flow table
- install_flows() writes real match-plus-action rules
- Example rule: dl_dst=00:00:00:00:00:02, actions=output:2
  This is exactly match-plus-action from Chapter 4
- Switches S1 S2 S3 S4 are the data plane
- They just forward packets — no thinking required

---

## Chapter 5 — Network Layer and Control Plane

### What the textbook says
Chapter 5 covers:
- Routing algorithms — how to choose which path
- SDN architecture — one controller manages all switches
- Control vs data plane separation
- OpenFlow protocol for controller-switch communication

### How our project connects
- controller.py IS the SDN controller from Chapter 5.5
- Four algorithms ARE four different routing approaches
- get_path_utilization() collects link-state information
- ovs-ofctl add-flow sends OpenFlow Flow-Mod messages
- Switches are data plane — they just follow rules
- Controller is control plane — it makes all decisions
- Changing ROUTING_MODE changes entire network behavior
  by updating ONE Python file — perfect demonstration
  of why Chapter 5 says SDN is powerful

---

## Mapping Table

| Project Component | Textbook Concept | Chapter |
|---|---|---|
| iperf3 9 Mbps traffic | Throughput measurement | Ch. 1 |
| TCP/IP packets | Packet switching | Ch. 1 |
| Wireshark SYN/SYN-ACK | TCP three-way handshake | Ch. 3 |
| Port 5201 in captures | TCP port numbers | Ch. 3 |
| Sequence numbers visible | TCP reliable delivery | Ch. 3 |
| OVS flow tables | Match-plus-action forwarding | Ch. 4 |
| install_flows() rules | Flow table entries | Ch. 4 |
| ovs-ofctl add-flow | OpenFlow Flow-Mod message | Ch. 4.4 |
| S1 S2 S3 S4 switches | Data plane | Ch. 4 |
| controller.py | SDN control plane | Ch. 5.5 |
| Four algorithms | Routing algorithms | Ch. 5.2 |
| Rate measurement | Link-state information | Ch. 5 |
| One controller all switches | Centralized SDN control | Ch. 5.5 |

---

## The Most Important Connection

Chapter 5.5 of Kurose and Ross describes SDN as:

"The control plane is physically separate from the
data plane. A single controller determines forwarding
rules for all switches. Switches are simple forwarding
devices programmed by the controller."

Our project IS this exact architecture:
- controller.py = the control plane (the brain)
- S1 S2 S3 S4 = the data plane (the muscle)
- ovs-ofctl commands = the OpenFlow communication
- ROUTING_MODE switch = demonstrates programmability

Simply changing one line of code changes how the
entire network behaves — this is exactly what
Chapter 5 means when it says SDN enables
network-wide control from a single point.
