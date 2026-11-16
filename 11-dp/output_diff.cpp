// 편집 거리 (토큰 단위). 입력/출력은 output_diff.py와 같다.
#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static std::vector<std::string> tokens(const std::string& line) {
    std::istringstream in(line);
    std::vector<std::string> out;
    for (std::string t; in >> t;) out.push_back(t);
    return out;
}

int main() {
    std::string la, lb;
    std::getline(std::cin, la);
    std::getline(std::cin, lb);
    auto a = tokens(la), b = tokens(lb);
    std::vector<int> prev(b.size() + 1), cur(b.size() + 1);
    for (size_t j = 0; j <= b.size(); ++j) prev[j] = (int)j;
    for (size_t i = 1; i <= a.size(); ++i) {
        cur[0] = (int)i;
        for (size_t j = 1; j <= b.size(); ++j)
            cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1]
                                          : 1 + std::min({prev[j], cur[j - 1], prev[j - 1]});
        std::swap(prev, cur);
    }
    std::cout << prev[b.size()] << '\n';
}
