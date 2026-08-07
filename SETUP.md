# Environment Setup Guide

## System Requirements
- Operating System: Ubuntu 22.04 LTS
- Platform: VMware Workstation on Windows
- Python: 3.10
- RAM: 4GB minimum recommended 8GB
- Disk Space: 20GB minimum

## Installation Steps

### Step 1 — Update Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2 — Install Mininet
```bash
sudo apt install mininet -y
```

Verify:
```bash
sudo mn --version
```
Expected: 2.3.0

### Step 3 — Install iperf3
```bash
sudo apt install iperf3 -y
```

Verify:
```bash
iperf3 --version
```
Expected: iperf 3.9

### Step 4 — Install Wireshark
```bash
sudo apt install wireshark -y
```

When asked "Should non-superusers be able to capture packets?" select Yes.

Verify:
```bash
wireshark --version
```

### Step 5 — Install net-tools
```bash
sudo apt install net-tools -y
```

### Step 6 — Install Python libraries
```bash
pip3 install matplotlib numpy
```

Verify:
```bash
python3 -c "import matplotlib; print('matplotlib OK')"
python3 -c "import numpy; print('numpy OK')"
```

### Step 7 — Install git
```bash
sudo apt install git -y
```

### Step 8 — Verify Open vSwitch
```bash
sudo ovs-vsctl show
```

Expected: shows OVS version installed

## Why We Did Not Use Ryu or POX

### Ryu Controller — Abandoned
Ryu was our original planned controller framework.
After installation, running ryu-manager failed with:
- eventlet.wsgi ALREADY_HANDLED import error
- collections.MutableMapping removed in Python 3.10
- TypeError on immutable TimeoutError type

Root cause: Ryu last updated 2020, designed for Python 3.6-3.8.
Ubuntu 22.04 ships with Python 3.10 which broke multiple dependencies.

### POX Controller — Abandoned
POX was evaluated as alternative to Ryu.
Issue: DNS parsing errors when connected to multi-switch topology.
Result: pingall showed 100% packet loss.

### Final Solution — Direct OVS Control
We used direct OpenFlow switch management via ovs-ofctl commands
called from Python subprocess. This approach:
- Has zero compatibility issues
- Works natively with Open vSwitch
- Is how production SDN systems interact with OVS
- Gives full control over flow rules without framework overhead

## Quick Verification — All Tools Working

Run this to verify everything is installed:
```bash
sudo mn --version
iperf3 --version
python3 --version
wireshark --version
sudo ovs-vsctl show
python3 -c "import matplotlib, numpy; print('Python libs OK')"
```

All commands should return version numbers without errors.
