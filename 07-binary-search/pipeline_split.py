"""이분 탐색 예제 2 (답을 이분 탐색, parametric search): 모델 레이어 N개의 계산 비용이 순서대로 주어진다.
파이프라인 병렬로 GPU K장에 "연속된 레이어 묶음"으로 나눌 때, 가장 무거운 GPU의 비용을 최소로.

핵심: "가장 무거운 단계를 C 이하로 만들 수 있나?"는 앞에서부터 채우는 욕심으로 O(N)에 답할 수 있고,
C가 커질수록 '가능'이 계속 유지된다(단조). 그래서 C를 이분 탐색한다.

입력: 첫 줄 "N K", 둘째 줄 레이어 비용 N개
출력: 가장 무거운 GPU 비용의 최솟값
"""
import sys


def stages_needed(cost: list[int], cap: int) -> int:
    """각 단계 비용이 cap 이하가 되도록 앞에서부터 채울 때 필요한 GPU 수."""
    stages, load = 1, 0
    for c in cost:
        if load + c > cap:              # 이 레이어부터 다음 GPU
            stages += 1
            load = 0
        load += c
    return stages


def min_max_stage(cost: list[int], k: int) -> int:
    lo, hi = max(cost), sum(cost)       # 답의 범위: 가장 큰 레이어 ~ 전부 한 GPU
    while lo < hi:
        mid = (lo + hi) // 2
        if stages_needed(cost, mid) <= k:
            hi = mid                    # 가능 → 더 작게 시도 (mid는 남긴다)
        else:
            lo = mid + 1                # 불가능 → 더 크게
    return lo


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, k = data[0], data[1]
    print(min_max_stage(data[2:2 + n], k))
