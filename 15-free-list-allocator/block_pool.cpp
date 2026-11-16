// free list 할당기 예제 2: 같은 크기 블록만 나눠 주는 풀 (vLLM KV 블록, 커널 slab과 같은 발상).
// 빈 블록의 "안쪽 첫 8바이트"에 다음 빈 블록 주소를 적어 둔다(intrusive free list) → 따로 쓰는 메모리 0, 할당·반납 O(1).
// 실행: ./pool  → 정확성 확인(중복 없음, 범위 안, 다 쓰면 nullptr, 반납 뒤 재사용) + new/delete와 시간 비교(한 번 측정)
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <set>
#include <vector>

class BlockPool {
    struct FreeNode { FreeNode* next; };
    std::vector<std::byte> arena_;
    FreeNode* head_ = nullptr;
    size_t block_;

  public:
    BlockPool(size_t block_size, size_t count)
        : arena_(block_size * count), block_(block_size < sizeof(FreeNode) ? sizeof(FreeNode) : block_size) {
        arena_.resize(block_ * count);
        for (size_t i = count; i-- > 0;) {               // 뒤에서부터 꿰어 head가 0번 블록을 가리키게
            auto* n = reinterpret_cast<FreeNode*>(arena_.data() + i * block_);
            n->next = head_;
            head_ = n;
        }
    }
    void* alloc() {
        if (!head_) return nullptr;
        FreeNode* n = head_;
        head_ = n->next;
        return n;
    }
    void free(void* p) {                                  // 반납한 블록이 다음 할당의 첫 후보 (LIFO, 캐시에 따뜻한 블록부터)
        auto* n = static_cast<FreeNode*>(p);
        n->next = head_;
        head_ = n;
    }
    bool owns(void* p) const {
        auto* b = static_cast<const std::byte*>(p);
        return b >= arena_.data() && b < arena_.data() + arena_.size() && (b - arena_.data()) % block_ == 0;
    }
};

int main() {
    const size_t kBlock = 64, kCount = 4096;
    BlockPool pool(kBlock, kCount);
    std::mt19937 rng(0);
    int errors = 0;
    for (int round = 0; round < 50; ++round) {
        std::vector<void*> held;
        std::set<void*> seen;
        while (void* p = pool.alloc()) {
            if (!pool.owns(p) || !seen.insert(p).second) ++errors;
            held.push_back(p);
        }
        if (held.size() != kCount) ++errors;              // 정확히 kCount개를 주고 멈춰야 한다
        std::shuffle(held.begin(), held.end(), rng);
        for (void* p : held) pool.free(p);                // 무작위 순서로 반납해도 다음 라운드에 다 나와야 한다
    }
    std::printf("정확성: 50라운드 × %zu블록, 오류 %d\n", kCount, errors);

    const int kOps = 20000000;
    std::vector<void*> slots(256, nullptr);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < kOps; ++i) {
        auto& s = slots[i & 255];
        if (s) { pool.free(s); s = nullptr; } else s = pool.alloc();
    }
    auto t1 = std::chrono::steady_clock::now();
    for (auto& s : slots) if (s) { pool.free(s); s = nullptr; }
    for (int i = 0; i < kOps; ++i) {
        auto& s = slots[i & 255];
        if (s) { ::operator delete(s); s = nullptr; } else s = ::operator new(kBlock);
    }
    auto t2 = std::chrono::steady_clock::now();
    for (auto& s : slots) if (s) ::operator delete(s);
    auto ns = [&](auto a, auto b) { return std::chrono::duration<double, std::nano>(b - a).count() / kOps; };
    std::printf("연산당: 풀 %.2f ns, new/delete %.2f ns (같은 패턴 %d회, 한 번 측정)\n", ns(t0, t1), ns(t1, t2), kOps);
    return errors ? 1 : 0;
}
