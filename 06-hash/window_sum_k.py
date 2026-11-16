"""해시 예제 2 (누적합 + 해시): 분 단위 토큰 사용량 배열에서, 합이 정확히 K인 연속 구간의 개수.
구간 [i+1..j]의 합 = prefix[j] - prefix[i]. 그러니 prefix[j] - K가 앞에서 몇 번 나왔는지 세면 된다.
모든 구간을 보면 O(n^2), 해시로 O(n). 음수가 있어도 된다.

입력: 첫 줄 "N K", 둘째 줄 N개의 정수
출력: 구간 개수
"""
import sys
from collections import defaultdict


def count_windows(a: list[int], k: int) -> int:
    seen: dict[int, int] = defaultdict(int)
    seen[0] = 1                          # 빈 앞부분: 처음부터 시작하는 구간을 위해
    prefix = answer = 0
    for x in a:
        prefix += x
        answer += seen[prefix - k]       # 이 앞부분과 짝이 되는 이전 앞부분 수
        seen[prefix] += 1
    return answer


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, k = data[0], data[1]
    print(count_windows(data[2:2 + n], k))
