#!/usr/bin/env python3
"""
HEXA Stat Node - Optimal Reset Strategy Calculator (MapleStory)

Uses policy iteration on the Markov chain with states (primary_level, total_level)
to find the minimum expected Sol Erda Fragment cost for each target primary stat.

Key insight: V(p,t) = a(p,t) + b(p,t) * X where X = E(0,0) is the expected cost
from scratch. This lets us solve the system as X = a(0,0) / (1 - b(0,0)).

At each state with total >= 10, we choose to RESET (pay mesos, go to (0,0))
or CONTINUE (pay fragments, roll for primary/secondary).
"""


def solve(target, sunny=True):
    """
    Find optimal reset strategy and expected fragment cost via policy iteration.

    Args:
        target: desired minimum primary stat level (6-10)
        sunny: True for Sunny Sunday event (+20% chance at primary lv5+)

    Returns:
        X: expected total Sol Erda Fragment cost
        reset: 2D list, reset[p][t] = True means reset at state (p, t)
        a, b: coefficient arrays where V(p,t) = a[p][t] + b[p][t] * X
        iterations: number of policy iteration rounds
    """
    # Base rates: primary_level -> (selection_chance, fragment_cost)
    base = {
        0: (0.35, 10), 1: (0.35, 10), 2: (0.35, 10),
        3: (0.20, 20), 4: (0.20, 20), 5: (0.20, 20), 6: (0.20, 20),
        7: (0.15, 30), 8: (0.10, 40), 9: (0.05, 50),
        10: (0.00, 50),  # primary maxed; cost assumed same as lv9
    }

    # Apply Sunny Sunday: +20% (multiplicative) to selection chance at lv5+
    data = {}
    for lv, (chance, cost) in base.items():
        if sunny and lv >= 5:
            data[lv] = (min(chance * 1.2, 1.0), cost)
        else:
            data[lv] = (chance, cost)

    MAX_P, MAX_T = 10, 20

    # Initialize policy: never reset
    reset = [[False] * (MAX_T + 1) for _ in range(MAX_P + 1)]

    for iteration in range(200):
        # Compute a[p][t], b[p][t] via backward induction
        a = [[0.0] * (MAX_T + 1) for _ in range(MAX_P + 1)]
        b = [[0.0] * (MAX_T + 1) for _ in range(MAX_P + 1)]

        # Terminal states at t=20
        for p in range(MAX_P + 1):
            a[p][MAX_T] = 0.0
            b[p][MAX_T] = 0.0 if p >= target else 1.0

        # Backward fill t = 19 down to 0
        for t in range(MAX_T - 1, -1, -1):
            for p in range(min(MAX_P, t) + 1):
                if t >= 10 and reset[p][t]:
                    a[p][t] = 0.0
                    b[p][t] = 1.0
                else:
                    prob, cost = data[p]
                    if p < MAX_P:
                        a[p][t] = cost + prob * a[p + 1][t + 1] + (1 - prob) * a[p][t + 1]
                        b[p][t] = prob * b[p + 1][t + 1] + (1 - prob) * b[p][t + 1]
                    else:
                        a[p][t] = cost + a[p][t + 1]
                        b[p][t] = b[p][t + 1]

        # X = E(0,0) = a(0,0) / (1 - b(0,0))
        X = float('inf') if b[0][0] >= 1.0 else a[0][0] / (1 - b[0][0])

        # Policy improvement: for each resettable state, pick better option
        changed = False
        for t in range(10, MAX_T):
            for p in range(min(MAX_P, t) + 1):
                prob, cost = data[p]
                if p < MAX_P:
                    a_c = cost + prob * a[p + 1][t + 1] + (1 - prob) * a[p][t + 1]
                    b_c = prob * b[p + 1][t + 1] + (1 - prob) * b[p][t + 1]
                else:
                    a_c = cost + a[p][t + 1]
                    b_c = b[p][t + 1]

                v_cont = a_c + b_c * X
                v_reset = X

                should_reset = v_reset < v_cont
                if should_reset != reset[p][t]:
                    reset[p][t] = should_reset
                    changed = True

        if not changed:
            break

    return X, reset, a, b, iteration + 1


def main():
    print("=" * 70)
    print("HEXA Stat Node — Optimal Reset Strategy Calculator")
    print("Sunny Sunday Event: +20% enhancement chance at Primary Lv.5+")
    print("=" * 70)

    # Display Sunny Sunday rates
    base_chances = [0.35, 0.35, 0.35, 0.20, 0.20, 0.20, 0.20, 0.15, 0.10, 0.05]
    costs = [10, 10, 10, 20, 20, 20, 20, 30, 40, 50]
    print(f"\n{'Primary Lv':<12}{'Normal %':<12}{'Sunny %':<12}{'Cost':>8}")
    print("-" * 44)
    for i in range(10):
        sunny_c = base_chances[i] * 1.2 if i >= 5 else base_chances[i]
        print(f"{i:<12}{base_chances[i]*100:.1f}%{'':<7}{sunny_c*100:.1f}%{'':<7}{costs[i]:>4}")

    for target in [6, 7, 8, 9, 10]:
        X_sunny, reset_s, a_s, b_s, it_s = solve(target, sunny=True)
        X_normal, reset_n, _, _, _ = solve(target, sunny=False)

        print(f"\n{'=' * 70}")
        print(f"TARGET: Primary Stat ≥ {target}")
        print(f"{'=' * 70}")
        print(f"  Expected cost (Sunny Sunday) : {X_sunny:>10.1f} Sol Erda Fragments")
        print(f"  Expected cost (Normal)       : {X_normal:>10.1f} Sol Erda Fragments")
        savings = (X_normal - X_sunny) / X_normal * 100 if X_normal > 0 else 0
        print(f"  Savings from Sunny Sunday    : {X_normal - X_sunny:>10.1f} fragments ({savings:.1f}%)")

        # Build reset thresholds for both strategies
        def get_thresholds(reset_policy):
            thresholds = {}
            for t in range(10, 20):
                max_reset_p = -1
                for p in range(min(10, t) + 1):
                    if reset_policy[p][t]:
                        max_reset_p = max(max_reset_p, p)
                if max_reset_p >= 0:
                    thresholds[t] = max_reset_p
            return thresholds

        for label, reset_policy in [("Sunny Sunday", reset_s), ("Normal", reset_n)]:
            thresholds = get_thresholds(reset_policy)
            print(f"\n  Optimal Reset Strategy ({label}):")
            if not thresholds:
                print("    Never reset (always continue to level 20)")
                continue

            for t in sorted(thresholds.keys()):
                print(f"    At level {t}, if primary ≤ {thresholds[t]}, then reset")


if __name__ == "__main__":
    main()
