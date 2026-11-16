// 링 버퍼 (덮어쓰기). 입력/출력은 ring_log.py와 같다.
#include <iostream>
#include <string>
#include <vector>

class RingLog {
    std::vector<long long> buf_;
    size_t head_ = 0, count_ = 0;
    long long total_ = 0;

  public:
    explicit RingLog(size_t cap) : buf_(cap) {}
    void push(long long x) {
        if (buf_.empty()) return;
        if (count_ == buf_.size()) {
            total_ -= buf_[head_];
            buf_[head_] = x;
            head_ = (head_ + 1) % buf_.size();
        } else {
            buf_[(head_ + count_) % buf_.size()] = x;
            ++count_;
        }
        total_ += x;
    }
    long long pop() {
        if (count_ == 0) return -1;
        long long x = buf_[head_];
        head_ = (head_ + 1) % buf_.size();
        --count_;
        total_ -= x;
        return x;
    }
    long long avg() const { return count_ ? total_ / (long long)count_ : -1; }
};

int main() {
    size_t n;
    int q;
    if (!(std::cin >> n >> q)) return 0;
    RingLog r(n);
    std::vector<long long> out;
    for (int i = 0; i < q; ++i) {
        std::string cmd;
        std::cin >> cmd;
        if (cmd == "push") { long long x; std::cin >> x; r.push(x); }
        else if (cmd == "pop") out.push_back(r.pop());
        else out.push_back(r.avg());
    }
    for (size_t i = 0; i < out.size(); ++i) std::cout << out[i] << (i + 1 < out.size() ? " " : "");
    std::cout << '\n';
}
