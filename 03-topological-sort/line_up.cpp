// 위상 정렬로 줄 세우기 (백준 2252 줄 세우기)
// 빌드: c++ -std=c++17 -O2 -o line_up line_up.cpp
// 실행: ./line_up < line_up_input.txt

#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;
    std::cin >> n >> m;
    std::vector<std::vector<int>> graph(n + 1);
    std::vector<int> indegree(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int a, b;
        std::cin >> a >> b;
        graph[a].push_back(b);
        indegree[b]++;
    }

    std::queue<int> q;
    for (int v = 1; v <= n; v++)
        if (indegree[v] == 0) q.push(v);

    std::vector<int> order;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        order.push_back(v);
        for (int nxt : graph[v])
            if (--indegree[nxt] == 0) q.push(nxt);
    }

    if ((int)order.size() != n) {
        std::cerr << "cycle detected\n";
        return 1;
    }
    for (int v : order) std::cout << v << ' ';
    std::cout << '\n';
    return 0;
}
