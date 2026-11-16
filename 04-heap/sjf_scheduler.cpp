// 요청 스케줄러 (SJF). 입력/출력은 sjf_scheduler.py와 같다.
#include <algorithm>
#include <cstdio>
#include <functional>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<pair<long long, long long>> jobs(n);  // (도착, 처리시간)
    for (auto& [a, w] : jobs) scanf("%lld %lld", &a, &w);
    sort(jobs.begin(), jobs.end());

    // (처리시간, 도착) 최소 힙: priority_queue는 기본이 최대 힙이라 greater를 준다
    priority_queue<pair<long long, long long>, vector<pair<long long, long long>>,
                   greater<>> ready;
    long long now = 0, total = 0;
    size_t i = 0;
    while (i < jobs.size() || !ready.empty()) {
        while (i < jobs.size() && jobs[i].first <= now) {
            ready.push({jobs[i].second, jobs[i].first});
            ++i;
        }
        if (ready.empty()) {
            now = jobs[i].first;
            continue;
        }
        auto [work, arrive] = ready.top();
        ready.pop();
        now += work;
        total += now - arrive;
    }
    printf("%lld\n", total / n);
}
