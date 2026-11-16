"""유니온 파인드 예제 2 (크루스칼 최소 신장 트리): 서버 N대를 모두 이으려 한다. 깔 수 있는 링크 후보 M개와
비용이 주어질 때, 모든 서버가 이어지는 가장 싼 링크 집합의 비용. 싼 링크부터 보면서, 이미 이어진 두 서버를
잇는 링크(고리를 만드는 링크)는 건너뛴다. "이미 이어졌나?"를 유니온 파인드로 답한다.

입력: 첫 줄 "N M", 다음 M줄 "u v cost"
출력: 최소 비용 (모두 이을 수 없으면 -1)
"""
import sys
from chip_groups import DSU


def mst_cost(n: int, edges: list[tuple[int, int, int]]) -> int:
    dsu, total, used = DSU(n), 0, 0
    for cost, u, v in sorted((c, u, v) for u, v, c in edges):
        if dsu.union(u, v):          # 다른 묶음일 때만 깐다
            total += cost
            used += 1
    return total if used == n - 1 else -1


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0], data[1]
    print(mst_cost(n, [tuple(data[2 + 3 * i: 5 + 3 * i]) for i in range(m)]))
