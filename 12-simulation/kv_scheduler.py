"""구현 예제: KV 블록 할당과 선점이 있는 단순화한 서빙 스케줄러 (vLLM v1의 재계산 선점과 같은 방식).

GPU에 KV 블록 B개, 블록 하나에 토큰 S개. 요청 i는 (도착 스텝, 프롬프트 길이 P, 출력 길이 O).
요청이 쓰는 블록 수 = ceil(지금까지의 토큰 수 / S), 토큰 수 = P + 생성한 토큰 수.

스텝 t마다 순서대로:
 1. 도착: 도착 스텝이 t인 요청을 대기열 뒤에 넣는다(같은 스텝이면 번호 순).
 2. 받기: 대기열 맨 앞 요청이 프롬프트+1토큰에 필요한 블록을 받을 수 있으면 받아 실행 목록 뒤에 넣는다.
    못 받으면 멈춘다(뒤의 요청도 받지 않음, FIFO).
 3. 생성: 실행 목록 순서대로 각 요청이 토큰 1개를 만든다. 새 블록이 필요한데 남은 블록이 없으면,
    실행 목록의 가장 마지막 요청을 선점한다(블록 반납, 생성한 토큰 0으로, 대기열 맨 앞에).
    선점된 것이 자기 자신이면 이번 스텝은 생성하지 않는다. 블록이 생길 때까지 반복.
 4. 완료: 출력 O개를 다 만든 요청은 블록을 반납하고 완료 스텝 t를 기록한다.
받기(2)에서 블록을 미리 잡으므로 받은 직후 스텝의 첫 토큰은 새 블록 없이 들어간다.

입력: 첫 줄 "N B S", 다음 N줄 "도착 P O" (요청 번호 0..N-1)
출력: 요청별 완료 스텝 (공백 구분), 그리고 선점 횟수
"""
import sys
from collections import deque


def blocks_for(tokens: int, s: int) -> int:
    return -(-tokens // s)


def simulate(reqs: list[tuple[int, int, int]], total_blocks: int, s: int):
    n = len(reqs)
    done = [-1] * n
    gen = [0] * n                     # 생성한 토큰 수
    held = [0] * n                    # 가진 블록 수
    free = total_blocks
    waiting: deque[int] = deque()
    running: list[int] = []
    order = sorted(range(n), key=lambda i: (reqs[i][0], i))
    nxt = preemptions = 0
    t = 0
    while sum(d < 0 for d in done):
        while nxt < n and reqs[order[nxt]][0] == t:            # 1. 도착
            waiting.append(order[nxt]); nxt += 1
        while waiting:                                          # 2. 받기
            i = waiting[0]
            need = blocks_for(reqs[i][1] + 1, s)
            if need > free:
                break
            waiting.popleft(); free -= need; held[i] = need; running.append(i)
        for i in list(running):                                 # 3. 생성
            if i not in running:                                # 이번 스텝에 이미 선점됨
                continue
            need = blocks_for(reqs[i][1] + gen[i] + 1, s) - held[i]
            while need > free:
                victim = running.pop()                          # 가장 나중에 받은 요청
                free += held[victim]; held[victim] = 0; gen[victim] = 0
                waiting.appendleft(victim); preemptions += 1
                if victim == i:
                    break
            if i not in running:
                continue
            free -= max(need, 0); held[i] += max(need, 0); gen[i] += 1
        for i in list(running):                                 # 4. 완료
            if gen[i] == reqs[i][2]:
                running.remove(i); free += held[i]; held[i] = 0; done[i] = t
        assert 0 <= free <= total_blocks and free + sum(held) == total_blocks
        t += 1
        if t > 10**6:
            raise RuntimeError("끝나지 않음: 블록이 너무 적다")
    return done, preemptions


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, b, s = data[:3]
    reqs = [tuple(data[3 + 3 * i: 6 + 3 * i]) for i in range(n)]
    done, pre = simulate(reqs, b, s)
    print(*done)
    print(pre)
