// Power of Two Random Choices (C++ 버전)
// 빌드: c++ -std=c++17 -O2 -o balls balls_into_bins.cpp
// 실행: ./balls [n] [m] [seed]

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

// C의 구조체 + 함수를 클래스 하나로 묶었다.
class XorShift64 {
public:
    explicit XorShift64(uint64_t seed) : state_(seed != 0 ? seed : 0x9E3779B97F4A7C15ULL) {}

    uint64_t next() {
        uint64_t x = state_;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        state_ = x;
        return x;
    }

    uint64_t below(uint64_t n) { return next() % n; }

private:
    uint64_t state_;
};

// vector를 값으로 돌려준다. 복사가 아니라 이동(move)이라 비용이 거의 없다.
std::vector<uint64_t> simulate(uint64_t n, uint64_t m, int d, uint64_t seed) {
    XorShift64 rng(seed);
    std::vector<uint64_t> loads(n, 0);  // malloc/free 대신. 스코프를 벗어나면 알아서 해제된다
    for (uint64_t i = 0; i < m; i++) {
        uint64_t best = rng.below(n);
        for (int k = 1; k < d; k++) {
            uint64_t cand = rng.below(n);
            if (loads[cand] < loads[best]) best = cand;
        }
        loads[best]++;
    }
    return loads;
}

void report(int d, const std::vector<uint64_t>& loads) {
    auto [mn, mx] = std::minmax_element(loads.begin(), loads.end());
    double mean = 0;
    for (auto x : loads) mean += x;
    mean /= loads.size();
    double var = 0;
    for (auto x : loads) var += (x - mean) * (x - mean);
    std::printf("d=%d  max=%llu  min=%llu  std=%.2f\n", d, (unsigned long long)*mx,
                (unsigned long long)*mn, std::sqrt(var / loads.size()));
}

int main(int argc, char** argv) {
    uint64_t n = argc > 1 ? std::stoull(argv[1]) : 1000;
    uint64_t m = argc > 2 ? std::stoull(argv[2]) : 1000000;
    uint64_t seed = argc > 3 ? std::stoull(argv[3]) : 42;
    if (n == 0) {
        std::fprintf(stderr, "n must be > 0\n");
        return 1;
    }

    std::printf("n=%llu m=%llu seed=%llu (평균 %.0f개)\n", (unsigned long long)n,
                (unsigned long long)m, (unsigned long long)seed, (double)m / n);
    for (int d = 1; d <= 2; d++) report(d, simulate(n, m, d, seed));
    return 0;
}
