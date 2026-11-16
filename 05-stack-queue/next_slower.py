"""스택 예제 (단조 스택): 요청 지연 기록에서, 각 요청 뒤로 처음으로 "더 느린" 요청이 나오기까지 몇 개 뒤인가.
없으면 0. 순진하게 하면 O(n^2), 단조 스택이면 O(n).

입력: 첫 줄 N, 둘째 줄 지연(ms) N개
출력: 각 요청의 거리 N개
"""
import sys


def next_slower(lat: list[int]) -> list[int]:
    ans = [0] * len(lat)
    stack: list[int] = []               # 아직 "더 느린 것"을 못 만난 요청의 인덱스 (지연이 내림차순)
    for i, x in enumerate(lat):
        while stack and lat[stack[-1]] < x:   # x가 그들의 답이다
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans                           # 스택에 남은 것은 답이 없음 → 0


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    print(*next_slower(data[1:1 + data[0]]))
