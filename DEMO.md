# Live Demo Guide

## Two Terminals Needed
Terminal 1 = Network
Terminal 2 = Controller

## PREPARATION

sudo mn -c

## STEP 1 — Start Network in Terminal 1

sudo python3 ~/networking_project/topology.py

Wait for mininet> then type:
pingall

Expected: 0% dropped (2/2 received)

## STEP 2 — Start Traffic at mininet> prompt

h2 iperf3 -s &
h1 iperf3 -c 10.0.0.2 -b 9M -t 120 &

Wait 5 seconds.

## ALGORITHM 1 — Round-Robin

Run in Terminal 2:
sed -i 's/ROUTING_MODE = .*/ROUTING_MODE = "round_robin"/' ~/networking_project/controller.py && python3 ~/networking_project/controller.py

Watch for: PATH SWITCH printed every 2 seconds
End result: Total path switches around 24
Say to class: Controller keeps changing its mind — route flapping

## RESTART between algorithms

At mininet> type: exit

In Terminal 1:
sudo mn -c && sudo python3 ~/networking_project/topology.py

At mininet> type:
h2 iperf3 -s &
h1 iperf3 -c 10.0.0.2 -b 9M -t 120 &

## ALGORITHM 2 — Least-Utilized

Run in Terminal 2:
sed -i 's/ROUTING_MODE = .*/ROUTING_MODE = "least_utilized"/' ~/networking_project/controller.py && python3 ~/networking_project/controller.py

Watch for: Almost no PATH SWITCH messages
End result: Total path switches around 1
Say to class: Reads real traffic — chose Path B and stayed stable

## RESTART (repeat same steps as above)

## ALGORITHM 3 — ECMP

Run in Terminal 2:
sed -i 's/ROUTING_MODE = .*/ROUTING_MODE = "ecmp"/' ~/networking_project/controller.py && python3 ~/networking_project/controller.py

Watch for: Zero PATH SWITCH messages
End result: Total path switches = 0
Say to class: Math formula never changes — perfect stability

## RESTART (repeat same steps as above)

## ALGORITHM 4 — Weighted-History

Run in Terminal 2:
sed -i 's/ROUTING_MODE = .*/ROUTING_MODE = "weighted_history"/' ~/networking_project/controller.py && python3 ~/networking_project/controller.py

Watch for: Very few PATH SWITCH messages
End result: Total path switches around 1
Say to class: Averages last 5 readings — smart and stable

## SHOW GRAPHS

eog ~/networking_project/graphs/graph1_path_switches.png &
eog ~/networking_project/graphs/graph2_stability.png &
eog ~/networking_project/graphs/graph3_per_run.png &

Say to class: These graphs prove everything you just watched

## SHOW WIRESHARK

sudo wireshark ~/networking_project/results/path_a_capture.pcap &

Apply filter: ip.src == 10.0.0.1 && tcp
Say to class: 22 million real packets — proof of real traffic

## CLEANUP

exit
sudo mn -c

## Demo Timing

Setup: 2 minutes
Each algorithm: 3 minutes x 4 = 12 minutes
Graphs: 2 minutes
Wireshark: 1 minute
Total: 17 minutes


