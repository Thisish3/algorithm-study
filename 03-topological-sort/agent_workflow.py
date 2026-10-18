"""에이전트 워크플로를 DAG로 보고, 실행 순서와 병렬 단계를 구한다.

LangGraph 같은 프레임워크도 노드 의존성을 보고 이 순서로 실행한다.
같은 단계(level)에 있는 노드는 서로 기다릴 필요가 없어 동시에 돌릴 수 있다.

실행: python3 agent_workflow.py
"""

from collections import deque

WORKFLOW = {
    "plan": ["web_search", "retrieve_docs", "query_db"],
    "web_search": ["summarize"],
    "retrieve_docs": ["summarize"],
    "query_db": ["check_policy"],
    "summarize": ["answer"],
    "check_policy": ["answer"],
    "answer": [],
}


def levels(graph: dict[str, list[str]]) -> list[list[str]]:
    """Kahn 알고리즘을 단계 단위로 돌린다. 큐에 있는 것을 한 번에 다 꺼내면 한 단계다."""
    indegree = {v: 0 for v in graph}
    for v in graph:
        for nxt in graph[v]:
            indegree[nxt] += 1

    queue = deque(v for v in graph if indegree[v] == 0)
    result, seen = [], 0
    while queue:
        level = list(queue)
        queue.clear()
        result.append(level)
        seen += len(level)
        for v in level:
            for nxt in graph[v]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

    if seen != len(graph):
        stuck = [v for v in graph if indegree[v] > 0]
        raise ValueError(f"사이클이 있다. 끝내 실행할 수 없는 노드: {stuck}")
    return result


def main() -> None:
    for i, level in enumerate(levels(WORKFLOW), 1):
        print(f"단계 {i}: {', '.join(level)}")

    looping = dict(WORKFLOW, answer=["plan"])  # 답을 보고 다시 계획하는 루프
    try:
        levels(looping)
    except ValueError as e:
        print(f"\n루프를 넣으면: {e}")


if __name__ == "__main__":
    main()
