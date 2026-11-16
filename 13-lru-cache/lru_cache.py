"""LRU 캐시: 용량 C. get(key)는 값(없으면 -1)을 돌려주고 "최근 사용"으로 표시. put(key, value)는 넣거나
갱신하고 최근 사용으로 표시. 꽉 찼는데 새 키가 오면 가장 오래 안 쓴 것을 버린다. 모든 연산 O(1).

해시(키 → 노드)로 바로 찾고, 이중 연결 리스트로 사용 순서를 유지한다. 리스트 머리 쪽이 가장 오래 안 쓴 것,
꼬리 쪽이 가장 최근. 노드를 리스트 중간에서 떼어 꼬리로 옮기는 게 O(1)이라 둘을 함께 쓴다.

입력: 첫 줄 "C Q", 다음 Q줄 "get k" 또는 "put k v"
출력: get 결과를 공백으로, 그리고 적중률(%)
"""
import sys


class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()      # 경계용 빈 노드: 빈 리스트 처리 분기가 사라진다
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node: Node) -> None:          # 꼬리(가장 최근) 앞에 붙이기
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        if len(self.map) == self.cap:              # 가장 오래 안 쓴 것 버리기
            lru = self.head.next
            self._unlink(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self._append(node)


if __name__ == "__main__":
    lines = sys.stdin.read().split("\n")
    cap, q = map(int, lines[0].split())
    cache, out, hits, gets = LRUCache(cap), [], 0, 0
    for line in lines[1:1 + q]:
        parts = line.split()
        if parts[0] == "get":
            v = cache.get(int(parts[1])); out.append(v); gets += 1; hits += v != -1
        else:
            cache.put(int(parts[1]), int(parts[2]))
    print(*out)
    print(hits * 100 // gets if gets else 0)
