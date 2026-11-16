"""다익스트라 예제 2 (여러 출발점): 서버 N대 중 몇 대에 모델 복제본이 있다. 각 서버(클라이언트 쪽)에서
가장 가까운 복제본까지의 지연. 복제본마다 따로 다익스트라를 돌리지 않고, 복제본 전부를 거리 0으로
힙에 함께 넣고 한 번만 돌린다(가상의 출발점 하나에서 모든 복제본으로 0짜리 링크가 있는 것과 같다).

입력: 첫 줄 "N M R", 둘째 줄 복제본 서버 R개, 다음 M줄 "u v w"
출력: 서버 1..N의 가장 가까운 복제본까지 지연 (갈 수 없으면 -1)
"""
import heapq
import sys


def nearest(n: int, adj, sources: list[int]) -> list[float]:
    dist = [float("inf")] * (n + 1)
    heap = []
    for s in sources:
        dist[s] = 0
        heap.append((0, s))
    heapq.heapify(heap)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, m, r = data[:3]
    reps = data[3:3 + r]
    adj = [[] for _ in range(n + 1)]
    base = 3 + r
    for i in range(m):
        u, v, w = data[base + 3 * i: base + 3 * i + 3]
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = nearest(n, adj, reps)
    print(*(d if d != float("inf") else -1 for d in dist[1:]))
