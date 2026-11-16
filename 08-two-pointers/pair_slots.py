"""투 포인터 예제 2 (양 끝에서 좁히기): 요청 N개의 토큰 수와 슬롯 용량 C. 슬롯 하나에는 요청을
최대 2개, 토큰 합 C 이하로 넣는다. 필요한 슬롯 수의 최솟값. (모든 요청은 혼자서는 C 이하)

정렬 후 가장 큰 요청부터 본다. 가장 큰 요청은 어차피 슬롯 하나를 쓴다. 같이 넣을 수 있는 후보 중
가장 작은 요청과 짝지어 보고, 안 되면 혼자 간다. (가장 작은 것과도 안 맞으면 누구와도 안 맞는다.)

입력: 첫 줄 "N C", 둘째 줄 토큰 수 N개
출력: 슬롯 수
"""
import sys


def min_slots(tokens: list[int], cap: int) -> int:
    a = sorted(tokens)
    lo, hi, slots = 0, len(a) - 1, 0
    while lo <= hi:
        if lo < hi and a[lo] + a[hi] <= cap:   # 가장 작은 것과 짝이 되면 같이
            lo += 1
        hi -= 1                                  # 가장 큰 것은 이번 슬롯으로
        slots += 1
    return slots


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, c = data[0], data[1]
    print(min_slots(data[2:2 + n], c))
