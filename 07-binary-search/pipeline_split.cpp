// 파이프라인 단계 나누기 (답을 이분 탐색). 입력/출력은 pipeline_split.py와 같다.
#include <algorithm>
#include <cstdio>
#include <numeric>
#include <vector>

static int stages_needed(const std::vector<long long>& cost, long long cap) {
    int stages = 1;
    long long load = 0;
    for (long long c : cost) {
        if (load + c > cap) { ++stages; load = 0; }
        load += c;
    }
    return stages;
}

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    std::vector<long long> cost(n);
    for (auto& c : cost) scanf("%lld", &c);
    long long lo = *std::max_element(cost.begin(), cost.end());
    long long hi = std::accumulate(cost.begin(), cost.end(), 0LL);
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;      // (lo + hi) / 2는 넘칠 수 있다
        if (stages_needed(cost, mid) <= k) hi = mid;
        else lo = mid + 1;
    }
    printf("%lld\n", lo);
}
