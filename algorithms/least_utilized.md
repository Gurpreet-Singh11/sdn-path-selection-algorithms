# Least-Utilized Algorithm

## Simple Description
Always checks which path is less busy right now and
sends new traffic to that path instantly.

## How It Works
- Reads bytes per second on Path A (Switch S2)
- Reads bytes per second on Path B (Switch S3)
- Compares both rates
- Sends traffic to whichever path has lower rate now
- Checks every 2 seconds

## Real World Analogy
Like a GPS that checks live traffic before every
decision and always picks the less congested road.

## Code
```python
def least_utilized_decision(rate_a, rate_b):
    if rate_a <= rate_b:
        return "A"
    else:
        return "B"
```

## Experimental Results
- Run 1: 1 path switch
- Run 2: 1 path switch
- Run 3: 1 path switch
- Average: 1.0 path switches
- Stability score: 96.1%
- Overall ranking: 2nd

## Verdict
Excellent performance under consistent traffic conditions.
Near-perfect stability with real traffic awareness.
Risk of flapping if both paths have equal load.
