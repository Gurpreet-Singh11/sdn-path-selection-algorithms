# Network Topology

## Layout

H1 (10.0.0.1) connects to S1
S1 connects to S2 (Path A) and S3 (Path B)
S2 and S3 both connect to S4
S4 connects to H2 (10.0.0.2)

Path A: H1 -> S1 -> S2 -> S4 -> H2
Path B: H1 -> S1 -> S3 -> S4 -> H2

## Hosts

H1 - IP 10.0.0.1 - MAC 00:00:00:00:00:01 - sends traffic
H2 - IP 10.0.0.2 - MAC 00:00:00:00:00:02 - receives traffic

## Links

H1 to S1 - 100 Mbps - 1ms delay
S1 to S2 - 10 Mbps - 5ms delay - Path A
S1 to S3 - 10 Mbps - 5ms delay - Path B
S2 to S4 - 10 Mbps - 5ms delay - Path A
S3 to S4 - 10 Mbps - 5ms delay - Path B
S4 to H2 - 100 Mbps - 1ms delay

## How to Start

sudo mn -c && sudo python3 topology.py

## How to Test

At mininet prompt type: pingall
Expected: 0% dropped (2/2 received)
