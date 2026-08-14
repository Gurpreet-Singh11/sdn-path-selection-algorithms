# ECMP — Equal-Cost Multi-Path Algorithm

## Full Name
ECMP stands for Equal-Cost Multi-Path

## Simple Description
Uses a mathematical hash formula based on the flow
identity to assign traffic to a path permanently.
Never checks live traffic at all.

## How It Works
- Takes flow identifier as input (example: h1-h2)
- Runs MD5 hash function on the flow identifier
- If hash result is even — send to Path A
- If hash result is odd — send to Path B
- Same flow always gets same path — never changes

## Real World Analogy
Like assigning cars to roads based on license plate
number. Even plates go left, odd plates go right.
Never changes regardless of traffic conditions.

## Code
```python
def ecmp_decision(flow_id):
    hash_value = int(
        hashlib.md5(str(flow_id).encode()).hexdigest(),
        16)
    if hash_value % 2 == 0:
        return "A"
    else:
        return "B"
```

## Experimental Results
- Run 1: 0 path switches
- Run 2: 0 path switches
- Run 3: 0 path switches
- Average: 0.0 path switches
- Stability score: 100.0%
- Overall ranking: 1st — most stable

## Verdict
Perfect stability — zero route flapping guaranteed.
Most widely used in real Internet routers today.
Weakness: completely ignores real-time congestion.
