// Power of Two Random Choices (C 버전)
// 빌드: cc -O2 -o balls balls_into_bins.c -lm
// 실행: ./balls [n] [m] [seed]

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// 난수 상태는 구조체 하나로 들고 다닌다. C에는 클래스가 없다.
typedef struct {
    uint64_t state;
} XorShift64;

static uint64_t xs_next(XorShift64 *rng) {
    uint64_t x = rng->state;
    x ^= x << 13;  // uint64_t는 넘치는 비트가 자동으로 버려진다
    x ^= x >> 7;
    x ^= x << 17;
    rng->state = x;
    return x;
}

static uint64_t xs_below(XorShift64 *rng, uint64_t n) {
    return xs_next(rng) % n;
}

// loads 배열은 호출한 쪽이 만들어서 넘긴다. 메모리 주인이 누구인지 분명히 하기 위해서다.
static void simulate(uint64_t *loads, uint64_t n, uint64_t m, int d, uint64_t seed) {
    XorShift64 rng = {seed != 0 ? seed : 0x9E3779B97F4A7C15ULL};
    for (uint64_t i = 0; i < n; i++) loads[i] = 0;

    for (uint64_t i = 0; i < m; i++) {
        uint64_t best = xs_below(&rng, n);
        for (int k = 1; k < d; k++) {
            uint64_t cand = xs_below(&rng, n);
            if (loads[cand] < loads[best]) best = cand;
        }
        loads[best]++;
    }
}

static void report(int d, const uint64_t *loads, uint64_t n) {
    uint64_t max = loads[0], min = loads[0], sum = 0;
    for (uint64_t i = 0; i < n; i++) {
        if (loads[i] > max) max = loads[i];
        if (loads[i] < min) min = loads[i];
        sum += loads[i];
    }
    double mean = (double)sum / n, var = 0;
    for (uint64_t i = 0; i < n; i++) {
        double diff = loads[i] - mean;
        var += diff * diff;
    }
    printf("d=%d  max=%llu  min=%llu  std=%.2f\n", d, (unsigned long long)max,
           (unsigned long long)min, sqrt(var / n));
}

int main(int argc, char **argv) {
    uint64_t n = argc > 1 ? strtoull(argv[1], NULL, 10) : 1000;
    uint64_t m = argc > 2 ? strtoull(argv[2], NULL, 10) : 1000000;
    uint64_t seed = argc > 3 ? strtoull(argv[3], NULL, 10) : 42;
    if (n == 0) {
        fprintf(stderr, "n must be > 0\n");
        return 1;
    }

    uint64_t *loads = malloc(n * sizeof *loads);  // 힙에 n칸 빌리기
    if (loads == NULL) {
        perror("malloc");
        return 1;
    }

    printf("n=%llu m=%llu seed=%llu (평균 %.0f개)\n", (unsigned long long)n,
           (unsigned long long)m, (unsigned long long)seed, (double)m / n);
    for (int d = 1; d <= 2; d++) {
        simulate(loads, n, m, d, seed);
        report(d, loads, n);
    }

    free(loads);  // 빌린 메모리는 직접 돌려줘야 한다
    return 0;
}
