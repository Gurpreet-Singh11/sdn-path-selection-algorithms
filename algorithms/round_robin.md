# Round-Robin Algorithm

## Simple Description
Alternates between Path A and Path B for every routing
decision without checking traffic conditions on either path.

## How It Works
- Maintains a simple counter starting at zero
- Even counter value sends traffic to Path A
- Odd counter value sends traffic to Path B
- Counter increases by 1 with every decision
- Never looks at traffic — completely blind

## Real World Analogy
Like a traffic officer who alternates cars left and right
without looking at how busy each road is.

## Code
```python
def round_robin_decision():
    global round_robin_counter
    if round_robin_counter % 2 == 0:
        chosen_path = "A"
    else:
        chosen_path = "B"
    round_robin_counter += 1
    return chosen_path
```

## Experimental Results
- Run 1: 23 path switches
- Run 2: 25 path switches
- Run 3: 25 path switches
- Average: 24.3 path switches
- Stability score: 3.9%
- Overall ranking: 4th — worst performing

## Verdict
Unsuitable for real SDN deployment.
Causes extreme route flapping — switches path almost
every single decision regardless of network conditions.

