// LRU 캐시 (해시 + 이중 연결 리스트). 입력/출력은 lru_cache.py와 같다.
#include <iostream>
#include <list>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

class LRUCache {
    int cap_;
    std::list<std::pair<int, int>> order_;   // 앞 = 가장 최근, 뒤 = 가장 오래 안 씀
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> map_;

  public:
    explicit LRUCache(int cap) : cap_(cap) {}
    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end()) return -1;
        order_.splice(order_.begin(), order_, it->second);   // 노드를 맨 앞으로 O(1), 반복자 유지
        return it->second->second;
    }
    void put(int key, int value) {
        if (cap_ == 0) return;
        auto it = map_.find(key);
        if (it != map_.end()) {
            it->second->second = value;
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        if ((int)map_.size() == cap_) {
            map_.erase(order_.back().first);
            order_.pop_back();
        }
        order_.emplace_front(key, value);
        map_[key] = order_.begin();
    }
};

int main() {
    int cap, q;
    if (!(std::cin >> cap >> q)) return 0;
    LRUCache cache(cap);
    std::vector<int> out;
    int hits = 0;
    for (int i = 0; i < q; ++i) {
        std::string cmd;
        int k, v;
        std::cin >> cmd >> k;
        if (cmd == "get") { int r = cache.get(k); out.push_back(r); hits += r != -1; }
        else { std::cin >> v; cache.put(k, v); }
    }
    for (size_t i = 0; i < out.size(); ++i) std::cout << out[i] << (i + 1 < out.size() ? " " : "");
    std::cout << '\n';
    std::cout << (out.empty() ? 0 : hits * 100 / (int)out.size()) << '\n';
}
