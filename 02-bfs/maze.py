"""BFS로 미로의 최단 거리 구하기 (백준 2178 미로 탐색).

입력: 첫 줄에 N M, 다음 N줄에 0/1 문자열 (1은 길, 0은 벽)
출력: (1,1)에서 (N,M)까지 지나는 칸 수의 최솟값 (시작, 끝 칸 포함)

실행: python3 maze.py < maze_input.txt
"""

import sys
from collections import deque


def shortest_path(grid: list[str]) -> int:
    n, m = len(grid), len(grid[0])
    dist = [[0] * m for _ in range(n)]  # 0이면 아직 안 간 칸
    dist[0][0] = 1
    queue = deque([(0, 0)])

    while queue:
        r, c = queue.popleft()  # 먼저 넣은 칸부터 꺼낸다. 이게 BFS의 핵심
        if (r, c) == (n - 1, m - 1):
            return dist[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == "1" and dist[nr][nc] == 0:
                dist[nr][nc] = dist[r][c] + 1  # 넣을 때 방문 표시. 꺼낼 때 하면 중복으로 들어간다
                queue.append((nr, nc))
    return -1


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    grid = data[2 : 2 + n]
    assert all(len(row) == m for row in grid)
    print(shortest_path(grid))


if __name__ == "__main__":
    main()
