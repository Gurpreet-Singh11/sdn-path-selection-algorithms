# Challenges and Solutions

## Overview
Five major technical challenges were encountered and resolved
during this project. Each challenge is documented here with
its root cause and the solution applied.

---

## Challenge 1 — Ryu Incompatible with Python 3.10

### Problem
After installing Ryu, running ryu-manager failed with:
- ImportError: cannot import ALREADY_HANDLED from eventlet.wsgi
- AttributeError: module collections has no attribute MutableMapping
- TypeError: cannot set is_timeout attribute of immutable type
- AttributeError: get_script_args not found in setuptools

### Root Cause
Ryu was last updated in 2020 and designed for Python 3.6-3.8.
Ubuntu 22.04 ships with Python 3.10 which removed several
functions and changed behaviors that Ryu depends on.

### What We Tried
- Downgrading eventlet to version 0.30.2
- Downgrading setuptools to version 58.2.0
- Installing Ryu from faucetsdn patched fork
- Creating Python 3.9 virtual environment
- Using --no-build-isolation pip flag

### Solution
Replaced Ryu entirely with direct OVS flow management
using ovs-ofctl commands called from Python subprocess.
This provides equivalent OpenFlow functionality without
any framework compatibility issues.

---

## Challenge 2 — Mininet pingall 100% Packet Loss

### Problem
After building the topology with 4 switches and 2 hosts,
pingall consistently showed 100% packet loss even though
all links showed OK OK status.

### Root Cause
Switches were operating in secure mode — they dropped all
packets when no controller was actively connected.
Also ovs-testcontroller was already running on port 6653
blocking new connections.

### What We Tried
- Using POX controller l2_learning module — DNS parsing errors
- Using Mininet built-in Controller class — executable not found
- Installing openvswitch-testcontroller — port conflict
- Manually setting fail-mode via ovs-vsctl — no such file error

### Solution
Set failMode=standalone directly in topology.py when
creating each switch. Combined with controller=None and
automatic flow rule installation using install_flows()
function. Each switch programmed with explicit forwarding
rules for H1 and H2 MAC addresses plus ARP flooding.

---

## Challenge 3 — OVS Traffic Stats Always Returning Zero

### Problem
The controller get_port_stats function always returned 0 bytes
for both paths even when iperf3 was generating gigabytes of
traffic. All four algorithms behaved identically because both
paths appeared equally busy at zero.

### Root Cause — Three Issues
Issue 1: Searched for port names like s2-eth1 but actual OVS
output used port numbers — port 1, port 2.

Issue 2: OVS output wrapped long lines across multiple lines.
Parser looked for tx line right after port line but a wrapped
continuation appeared between them.

Issue 3: Running topology in background caused it to stop
when terminal session changed.

### Solution
Used regex with DOTALL flag to match port sections regardless
of line wrapping. Searched by port number pattern instead of
port name. Switched from cumulative bytes to rate of change
measurement — bytes per second between consecutive readings.

---

## Challenge 4 — tcpdump Cannot Access Mininet Interfaces

### Problem
Running sudo tcpdump -i s2-eth1 from regular terminal showed:
s2-eth1: No such device exists (SIOCGIFHWADDR: No such device)

### Root Cause
Mininet creates virtual network interfaces inside Linux network
namespaces. Each switch exists in its own isolated namespace.
From outside these namespaces the interfaces are not visible
to the regular Linux networking stack.

### Solution
Ran tcpdump from inside the Mininet namespace using the
Mininet CLI switch prefix:
s2 tcpdump -i s2-eth1 -w /path/to/capture.pcap &
The s2 prefix executes the command inside Switch S2 namespace
where the interface exists and is accessible.

---

## Challenge 5 — Cumulative Stats Blocking Congestion Detection

### Problem
Even after fixing the stats reader, Least-Utilized always
chose Path B because Path A had accumulated billions of bytes
from previous sessions — making it always appear more congested
regardless of current traffic load.

### Root Cause
OVS port statistics are cumulative from when the switch was
created. Previous experiment runs kept adding to the total.
Path A always had higher totals than Path B from history.

### Solution
Implemented rate-based measurement — instead of comparing
total bytes, the controller measures the difference in bytes
between two consecutive readings divided by time elapsed.
This gives bytes per second — current traffic rate — which
effectively resets logically with each experiment.

Formula:
rate = (current_bytes - previous_bytes) / time_elapsed

---

## Summary Table

| Challenge | Root Cause | Solution |
|---|---|---|
| Ryu Python 3.10 incompatibility | eventlet and collections changes | Direct ovs-ofctl subprocess calls |
| pingall 100% packet loss | Switches in secure mode | failMode=standalone + install_flows() |
| Stats always returning zero | Port names vs numbers, line wrapping | Regex DOTALL + port number search |
| tcpdump no such device | Mininet network namespaces | Run inside Mininet CLI namespace |
| Cumulative stats blocking detection | OVS stats never reset | Rate-of-change measurement |

---

## Key Lesson

These challenges demonstrate that real networking projects
require systematic debugging and willingness to change
approach when the original plan fails. The final solution
for each challenge was simpler and more reliable than the
original planned approach.
