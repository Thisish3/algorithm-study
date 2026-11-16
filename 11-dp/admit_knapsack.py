"""DP 예제 1 (0/1 배낭): 대기 요청 N개마다 필요한 KV 블록 수와 우선순위 점수가 있다. KV 블록 B개 안에서
받아들일 요청을 골라 점수 합을 최대로. 각 요청은 받거나 말거나(나눌 수 없음).

dp[b] = 블록 b개까지 썼을 때의 최대 점수. 요청 하나씩 보며, 그 요청을 넣는 경우와 안 넣는 경우 중 큰 것.
같은 요청을 두 번 넣지 않으려고 b를 큰 쪽에서 작은 쪽으로 돈다.

입력: 첫 줄 "N B", 다음 N줄 "blocks score"
출력: 최대 점수
"""
import sys


def best_score(items: list[tuple[int, int]], budget: int) -> int:
    dp = [0] * (budget + 1)
    for blocks, score in items:
        for b in range(budget, blocks - 1, -1):   # 거꾸로: 이번 요청은 한 번만
            dp[b] = max(dp[b], dp[b - blocks] + score)
    return dp[budget]


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, b = data[0], data[1]
    print(best_score([(data[2 + 2 * i], data[3 + 2 * i]) for i in range(n)], b))
