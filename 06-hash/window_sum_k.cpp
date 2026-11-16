// 합이 K인 연속 구간 개수 (누적합 + 해시). 입력/출력은 window_sum_k.py와 같다.
#include <cstdio>
#include <unordered_map>

int main() {
    int n;
    long long k;
    if (scanf("%d %lld", &n, &k) != 2) return 0;
    std::unordered_map<long long, long long> seen;
    seen.reserve(n * 2 + 1);
    seen[0] = 1;
    long long prefix = 0, answer = 0;
    for (int i = 0; i < n; ++i) {
        long long x;
        scanf("%lld", &x);
        prefix += x;
        auto it = seen.find(prefix - k);       // seen[prefix - k]로 읽으면 없는 키가 생긴다
        if (it != seen.end()) answer += it->second;
        ++seen[prefix];
    }
    printf("%lld\n", answer);
}
