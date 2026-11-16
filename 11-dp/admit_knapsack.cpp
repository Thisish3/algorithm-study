// 0/1 배낭: KV 블록 예산 안에서 요청 점수 합 최대. 입력/출력은 admit_knapsack.py와 같다.
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
    int n, budget;
    if (scanf("%d %d", &n, &budget) != 2) return 0;
    std::vector<long long> dp(budget + 1, 0);
    for (int i = 0; i < n; ++i) {
        int blocks;
        long long score;
        scanf("%d %lld", &blocks, &score);
        for (int b = budget; b >= blocks; --b) dp[b] = std::max(dp[b], dp[b - blocks] + score);
    }
    printf("%lld\n", dp[budget]);
}
