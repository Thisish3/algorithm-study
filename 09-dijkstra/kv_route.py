"""다익스트라 예제 1: 서버 N대와 링크 M개(양방향, 지연 ms). 서버 S에서 서버 T로 KV 캐시를 보낼 때
지연이 가장 짧은 경로와 그 지연. 링크 지연은 모두 0 이상.

입력: 첫 줄 "N M S T", 다음 M줄 "u v w" (서버 번호 1..N)
출력: 첫 줄 최소 지연 (갈 수 없으면 -1), 둘째 줄 경로 (서버 번호들)
"""
import heapq
import sys

INF = float("inf")


def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int):
    dist = [INF] * (n + 1)
    prev = [0] * (n + 1)
    dist[src] = 0
    heap = [(0, src)]                       # (지금까지 거리, 서버)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                     # 이미 더 짧게 확정된 낡은 항목 → 건너뜀
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:             # 완화(relax)
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def path_to(prev: list[int], src: int, dst: int) -> list[int]:
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    return path[::-1]


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, m, s, t = data[:4]
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v, w = data[4 + 3 * i: 7 + 3 * i]
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist, prev = dijkstra(n, adj, s)
    if dist[t] == INF:
        print(-1)
    else:
        print(dist[t])
        print(*path_to(prev, s, t))
