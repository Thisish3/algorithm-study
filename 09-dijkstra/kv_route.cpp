// 다익스트라: 최소 지연 경로. 입력/출력은 kv_route.py와 같다.
#include <algorithm>
#include <climits>
#include <cstdio>
#include <functional>
#include <queue>
#include <utility>
#include <vector>

int main() {
    int n, m, s, t;
    if (scanf("%d %d %d %d", &n, &m, &s, &t) != 4) return 0;
    std::vector<std::vector<std::pair<int, long long>>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v;
        long long w;
        scanf("%d %d %lld", &u, &v, &w);
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    const long long INF = LLONG_MAX;
    std::vector<long long> dist(n + 1, INF);
    std::vector<int> prev(n + 1, 0);
    using Item = std::pair<long long, int>;               // (거리, 서버)
    std::priority_queue<Item, std::vector<Item>, std::greater<>> heap;
    dist[s] = 0;
    heap.push({0, s});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                prev[v] = u;
                heap.push({dist[v], v});
            }
        }
    }
    if (dist[t] == INF) { printf("-1\n"); return 0; }
    std::vector<int> path{t};
    while (path.back() != s) path.push_back(prev[path.back()]);
    std::reverse(path.begin(), path.end());
    printf("%lld\n", dist[t]);
    for (size_t i = 0; i < path.size(); ++i) printf("%d%c", path[i], i + 1 < path.size() ? ' ' : '\n');
}
