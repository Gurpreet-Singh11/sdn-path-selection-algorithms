# Weighted-History Algorithm

## Simple Description
Instead of reacting to traffic right now, looks at the
average traffic over the last 5 readings before deciding.
Smoother and more stable than Least-Utilized.

## How It Works
- Reads current traffic rate on Path A and Path B
- Stores last 5 readings for each path
- Calculates average of those 5 readings
- Picks path with lower recent average
- Requires sustained trend — not just one spike

## Real World Analogy
Like a wise driver who checks average traffic over
the last 5 minutes before choosing a route — not
just the traffic at this exact second.

## Code
```python
def weighted_history_decision(rate_a, rate_b):
    path_a_history.append(rate_a)
    path_b_history.append(rate_b)
    if len(path_a_history) > HISTORY_SIZE:
        path_a_history.pop(0)
    if len(path_b_history) > HISTORY_SIZE:
        path_b_history.pop(0)
    avg_a = sum(path_a_history) / len(path_a_history)
    avg_b = sum(path_b_history) / len(path_b_history)
    if avg_a <= avg_b:
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
Best overall balance between intelligence and stability.
Recommended algorithm for practical SDN deployment.
More resistant to temporary traffic spikes than
Least-Utilized while still being traffic-aware.
