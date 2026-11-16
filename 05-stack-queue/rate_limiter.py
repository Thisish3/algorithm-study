"""큐 예제: 슬라이딩 윈도우 요청 한도 (게이트웨이의 "최근 W초 동안 최대 L건").
요청 시각을 큐에 넣고, 창(W초) 밖으로 나간 오래된 시각은 앞에서 뺀다.

입력: 첫 줄 "N W L", 다음 줄 요청 시각 N개 (오름차순, 초)
출력: 각 요청의 결과 (O = 통과, X = 거절)
"""
import sys
from collections import deque


def decide(times: list[int], window: int, limit: int) -> str:
    accepted: deque[int] = deque()      # 통과한 요청의 시각
    out = []
    for t in times:
        while accepted and accepted[0] <= t - window:   # 창 밖으로 나간 것 제거
            accepted.popleft()
        if len(accepted) < limit:
            accepted.append(t)
            out.append("O")
        else:
            out.append("X")              # 거절된 요청은 한도에 세지 않는다
    return "".join(out)


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, w, l = data[:3]
    print(decide(data[3:3 + n], w, l))
