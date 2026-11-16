// 링 버퍼 예제 2: 생산자 1개 · 소비자 1개(SPSC) 잠금 없는 링 버퍼.
// 생산자는 tail만, 소비자는 head만 쓴다. 상대가 쓴 값은 acquire로 읽고, 자기 값은 release로 쓴다.
// 용량을 2의 거듭제곱으로 두면 % 대신 & (cap - 1)로 위치를 구한다.
// 실행: ./spsc [개수]  → 생산자가 1..개수를 넣고, 소비자가 순서대로 다 받았는지 확인한다.
#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <thread>
#include <vector>

template <typename T>
class SpscRing {
    std::vector<T> buf_;
    const size_t mask_;
    alignas(64) std::atomic<size_t> head_{0};   // 소비자가 다음에 읽을 위치 (계속 증가, 감싸지 않음)
    alignas(64) std::atomic<size_t> tail_{0};   // 생산자가 다음에 쓸 위치

  public:
    explicit SpscRing(size_t cap_pow2) : buf_(cap_pow2), mask_(cap_pow2 - 1) {}
    bool push(const T& x) {                      // 생산자만 부른다
        size_t t = tail_.load(std::memory_order_relaxed);
        if (t - head_.load(std::memory_order_acquire) == buf_.size()) return false;   // 꽉 참
        buf_[t & mask_] = x;
        tail_.store(t + 1, std::memory_order_release);   // 값을 쓴 "뒤에" 위치를 공개
        return true;
    }
    bool pop(T& out) {                           // 소비자만 부른다
        size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return false;                // 비었음
        out = buf_[h & mask_];
        head_.store(h + 1, std::memory_order_release);   // 다 읽은 "뒤에" 자리를 돌려줌
        return true;
    }
};

int main(int argc, char** argv) {
    const long long n = argc > 1 ? std::atoll(argv[1]) : 5000000;
    SpscRing<long long> ring(1024);
    long long errors = 0, received = 0, full_spins = 0;
    std::thread producer([&] {
        for (long long i = 1; i <= n; ++i)
            while (!ring.push(i)) ++full_spins;
    });
    std::thread consumer([&] {
        long long expect = 1, x;
        while (expect <= n) {
            if (ring.pop(x)) {
                if (x != expect) ++errors;
                ++expect;
                ++received;
            }
        }
    });
    producer.join();
    consumer.join();
    std::printf("받은 개수 %lld / %lld, 순서 오류 %lld, 꽉 차서 기다린 횟수 %lld\n", received, n, errors, full_spins);
    return errors ? 1 : 0;
}
