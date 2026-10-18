# Power of Two Random Choices

공 m개를 상자 n개에 담는다. 공마다 상자 d개를 무작위로 골라 가장 덜 찬 곳에 넣는다.
AWS S3가 디스크에 데이터를 나눌 때 쓰는 방식으로 알려져 있고, 서빙 라우터의 least-loaded-of-two도 같은 아이디어다.

네 언어가 같은 난수 생성기(xorshift64)를 써서, 같은 seed면 결과가 똑같이 나온다.

## 실행

```bash
python3 python/balls_into_bins.py 1000 1000000 42
cc -O2 -o c/balls c/balls_into_bins.c -lm && c/balls 1000 1000000 42
c++ -std=c++17 -O2 -o cpp/balls cpp/balls_into_bins.cpp && cpp/balls 1000 1000000 42
cd rust && cargo run --release -- 1000 1000000 42
```

## 결과 (Apple M2, n=1000, m=1,000,000, seed=42)

| d | max | min | std |
|---|---|---|---|
| 1 | 1095 | 905 | 31.39 |
| 2 | 1002 | 996 | 0.94 |

상자 하나를 더 보는 것만으로 표준편차가 31.39에서 0.94로 줄었다.

| 언어 | 실행 시간 |
|---|---|
| Python | 1.94s |
| C / C++ / Rust | 0.01s |

## 연습 방법

1. 읽기: 파이썬 버전을 한 줄씩 소리 내어 설명한다.
2. 백지 재작성: 파일을 닫고 빈 파일에 다시 짠다. 막히면 그 줄만 보고 다시 닫는다.
3. 결과 대조: 같은 seed로 실행해 위 표와 같은지 확인한다.
4. 변형: d=3을 추가하거나, 동점일 때 규칙을 바꿔 보고 결과를 예측한 뒤 실행한다.
5. 다른 언어로 옮기기: 파이썬을 보며 C++로 직접 옮긴다.
