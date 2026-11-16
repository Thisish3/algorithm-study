// 두 개씩 슬롯에 담기 (양 끝 투 포인터). 입력/출력은 pair_slots.py와 같다.
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
    int n;
    long long cap;
    if (scanf("%d %lld", &n, &cap) != 2) return 0;
    std::vector<long long> a(n);
    for (auto& x : a) scanf("%lld", &x);
    std::sort(a.begin(), a.end());
    int lo = 0, hi = n - 1, slots = 0;
    while (lo <= hi) {
        if (lo < hi && a[lo] + a[hi] <= cap) ++lo;
        --hi;
        ++slots;
    }
    printf("%d\n", slots);
}
