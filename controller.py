#!/usr/bin/env python3
"""
Project: Comparative Evaluation of Path-Selection Algorithms in SDN
File: controller.py
Description: Implements four path-selection algorithms
    1. Round-Robin
    2. Least-Utilized
    3. ECMP
    4. Weighted-History

How it works:
    - Reads traffic stats from switches using ovs-ofctl
    - Decides which path (A or B) to use for new flows
    - Installs OpenFlow rules to direct traffic
    - Records decisions to a log file for analysis
"""

import subprocess
import time
import json
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION — change this before each test
# ─────────────────────────────────────────────
ROUTING_MODE = "weighted_history"
# Options:
#   "round_robin"
#   "least_utilized"
#   "ecmp"
#   "weighted_history"

# How often to check traffic stats (seconds)
MONITOR_INTERVAL = 2

# How many past readings to average for weighted history
HISTORY_SIZE = 5

# Log file for recording decisions
LOG_FILE = os.path.expanduser("~/networking_project/results/controller_log.csv")

# ─────────────────────────────────────────────
# GLOBAL STATE
# ─────────────────────────────────────────────

# Tracks which path to use next for round-robin
round_robin_counter = 0

# Stores history of traffic readings for weighted history
path_a_history = []
path_b_history = []

# Counts how many times path was switched (for flapping detection)
path_switch_count = 0
current_path = "A"

# ─────────────────────────────────────────────
# STEP 1 — READ TRAFFIC STATS FROM SWITCHES
# ─────────────────────────────────────────────

def get_port_stats(switch_name, port_number):
    """
    Get tx bytes from a switch port using port number.
    Works with OVS output format on this system.
    """
    try:
        import re
        cmd = f"sudo ovs-ofctl dump-ports {switch_name} 2>/dev/null"
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True, timeout=5
        )
        raw = result.stdout
        pattern = f"port\\s+{port_number}:(.*?)(?=port\\s+|$)"
        matches = re.findall(pattern, raw, re.DOTALL)
        if matches:
            section = matches[0]
            if 'tx' in section and 'bytes=' in section:
                tx_part = section.split('tx')[1]
                if 'bytes=' in tx_part:
                    val = tx_part.split('bytes=')[1]
                    val = val.split(',')[0].strip()
                    return int(val)
        return 0
    except Exception as e:
        return 0

# Store previous readings for rate calculation
prev_a = 0
prev_b = 0
prev_time = 0

def get_path_utilization():
    """
    Calculate RATE of traffic on each path (bytes per second)
    Not total bytes — this gives current congestion level
    """
    global prev_a, prev_b, prev_time
    import time

    current_time = time.time()
    current_a = get_port_stats('s2', 1)
    current_b = get_port_stats('s3', 1)

    if prev_time == 0:
        # First reading — no rate yet
        prev_a = current_a
        prev_b = current_b
        prev_time = current_time
        return 0, 0

    # Calculate time difference
    time_diff = current_time - prev_time
    if time_diff == 0:
        return 0, 0

    # Calculate bytes per second
    rate_a = (current_a - prev_a) / time_diff
    rate_b = (current_b - prev_b) / time_diff

    # Store for next calculation
    prev_a = current_a
    prev_b = current_b
    prev_time = current_time

    return rate_a, rate_b

# ─────────────────────────────────────────────
# STEP 2 — THE FOUR DECISION METHODS
# ─────────────────────────────────────────────

def round_robin_decision():
    """
    Method 1 — Round Robin
    Simply alternate between Path A and Path B
    Does NOT check how busy either path is
    Like flipping a coin every time

    In simple language:
    First flow → Path A
    Second flow → Path B
    Third flow → Path A
    And so on...
    """
    global round_robin_counter
    if round_robin_counter % 2 == 0:
        chosen_path = "A"
    else:
        chosen_path = "B"
    round_robin_counter += 1
    return chosen_path

def least_utilized_decision(path_a_bytes, path_b_bytes):
    """
    Method 2 — Least Utilized
    Always pick whichever path has LESS traffic right NOW
    The most reactive method — checks live traffic every time

    In simple language:
    Check which road has fewer cars right now
    Send new traffic down that road
    """
    if path_a_bytes <= path_b_bytes:
        return "A"
    else:
        return "B"

def ecmp_decision(flow_id):
    """
    Method 3 — ECMP (Equal Cost Multi Path)
    Uses a hash formula based on the flow identity
    Does NOT check live traffic at all
    Very stable — never switches paths mid-flow

    In simple language:
    Run a math formula on who is sending
    If result is even → Path A
    If result is odd → Path B
    Always gives same answer for same sender
    """
    hash_value = int(hashlib.md5(str(flow_id).encode()).hexdigest(), 16)
    if hash_value % 2 == 0:
        return "A"
    else:
        return "B"

