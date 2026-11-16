"""해시 예제 1 (묶어서 세기): 게이트웨이 로그 "테넌트 토큰수" N줄 → 테넌트별 총 토큰과 요청 수,
총 토큰이 많은 순으로 상위 K개 (같으면 이름순).

입력: 첫 줄 "N K", 다음 N줄 "tenant tokens"
출력: 상위 K개 "tenant total count"
"""
import sys
from collections import defaultdict


def top_tenants(rows: list[tuple[str, int]], k: int) -> list[tuple[str, int, int]]:
    total: dict[str, int] = defaultdict(int)
    count: dict[str, int] = defaultdict(int)
    for tenant, tokens in rows:
        total[tenant] += tokens
        count[tenant] += 1
    ranked = sorted(total, key=lambda t: (-total[t], t))   # 토큰 내림차순, 이름 오름차순
    return [(t, total[t], count[t]) for t in ranked[:k]]


if __name__ == "__main__":
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    rows = [(data[2 + 2 * i], int(data[3 + 2 * i])) for i in range(n)]
    for t, total, cnt in top_tenants(rows, k):
        print(t, total, cnt)
