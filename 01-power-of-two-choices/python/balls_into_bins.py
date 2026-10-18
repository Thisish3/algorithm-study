"""Power of Two Random Choices: 공 m개를 상자 n개에 나눠 담는 시뮬레이션.

d=1: 상자 하나를 무작위로 골라 넣는다.
d=2: 상자 두 개를 무작위로 고르고, 덜 찬 쪽에 넣는다.

실행: python3 balls_into_bins.py [n] [m] [seed]
"""

import math
import sys

MASK64 = (1 << 64) - 1  # 파이썬 정수는 크기 제한이 없어서 64비트로 잘라 줘야 한다


class XorShift64:
    """네 언어가 같은 결과를 내도록 직접 만든 난수 생성기."""

    def __init__(self, seed: int):
        self.state = seed if seed != 0 else 0x9E3779B97F4A7C15  # 0이면 영원히 0만 나온다

    def next(self) -> int:
        x = self.state
        x ^= (x << 13) & MASK64
        x ^= x >> 7
        x ^= (x << 17) & MASK64
        self.state = x
        return x

    def below(self, n: int) -> int:
        """0 이상 n 미만의 정수."""
        return self.next() % n


def simulate(n: int, m: int, d: int, seed: int) -> list[int]:
    rng = XorShift64(seed)
    loads = [0] * n
    for _ in range(m):
        best = rng.below(n)
        for _ in range(d - 1):
            cand = rng.below(n)
            if loads[cand] < loads[best]:
                best = cand
        loads[best] += 1
    return loads


def report(d: int, loads: list[int]) -> None:
    n = len(loads)
    mean = sum(loads) / n
    var = sum((x - mean) ** 2 for x in loads) / n
    print(f"d={d}  max={max(loads)}  min={min(loads)}  std={math.sqrt(var):.2f}")


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 1_000_000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 42
    print(f"n={n} m={m} seed={seed} (평균 {m / n:.0f}개)")
    for d in (1, 2):
        report(d, simulate(n, m, d, seed))


if __name__ == "__main__":
    main()
