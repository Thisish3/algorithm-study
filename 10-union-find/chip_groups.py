"""유니온 파인드 예제 1: 칩 N장에 연결(링크)이 하나씩 추가된다. 명령마다
  "link a b"  → a와 b를 연결
  "same a b"  → a와 b가 (몇 단계를 거쳐서라도) 이어져 있나? YES/NO
  "size a"    → a가 속한 묶음의 칩 수
묶음이 합쳐지기만 하고 끊기지는 않을 때, 명령 하나를 거의 O(1)에 처리한다.

입력: 첫 줄 "N Q", 다음 Q줄 명령
출력: same / size 결과를 한 줄씩
"""
import sys


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))   # 처음엔 모두 자기 자신이 대표
        self.size = [1] * (n + 1)

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:      # 경로 압축: 지나온 칩을 대표에 바로 연결
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False                   # 이미 같은 묶음
        if self.size[a] < self.size[b]:    # 작은 묶음을 큰 묶음 밑에 (트리가 낮게 유지됨)
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


if __name__ == "__main__":
    lines = sys.stdin.read().split("\n")
    n, q = map(int, lines[0].split())
    dsu, out = DSU(n), []
    for line in lines[1:1 + q]:
        cmd, *args = line.split()
        if cmd == "link":
            dsu.union(int(args[0]), int(args[1]))
        elif cmd == "same":
            out.append("YES" if dsu.find(int(args[0])) == dsu.find(int(args[1])) else "NO")
        else:
            out.append(str(dsu.size[dsu.find(int(args[0]))]))
    print("\n".join(out))
