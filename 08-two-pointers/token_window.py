"""투 포인터 예제 1 (슬라이딩 윈도우, 길이가 변함): 들어온 순서대로의 요청 토큰 수 N개.
한 스텝의 토큰 예산 B 안에 넣을 수 있는 "연속된 요청"의 최대 개수.
토큰 수가 모두 0 이상이라, 오른쪽을 늘리면 합이 늘고 왼쪽을 줄이면 합이 준다 → 두 포인터가 각각 한 방향으로만 움직인다.

입력: 첫 줄 "N B", 둘째 줄 토큰 수 N개 (0 이상)
출력: 최대 개수
"""
import sys


def longest_within(tokens: list[int], budget: int) -> int:
    best = left = total = 0
    for right, t in enumerate(tokens):
        total += t                          # 오른쪽으로 한 칸 넓히기
        while total > budget:               # 예산을 넘으면 왼쪽을 줄인다
            total -= tokens[left]
            left += 1
        best = max(best, right - left + 1)  # [left, right]는 예산 안
    return best


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, b = data[0], data[1]
    print(longest_within(data[2:2 + n], b))
