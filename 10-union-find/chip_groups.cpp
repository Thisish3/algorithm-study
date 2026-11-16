// 유니온 파인드: 칩 묶음 질의. 입력/출력은 chip_groups.py와 같다.
#include <iostream>
#include <numeric>
#include <string>
#include <utility>
#include <vector>

struct DSU {
    std::vector<int> parent, size;
    explicit DSU(int n) : parent(n + 1), size(n + 1, 1) { std::iota(parent.begin(), parent.end(), 0); }
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];   // 경로 절반 압축 (반복문 버전)
            x = parent[x];
        }
        return x;
    }
    bool unite(int a, int b) {
        a = find(a), b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) std::swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};

int main() {
    std::ios::sync_with_stdio(false);
    int n, q;
    if (!(std::cin >> n >> q)) return 0;
    DSU dsu(n);
    for (int i = 0; i < q; ++i) {
        std::string cmd;
        int a, b;
        std::cin >> cmd >> a;
        if (cmd == "link") { std::cin >> b; dsu.unite(a, b); }
        else if (cmd == "same") { std::cin >> b; std::cout << (dsu.find(a) == dsu.find(b) ? "YES" : "NO") << '\n'; }
        else std::cout << dsu.size[dsu.find(a)] << '\n';
    }
}
