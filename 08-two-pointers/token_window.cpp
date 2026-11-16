// 예산 안의 가장 긴 연속 요청 구간 (슬라이딩 윈도우). 입력/출력은 token_window.py와 같다.
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
    int n;
    long long budget;
    if (scanf("%d %lld", &n, &budget) != 2) return 0;
    std::vector<long long> t(n);
    for (auto& x : t) scanf("%lld", &x);
    long long total = 0;
    int best = 0, left = 0;
    for (int right = 0; right < n; ++right) {
        total += t[right];
        while (total > budget) total -= t[left++];
        best = std::max(best, right - left + 1);
    }
    printf("%d\n", best);
}
