"""위상 정렬로 줄 세우기 (백준 2252 줄 세우기).

입력: 첫 줄에 N M, 다음 M줄에 A B ("A가 B보다 앞에 서야 한다")
출력: 조건을 만족하는 순서 하나 (답이 여러 개면 아무거나)

실행: python3 line_up.py < line_up_input.txt
"""

import sys
from collections import deque


def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int]:
    graph = [[] for _ in range(n + 1)]  # 번호가 1부터라서 한 칸 더 만든다
    indegree = [0] * (n + 1)  # 나보다 먼저 와야 하는 것의 개수
    for a, b in edges:
        graph[a].append(b)
        indegree[b] += 1

    queue = deque(v for v in range(1, n + 1) if indegree[v] == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for nxt in graph[v]:
            indegree[nxt] -= 1  # v가 줄을 섰으니 nxt의 선행 조건 하나가 풀렸다
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != n:
        raise ValueError("사이클이 있어 순서를 정할 수 없다")
    return order


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0], data[1]
    edges = [(data[2 + 2 * i], data[3 + 2 * i]) for i in range(m)]
    print(*topo_sort(n, edges))


if __name__ == "__main__":
    main()
