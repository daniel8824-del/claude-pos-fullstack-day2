#!/usr/bin/env python3
"""POS 상권분석 실습 데이터 생성기 — Day 2 수업용

생성 데이터:
  - 정상 거래 200건 (시간대·카테고리·결제수단 가중치 적용)
  - 이상 거래 5건 (동일 단말 1초 내 중복 결제 — Phase 2 탐지 대상)

실행:
  python3 generate_pos_data.py

출력:
  pos_data.csv (같은 디렉토리)
"""
import csv
import random
import datetime
from pathlib import Path

random.seed(42)  # 재현 가능한 결과

N = 200
CATEGORIES = ["식음료", "생필품", "의류", "잡화", "디지털"]
PAYMENTS = ["카드", "현금", "모바일"]
TERMINALS = [f"T{i:02d}" for i in range(1, 11)]  # T01~T10

# 시간대별 가중치 (점심 12-13시 + 저녁 18-19시 피크)
HOURS = list(range(8, 22))
HOUR_WEIGHTS = [3, 4, 5, 8, 9, 6, 4, 3, 5, 7, 9, 8, 5, 3]

# 카테고리별 금액 분포 (원)
AMOUNT_RANGE = {
    "식음료": (3000, 25000),
    "생필품": (1000, 50000),
    "의류": (15000, 200000),
    "잡화": (2000, 30000),
    "디지털": (10000, 500000),
}

# 카테고리 등장 빈도 (식음료 40% / 생필품 25% / 잡화 15% / 의류 10% / 디지털 10%)
CAT_WEIGHTS = [40, 25, 10, 15, 10]

# 결제 수단 빈도 (카드 60% / 모바일 25% / 현금 15%)
PAY_WEIGHTS = [60, 15, 25]


def random_timestamp():
    """가상의 영업일 (2026-05-12) 8시~22시 사이 랜덤 시간"""
    base = datetime.datetime(2026, 5, 12, 8, 0, 0)
    h = random.choices(HOURS, weights=HOUR_WEIGHTS)[0]
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return base.replace(hour=h, minute=m, second=s)


def generate_normal_rows():
    """정상 거래 200건 생성"""
    rows = []
    for _ in range(N):
        ts = random_timestamp()
        term = random.choice(TERMINALS)
        cat = random.choices(CATEGORIES, weights=CAT_WEIGHTS)[0]
        lo, hi = AMOUNT_RANGE[cat]
        amt = random.randint(lo, hi)
        pay = random.choices(PAYMENTS, weights=PAY_WEIGHTS)[0]
        rows.append([ts.isoformat(), term, cat, amt, pay])
    return rows


def generate_anomalies(base_rows, count=5):
    """이상 거래 5건 생성 — 동일 단말 1초 내 중복 결제

    Phase 2 이상 탐지 실습에서 학생들이 찾아내야 할 케이스.
    """
    anomalies = []
    samples = random.sample(base_rows, count)
    for base in samples:
        base_ts = datetime.datetime.fromisoformat(base[0])
        # 1초 후 동일 단말·동일 금액 중복
        dup_ts = base_ts + datetime.timedelta(seconds=1)
        # 시간이 22:00을 넘으면 영업시간 내로 조정
        if dup_ts.hour >= 22:
            dup_ts = dup_ts.replace(hour=21, minute=59)
        anomalies.append([
            dup_ts.isoformat(),
            base[1],  # 동일 단말
            base[2],  # 동일 카테고리
            base[3],  # 동일 금액
            base[4],  # 동일 결제수단
        ])
    return anomalies


def main():
    # 데이터 생성
    normal_rows = generate_normal_rows()
    anomaly_rows = generate_anomalies(normal_rows, count=5)
    all_rows = normal_rows + anomaly_rows

    # 시간순 정렬
    all_rows.sort(key=lambda r: r[0])

    # CSV 저장
    out_path = Path(__file__).parent / "pos_data.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "terminal_id", "category", "amount", "payment_method"])
        writer.writerows(all_rows)

    # 통계 출력
    print(f"Generated {len(all_rows)} rows → {out_path}")
    print(f"  - Normal: {len(normal_rows)}")
    print(f"  - Anomalies: {len(anomaly_rows)} (동일 단말 1초 내 중복 결제)")
    print()
    print(f"카테고리 분포:")
    cat_count = {c: 0 for c in CATEGORIES}
    for r in all_rows:
        cat_count[r[2]] += 1
    for c, n in cat_count.items():
        bar = "█" * (n // 5)
        print(f"  {c:6s}  {n:4d}  {bar}")


if __name__ == "__main__":
    main()
