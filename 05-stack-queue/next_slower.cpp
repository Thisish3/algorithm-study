// 단조 스택: 처음으로 더 느린 요청까지의 거리. 입력/출력은 next_slower.py와 같다.
#include <cstdio>
#include <vector>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    std::vector<int> lat(n), ans(n, 0), stack;
    for (auto& x : lat) scanf("%d", &x);
    for (int i = 0; i < n; ++i) {
        while (!stack.empty() && lat[stack.back()] < lat[i]) {
            ans[stack.back()] = i - stack.back();
            stack.pop_back();
        }
        stack.push_back(i);
    }
    for (int i = 0; i < n; ++i) printf("%d%c", ans[i], i + 1 < n ? ' ' : '\n');
}