def weighted_history_decision(path_a_bytes, path_b_bytes):
    """
    Method 4 — Weighted History
    Look at AVERAGE traffic over last few readings
    NOT just the current instant
    More stable than least-utilized — avoids overreacting

    In simple language:
    Instead of checking traffic just right now,
    look at the average over the last 5 seconds
    Then decide which path to use
    """
    global path_a_history, path_b_history

    # Add current readings to history
    path_a_history.append(path_a_bytes)
    path_b_history.append(path_b_bytes)

    # Keep only the last HISTORY_SIZE readings
    if len(path_a_history) > HISTORY_SIZE:
        path_a_history.pop(0)
    if len(path_b_history) > HISTORY_SIZE:
        path_b_history.pop(0)

    # Calculate averages
    avg_a = sum(path_a_history) / len(path_a_history)
    avg_b = sum(path_b_history) / len(path_b_history)

    if avg_a <= avg_b:
        return "A"
    else:
        return "B"

# ─────────────────────────────────────────────
# STEP 3 — INSTALL FLOW RULES ON SWITCHES
# ─────────────────────────────────────────────

def install_path_rule(chosen_path, h1_mac, h2_mac):
    """
    Tell Switch S1 which path to use for new traffic.
    This installs an OpenFlow flow rule on S1.

    Path A → S1 sends traffic out port 2 (towards S2)
    Path B → S1 sends traffic out port 3 (towards S3)

    In simple language:
    Like telling the entry security guard:
    'Send all visitors through Door A' or 'through Door B'
    """
    global current_path, path_switch_count

    if chosen_path == "A":
        port = 2  # S1 port 2 connects to S2 (Path A)
    else:
        port = 3  # S1 port 3 connects to S3 (Path B)

    # Count path switches (flapping detection)
    if chosen_path != current_path:
        path_switch_count += 1
        print(f"  [PATH SWITCH] Path changed from {current_path} to {chosen_path} "
              f"(total switches: {path_switch_count})")
        current_path = chosen_path

    # Install the flow rule on S1
    cmd = (f'ovs-ofctl add-flow s1 '
           f'"priority=200,dl_dst={h2_mac},actions=output:{port}"')
    subprocess.run(cmd, shell=True, capture_output=True)

    print(f"  [RULE] Traffic to H2 → Path {chosen_path} "
          f"(S1 port {port})")

# ─────────────────────────────────────────────
# STEP 4 — LOG RESULTS TO FILE
# ─────────────────────────────────────────────

def log_decision(chosen_path, path_a_bytes, path_b_bytes, method):
    """
    Save each routing decision to a CSV file
    so we can analyse results later
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Write header if file is new
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("timestamp,method,chosen_path,"
                    "path_a_bytes,path_b_bytes,path_switches\n")

    # Write this decision
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%H:%M:%S")
        f.write(f"{timestamp},{method},{chosen_path},"
                f"{path_a_bytes},{path_b_bytes},{path_switch_count}\n")

# ─────────────────────────────────────────────
# STEP 5 — MAIN MONITORING LOOP
# ─────────────────────────────────────────────

def run_controller(h1_mac="00:00:00:00:00:01",
                   h2_mac="00:00:00:00:00:02",
                   flow_id="h1-h2",
                   duration=60):
    """
    Main controller loop.
    Runs for 'duration' seconds, checking traffic every
    MONITOR_INTERVAL seconds and making path decisions.
    """
    print(f"\n{'='*50}")
    print(f"  SDN Path Selection Controller")
    print(f"  Mode: {ROUTING_MODE.upper()}")
    print(f"  Duration: {duration} seconds")
    print(f"  Monitor interval: {MONITOR_INTERVAL} seconds")
    print(f"{'='*50}\n")

    start_time = time.time()
    decision_count = 0

    while time.time() - start_time < duration:
        # Get current traffic stats
        path_a_bytes, path_b_bytes = get_path_utilization()

        # Choose path based on selected method
        if ROUTING_MODE == "round_robin":
            chosen_path = round_robin_decision()

        elif ROUTING_MODE == "least_utilized":
            chosen_path = least_utilized_decision(
                path_a_bytes, path_b_bytes)

        elif ROUTING_MODE == "ecmp":
            chosen_path = ecmp_decision(flow_id)

        elif ROUTING_MODE == "weighted_history":
            chosen_path = weighted_history_decision(
                path_a_bytes, path_b_bytes)

        else:
            print(f"Unknown mode: {ROUTING_MODE}")
            break

        # Install the flow rule
        install_path_rule(chosen_path, h1_mac, h2_mac)

        # Log the decision
        log_decision(chosen_path, path_a_bytes,
                     path_b_bytes, ROUTING_MODE)

        decision_count += 1
        elapsed = time.time() - start_time

        print(f"[{elapsed:.1f}s] Mode={ROUTING_MODE} | "
              f"Path={chosen_path} | "
              f"A={path_a_bytes}B | "
              f"B={path_b_bytes}B | "
              f"Switches={path_switch_count}")

        # Wait before next check
        time.sleep(MONITOR_INTERVAL)

    print(f"\n{'='*50}")
    print(f"  Controller finished")
    print(f"  Total decisions: {decision_count}")
    print(f"  Total path switches: {path_switch_count}")
    print(f"  Log saved to: {LOG_FILE}")
    print(f"{'='*50}\n")

    return path_switch_count

# ─────────────────────────────────────────────
# RUN THE CONTROLLER
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("\nStarting SDN Path Selection Controller")
    print(f"Routing mode: {ROUTING_MODE}")
    print("Press Ctrl+C to stop\n")

    try:
        run_controller(duration=60)
    except KeyboardInterrupt:
        print("\nController stopped by user")
