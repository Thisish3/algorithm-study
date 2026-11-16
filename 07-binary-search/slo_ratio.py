"""이분 탐색 예제 1 (경계 찾기): 지연 기록 N개와 질의 Q개. 질의마다 "X ms 이하로 끝난 요청이 몇 %인가".
정렬해 두고, X보다 큰 첫 위치(upper bound)를 이분 탐색으로 찾으면 질의당 O(log N).

입력: 첫 줄 "N Q", 둘째 줄 지연 N개, 셋째 줄 질의 X Q개
출력: 질의마다 비율 (소수점 버림 정수 %)
"""
import sys


def upper_bound(a: list[int], x: int) -> int:
    """a[i] > x인 첫 i (없으면 len(a)). a는 오름차순."""
    lo, hi = 0, len(a)              # 답은 [lo, hi] 안에 있다
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1            # mid까지는 x 이하 → 답은 mid 오른쪽
        else:
            hi = mid                # mid가 답일 수도 있다 → 남긴다
    return lo


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, q = data[0], data[1]
    lat = sorted(data[2:2 + n])
    print(*(upper_bound(lat, x) * 100 // n for x in data[2 + n:2 + n + q]))
