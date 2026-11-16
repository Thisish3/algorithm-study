// 테넌트별 사용량 집계와 상위 K. 입력/출력은 tenant_usage.py와 같다.
#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    int n, k;
    if (!(std::cin >> n >> k)) return 0;
    std::unordered_map<std::string, std::pair<long long, int>> usage;  // tenant -> (토큰 합, 요청 수)
    for (int i = 0; i < n; ++i) {
        std::string tenant;
        long long tokens;
        std::cin >> tenant >> tokens;
        auto& [total, count] = usage[tenant];   // 없으면 (0, 0)으로 만들어진다
        total += tokens;
        ++count;
    }
    std::vector<std::pair<std::string, std::pair<long long, int>>> ranked(usage.begin(), usage.end());
    std::sort(ranked.begin(), ranked.end(), [](const auto& a, const auto& b) {
        if (a.second.first != b.second.first) return a.second.first > b.second.first;
        return a.first < b.first;
    });
    for (int i = 0; i < k && i < (int)ranked.size(); ++i)
        std::cout << ranked[i].first << ' ' << ranked[i].second.first << ' ' << ranked[i].second.second << '\n';
}
