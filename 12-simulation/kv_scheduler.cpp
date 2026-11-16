// KV 블록 할당 + 선점 스케줄러. 규칙과 입출력은 kv_scheduler.py와 같다.
#include <algorithm>
#include <cstdio>
#include <deque>
#include <numeric>
#include <tuple>
#include <vector>

static int blocks_for(long long tokens, int s) { return (int)((tokens + s - 1) / s); }

int main() {
    int n, total, s;
    if (scanf("%d %d %d", &n, &total, &s) != 3) return 0;
    std::vector<std::tuple<int, int, int>> r(n);  // (도착, P, O)
    for (auto& [a, p, o] : r) scanf("%d %d %d", &a, &p, &o);
    std::vector<int> order(n), done(n, -1), gen(n, 0), held(n, 0);
    std::iota(order.begin(), order.end(), 0);
    std::stable_sort(order.begin(), order.end(),
                     [&](int x, int y) { return std::get<0>(r[x]) < std::get<0>(r[y]); });
    std::deque<int> waiting;
    std::vector<int> running;
    int free_blocks = total, nxt = 0, remaining = n;
    long long preemptions = 0;
    auto in_running = [&](int i) { return std::find(running.begin(), running.end(), i) != running.end(); };
    for (int t = 0; remaining > 0; ++t) {
        while (nxt < n && std::get<0>(r[order[nxt]]) == t) waiting.push_back(order[nxt++]);
        while (!waiting.empty()) {
            int i = waiting.front();
            int need = blocks_for(std::get<1>(r[i]) + 1, s);
            if (need > free_blocks) break;
            waiting.pop_front();
            free_blocks -= need;
            held[i] = need;
            running.push_back(i);
        }
        std::vector<int> snapshot = running;
        for (int i : snapshot) {
            if (!in_running(i)) continue;
            int need = blocks_for(std::get<1>(r[i]) + gen[i] + 1, s) - held[i];
            while (need > free_blocks) {
                int victim = running.back();
                running.pop_back();
                free_blocks += held[victim];
                held[victim] = 0;
                gen[victim] = 0;
                waiting.push_front(victim);
                ++preemptions;
                if (victim == i) break;
            }
            if (!in_running(i)) continue;
            int add = std::max(need, 0);
            free_blocks -= add;
            held[i] += add;
            ++gen[i];
        }
        snapshot = running;
        for (int i : snapshot) {
            if (gen[i] == std::get<2>(r[i])) {
                running.erase(std::find(running.begin(), running.end(), i));
                free_blocks += held[i];
                held[i] = 0;
                done[i] = t;
                --remaining;
            }
        }
        if (t > 1000000) { printf("끝나지 않음\n"); return 1; }
    }
    for (int i = 0; i < n; ++i) printf("%d%c", done[i], i + 1 < n ? ' ' : '\n');
    printf("%lld\n", preemptions);
}
