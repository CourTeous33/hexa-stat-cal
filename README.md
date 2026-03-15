# HEXA Stat Node — Optimal Reset Strategy Calculator

Calculates the minimum expected Sol Erda Fragment cost and optimal reset strategy for leveling HEXA stat nodes in MapleStory.

## How It Works

Uses **policy iteration on a Markov chain** with states `(primary_level, total_level)` to find the optimal reset strategy that minimizes expected Sol Erda Fragment cost.

Each state's expected cost is expressed as `V(p,t) = a + b*X` where `X = E(0,0)` is the expected cost from scratch, solved as `X = a(0,0) / (1 - b(0,0))`.

At each state with total level >= 10, the algorithm decides whether to **reset** (costs only mesos, goes back to level 0) or **continue** (costs fragments, rolls for primary/secondary).

## Usage

```bash
python3 hexa_stat_optimizer.py
```

## Sunny Sunday Event

When Main Stat is Lv. 5+, the enhancement chance is increased by 20% (multiplicative).

| Primary Lv | Normal % | Sunny % | Cost |
|:---:|:---:|:---:|:---:|
| 0 | 35.0% | 35.0% | 10 |
| 1 | 35.0% | 35.0% | 10 |
| 2 | 35.0% | 35.0% | 10 |
| 3 | 20.0% | 20.0% | 20 |
| 4 | 20.0% | 20.0% | 20 |
| 5 | 20.0% | 24.0% | 20 |
| 6 | 20.0% | 24.0% | 20 |
| 7 | 15.0% | 18.0% | 30 |
| 8 | 10.0% | 12.0% | 40 |
| 9 | 5.0% | 6.0% | 50 |

## Results

### Expected Sol Erda Fragment Cost

| Target Primary | Sunny Sunday | Normal | Savings |
|:---:|:---:|:---:|:---:|
| 6 | 671 | 719 | 6.6% |
| 7 | 1,052 | 1,250 | 15.9% |
| 8 | 2,271 | 3,126 | 27.3% |
| 9 | 8,167 | 13,621 | 40.0% |
| 10 | 70,741 | 145,925 | 51.5% |

### Optimal Reset Strategies (Sunny Sunday)

#### Target: Primary Stat >= 6

| Level | Reset if Primary <= |
|:---:|:---:|
| 10 | 1 |
| 11 | 2 |
| 12 | 2 |
| 13 | 2 |
| 14 | 2 |
| 15 | 3 |
| 16 | 3 |
| 17 | 3 |
| 18 | 3 |
| 19 | 4 |

#### Target: Primary Stat >= 7

| Level | Reset if Primary <= |
|:---:|:---:|
| 10 | 2 |
| 11 | 2 |
| 12 | 3 |
| 13 | 3 |
| 14 | 3 |
| 15 | 3 |
| 16 | 3 |
| 17 | 4 |
| 18 | 4 |
| 19 | 5 |

#### Target: Primary Stat >= 8

| Level | Reset if Primary <= |
|:---:|:---:|
| 10 | 3 |
| 11 | 3 |
| 12 | 3 |
| 13 | 3 |
| 14 | 4 |
| 15 | 4 |
| 16 | 4 |
| 17 | 5 |
| 18 | 5 |
| 19 | 6 |

#### Target: Primary Stat >= 9

| Level | Reset if Primary <= |
|:---:|:---:|
| 10 | 3 |
| 11 | 3 |
| 12 | 3 |
| 13 | 4 |
| 14 | 4 |
| 15 | 4 |
| 16 | 5 |
| 17 | 5 |
| 18 | 6 |
| 19 | 7 |

#### Target: Primary Stat >= 10

| Level | Reset if Primary <= |
|:---:|:---:|
| 10 | 3 |
| 11 | 4 |
| 12 | 4 |
| 13 | 4 |
| 14 | 5 |
| 15 | 5 |
| 16 | 6 |
| 17 | 6 |
| 18 | 7 |
| 19 | 8 |
