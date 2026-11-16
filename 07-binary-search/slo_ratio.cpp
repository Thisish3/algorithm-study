// X ms 이하 요청 비율. 입력/출력은 slo_ratio.py와 같다.
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    std::vector<int> lat(n);
    for (auto& x : lat) scanf("%d", &x);
    std::sort(lat.begin(), lat.end());
    for (int i = 0; i < q; ++i) {
        int x;
        scanf("%d", &x);
        long long cnt = std::upper_bound(lat.begin(), lat.end(), x) - lat.begin();  // x 이하 개수
        printf("%lld%c", cnt * 100 / n, i + 1 < q ? ' ' : '\n');
    }
}
