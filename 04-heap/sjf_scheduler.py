"""요청 스케줄러: GPU 한 장이 요청을 하나씩 처리한다. 규칙: 쉬고 있을 때 도착해 있는 요청 중
처리 시간이 가장 짧은 것부터 처리한다(SJF). 이 규칙대로 했을 때의 평균 turnaround(도착~완료)를 구한다.

입력: 첫 줄 N, 다음 N줄 "도착시각 처리시간"
출력: 평균 turnaround (소수점 버림)
"""
import heapq
import sys


def average_turnaround(jobs: list[tuple[int, int]]) -> int:
    jobs = sorted(jobs)                 # 도착 시각 순
    ready: list[tuple[int, int]] = []   # (처리시간, 도착시각) 최소 힙
    now = total = i = 0
    while i < len(jobs) or ready:
        while i < len(jobs) and jobs[i][0] <= now:   # 지금까지 도착한 요청을 힙에
            arrive, work = jobs[i]
            heapq.heappush(ready, (work, arrive))
            i += 1
        if not ready:                    # 놀고 있으면 다음 도착 시각으로 건너뜀
            now = jobs[i][0]
            continue
        work, arrive = heapq.heappop(ready)
        now += work
        total += now - arrive
    return total // len(jobs)


if __name__ == "__main__":
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = list(map(int, data[1:1 + 2 * n]))
    print(average_turnaround(list(zip(nums[::2], nums[1::2]))))
