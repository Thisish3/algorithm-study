"""링 버퍼 예제 1: 최근 지연 기록 N개만 보관하는 버퍼. 배열 하나와 머리(head) 위치, 개수(count)로 원형으로 쓴다.
꽉 찼을 때 새 값이 오면 가장 오래된 값을 덮어쓴다(로그·지표 버퍼의 보통 동작).

명령: "push x" (기록), "pop" (가장 오래된 것 꺼내기, 비었으면 -1), "avg" (지금 들어 있는 값의 평균, 버림, 비었으면 -1)
입력: 첫 줄 "N Q", 다음 Q줄 명령
출력: pop / avg 결과를 공백으로
"""
import sys


class RingLog:
    def __init__(self, capacity: int):
        self.buf = [0] * capacity
        self.cap = capacity
        self.head = 0          # 가장 오래된 값의 위치
        self.count = 0         # 들어 있는 개수 (꽉 참과 빔을 구분하려고 따로 센다)
        self.total = 0         # 평균을 O(1)에 주려고 합을 들고 다닌다

    def push(self, x: int) -> None:
        if self.cap == 0:
            return
        if self.count == self.cap:                 # 꽉 참: 가장 오래된 것을 덮어쓴다
            self.total -= self.buf[self.head]
            self.buf[self.head] = x
            self.head = (self.head + 1) % self.cap
        else:
            self.buf[(self.head + self.count) % self.cap] = x
            self.count += 1
        self.total += x

    def pop(self) -> int:
        if self.count == 0:
            return -1
        x = self.buf[self.head]
        self.head = (self.head + 1) % self.cap
        self.count -= 1
        self.total -= x
        return x

    def avg(self) -> int:
        return self.total // self.count if self.count else -1


if __name__ == "__main__":
    lines = sys.stdin.read().split("\n")
    n, q = map(int, lines[0].split())
    r, out = RingLog(n), []
    for line in lines[1:1 + q]:
        p = line.split()
        if p[0] == "push":
            r.push(int(p[1]))
        elif p[0] == "pop":
            out.append(r.pop())
        else:
            out.append(r.avg())
    print(*out)
