// 슬라이딩 윈도우 요청 한도. 입력/출력은 rate_limiter.py와 같다.
#include <cstdio>
#include <deque>
#include <string>

int main() {
    int n;
    long long w, l;
    if (scanf("%d %lld %lld", &n, &w, &l) != 3) return 0;
    std::deque<long long> accepted;
    std::string out;
    for (int i = 0; i < n; ++i) {
        long long t;
        scanf("%lld", &t);
        while (!accepted.empty() && accepted.front() <= t - w) accepted.pop_front();
        if ((long long)accepted.size() < l) {
            accepted.push_back(t);
            out += 'O';
        } else {
            out += 'X';
        }
    }
    printf("%s\n", out.c_str());
}
