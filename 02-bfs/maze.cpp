// BFS로 미로의 최단 거리 구하기 (백준 2178 미로 탐색)
// 빌드: c++ -std=c++17 -O2 -o maze maze.cpp
// 실행: ./maze < maze_input.txt

#include <iostream>
#include <queue>
#include <string>
#include <utility>
#include <vector>

int shortest_path(const std::vector<std::string>& grid) {
    int n = grid.size(), m = grid[0].size();
    std::vector<std::vector<int>> dist(n, std::vector<int>(m, 0));
    std::queue<std::pair<int, int>> q;
    dist[0][0] = 1;
    q.push({0, 0});

    const int dr[] = {1, -1, 0, 0};
    const int dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front();  // C++의 queue는 front()로 보고 pop()으로 뺀다
        q.pop();
        if (r == n - 1 && c == m - 1) return dist[r][c];
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
            if (grid[nr][nc] != '1' || dist[nr][nc] != 0) continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    return -1;
}

int main() {
    std::ios::sync_with_stdio(false);  // 코테에서 입력이 많을 때 cin을 빠르게
    std::cin.tie(nullptr);

    int n, m;
    std::cin >> n >> m;
    std::vector<std::string> grid(n);
    for (auto& row : grid) std::cin >> row;
    std::cout << shortest_path(grid) << '\n';
    return 0;
}
