// Power of Two Random Choices (Rust 버전)
// 실행: cargo run --release -- [n] [m] [seed]

struct XorShift64 {
    state: u64,
}

impl XorShift64 {
    fn new(seed: u64) -> Self {
        let state = if seed != 0 { seed } else { 0x9E3779B97F4A7C15 };
        Self { state }
    }

    // &mut self: 상태를 바꾸니까 가변 참조로 빌린다
    fn next(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13; // Rust의 <<는 u64에서 넘치는 비트를 버린다 (C와 같음)
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }

    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

fn simulate(n: usize, m: u64, d: u32, seed: u64) -> Vec<u64> {
    let mut rng = XorShift64::new(seed);
    let mut loads = vec![0u64; n]; // C++ vector처럼 스코프를 벗어나면 해제된다
    for _ in 0..m {
        let mut best = rng.below(n as u64) as usize;
        for _ in 1..d {
            let cand = rng.below(n as u64) as usize;
            if loads[cand] < loads[best] {
                best = cand;
            }
        }
        loads[best] += 1;
    }
    loads // 마지막 식이 반환값. 소유권이 호출한 쪽으로 넘어간다
}

// &[u64]: 빌려서 읽기만 한다. 소유권을 가져가지 않는다
fn report(d: u32, loads: &[u64]) {
    let max = loads.iter().max().unwrap();
    let min = loads.iter().min().unwrap();
    let n = loads.len() as f64;
    let mean = loads.iter().sum::<u64>() as f64 / n;
    let var = loads.iter().map(|&x| (x as f64 - mean).powi(2)).sum::<f64>() / n;
    println!("d={d}  max={max}  min={min}  std={:.2}", var.sqrt());
}

fn arg<T: std::str::FromStr>(args: &[String], i: usize, default: T) -> T {
    args.get(i).and_then(|s| s.parse().ok()).unwrap_or(default)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = arg(&args, 1, 1000);
    let m: u64 = arg(&args, 2, 1_000_000);
    let seed: u64 = arg(&args, 3, 42);
    if n == 0 {
        eprintln!("n must be > 0");
        std::process::exit(1);
    }

    println!("n={n} m={m} seed={seed} (평균 {:.0}개)", m as f64 / n as f64);
    for d in 1..=2 {
        report(d, &simulate(n, m, d, seed));
    }
}
