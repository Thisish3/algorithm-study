"""DP 예제 2 (편집 거리): GPU와 새 칩에서 같은 프롬프트로 만든 출력 토큰 열 A, B. A를 B로 바꾸는 데 필요한
최소 편집(토큰 하나 넣기·지우기·바꾸기) 횟수. 두 칩의 출력이 얼마나 다른지 숫자로 비교할 때 쓴다.

dp[i][j] = A의 앞 i개를 B의 앞 j개로 바꾸는 최소 횟수.
마지막 토큰이 같으면 dp[i-1][j-1], 다르면 1 + min(지우기 dp[i-1][j], 넣기 dp[i][j-1], 바꾸기 dp[i-1][j-1]).

입력: 첫 줄 A의 토큰들(공백 구분), 둘째 줄 B의 토큰들
출력: 편집 거리
"""
import sys


def edit_distance(a: list[str], b: list[str]) -> int:
    prev = list(range(len(b) + 1))           # dp[0][j] = j (전부 넣기)
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)             # dp[i][0] = i (전부 지우기)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur                            # 한 줄만 들고 간다 (메모리 O(len(b)))
    return prev[-1]


if __name__ == "__main__":
    lines = sys.stdin.read().split("\n")
    print(edit_distance(lines[0].split(), lines[1].split() if len(lines) > 1 else []))
