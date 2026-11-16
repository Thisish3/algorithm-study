"""free list 할당기 예제 1: 크기가 제각각인 요청을 first-fit으로 나눠 주는 할당기.
빈 칸 목록을 주소 순으로 들고, 반납되면 양옆 빈 칸과 합친다(coalescing).

명령: "alloc 이름 크기" (주소 출력, 못 주면 -1), "free 이름"
입력: 첫 줄 "N Q" (전체 칸 수, 명령 수), 다음 Q줄 명령
출력: 첫 줄 alloc 결과, 둘째 줄 "남은 칸 합계 / 가장 큰 연속 빈 칸"
"""
import bisect
import sys


class FirstFit:
    def __init__(self, n: int):
        self.starts = [0] if n > 0 else []   # 빈 칸 시작 주소 (정렬 유지)
        self.sizes = [n] if n > 0 else []
        self.used = {}                       # 이름 -> (시작, 크기)

    def alloc(self, name: str, size: int) -> int:
        if size <= 0 or name in self.used:
            return -1
        for i, s in enumerate(self.sizes):
            if s >= size:                    # 처음 맞는 칸 (first-fit)
                addr = self.starts[i]
                if s == size:
                    del self.starts[i], self.sizes[i]
                else:                        # 앞쪽을 떼어 주고 나머지는 빈 칸으로 남긴다 (split)
                    self.starts[i] += size
                    self.sizes[i] -= size
                self.used[name] = (addr, size)
                return addr
        return -1

    def free(self, name: str) -> None:
        if name not in self.used:
            return
        addr, size = self.used.pop(name)
        i = bisect.bisect_left(self.starts, addr)
        self.starts.insert(i, addr)
        self.sizes.insert(i, size)
        if i + 1 < len(self.starts) and addr + size == self.starts[i + 1]:   # 뒤와 합치기
            self.sizes[i] += self.sizes[i + 1]
            del self.starts[i + 1], self.sizes[i + 1]
        if i > 0 and self.starts[i - 1] + self.sizes[i - 1] == addr:          # 앞과 합치기
            self.sizes[i - 1] += self.sizes[i]
            del self.starts[i], self.sizes[i]

    def stats(self) -> tuple[int, int]:
        return sum(self.sizes), max(self.sizes, default=0)


if __name__ == "__main__":
    lines = sys.stdin.read().split("\n")
    n, q = map(int, lines[0].split())
    a, out = FirstFit(n), []
    for line in lines[1:1 + q]:
        p = line.split()
        if p[0] == "alloc":
            out.append(a.alloc(p[1], int(p[2])))
        else:
            a.free(p[1])
    print(*out)
    print(*a.stats())
