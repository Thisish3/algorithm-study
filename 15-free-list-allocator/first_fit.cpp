// first-fit 할당기 (분할 + 병합). 입력/출력은 first_fit.py와 같다.
// 빈 칸을 std::map<시작, 크기>로 들어 주소 순서와 이웃 찾기를 O(log n)에 한다.
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class FirstFit {
    std::map<long long, long long> free_;                          // 시작 -> 크기
    std::unordered_map<std::string, std::pair<long long, long long>> used_;

  public:
    explicit FirstFit(long long n) { if (n > 0) free_[0] = n; }
    long long alloc(const std::string& name, long long size) {
        if (size <= 0 || used_.count(name)) return -1;
        for (auto it = free_.begin(); it != free_.end(); ++it) {
            if (it->second < size) continue;
            long long addr = it->first, rest = it->second - size;
            free_.erase(it);
            if (rest) free_[addr + size] = rest;
            used_[name] = {addr, size};
            return addr;
        }
        return -1;
    }
    void free(const std::string& name) {
        auto u = used_.find(name);
        if (u == used_.end()) return;
        auto [addr, size] = u->second;
        used_.erase(u);
        auto it = free_.emplace(addr, size).first;
        auto next = std::next(it);
        if (next != free_.end() && addr + size == next->first) {
            it->second += next->second;
            free_.erase(next);
        }
        if (it != free_.begin()) {
            auto prev = std::prev(it);
            if (prev->first + prev->second == it->first) {
                prev->second += it->second;
                free_.erase(it);
            }
        }
    }
    std::pair<long long, long long> stats() const {
        long long total = 0, largest = 0;
        for (auto& [s, n] : free_) { total += n; largest = std::max(largest, n); }
        return {total, largest};
    }
};

int main() {
    long long n;
    int q;
    if (!(std::cin >> n >> q)) return 0;
    FirstFit a(n);
    std::vector<long long> out;
    for (int i = 0; i < q; ++i) {
        std::string cmd, name;
        std::cin >> cmd >> name;
        if (cmd == "alloc") { long long s; std::cin >> s; out.push_back(a.alloc(name, s)); }
        else a.free(name);
    }
    for (size_t i = 0; i < out.size(); ++i) std::cout << out[i] << (i + 1 < out.size() ? " " : "");
    std::cout << '\n';
    auto [total, largest] = a.stats();
    std::cout << total << ' ' << largest << '\n';
}
