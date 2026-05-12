#!/usr/bin/env python3
"""POS 거래 데이터 → 지식그래프 시각화 (완전 무료, pyvis MIT)

agentmemory의 '관계 시각화' 정신을 단독 스크립트로 구현.
LLM 호출 없음 · 외부 API 호출 없음 · 로컬 단독 실행.

POS CSV → 단말·카테고리·결제수단 노드 + 거래 엣지 → HTML 그래프

설치 (한 줄):
  pip install pyvis

실행:
  python3 pos_graph.py                 # 기본: ./pos_data.csv
  python3 pos_graph.py path/to.csv     # 다른 CSV

결과:
  pos_graph.html (브라우저로 열기 — 인터랙티브 그래프)
"""
import csv
import sys
from pathlib import Path


def build_graph(csv_path: str, out_path: str = None):
    """POS CSV → pyvis Network → HTML 저장."""
    try:
        from pyvis.network import Network
    except ImportError:
        print("[ERROR] pyvis가 설치되어 있지 않습니다.")
        print("  pip install pyvis")
        sys.exit(1)

    net = Network(
        height="700px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#1a1a1a",
        directed=False,
    )
    # 그래프 물리 설정 (노드 간 적절한 간격)
    net.barnes_hut(gravity=-3000, spring_length=200)

    terminals = set()
    categories = set()
    payments = {}                    # payment_method -> 거래 횟수
    edges_tc = {}                    # (terminal, category) -> [count, total_amount]
    edges_cp = {}                    # (category, payment) -> count

    # CSV 읽기
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = row["terminal_id"]
            c = row["category"]
            amt = int(row["amount"])
            p = row["payment_method"]

            terminals.add(t)
            categories.add(c)
            payments[p] = payments.get(p, 0) + 1

            key_tc = (t, c)
            if key_tc not in edges_tc:
                edges_tc[key_tc] = [0, 0]
            edges_tc[key_tc][0] += 1
            edges_tc[key_tc][1] += amt

            key_cp = (c, p)
            edges_cp[key_cp] = edges_cp.get(key_cp, 0) + 1

    # 카테고리별 총 거래 (노드 크기 결정용)
    cat_totals = {}
    for (t, c), (count, total) in edges_tc.items():
        cat_totals[c] = cat_totals.get(c, 0) + count

    # 단말 노드 (파란색 원, 균일 크기)
    for t in sorted(terminals):
        net.add_node(
            t,
            label=t,
            color="#00b4d8",
            size=18,
            shape="dot",
            title=f"단말 {t}",
        )

    # 카테고리 노드 (노란색 원, 거래량 비례 크기)
    for c in sorted(categories):
        size = 15 + cat_totals.get(c, 0) * 0.4
        net.add_node(
            c,
            label=c,
            color="#fdd835",
            size=min(size, 50),
            shape="dot",
            title=f"{c} · {cat_totals.get(c, 0)}건",
        )

    # 결제수단 노드 (녹색 다이아몬드)
    for p in sorted(payments.keys()):
        net.add_node(
            p,
            label=p,
            color="#2d6a4f",
            size=22,
            shape="diamond",
            title=f"{p} · {payments[p]}건",
        )

    # 엣지 — 단말 ↔ 카테고리 (회색, 두께는 거래 횟수)
    for (t, c), (count, total) in edges_tc.items():
        net.add_edge(
            t,
            c,
            value=count,
            title=f"{count}건 / 총 {total:,}원",
            color={"color": "#cccccc", "highlight": "#0077b6"},
        )

    # 엣지 — 카테고리 ↔ 결제수단 (주황, 두께는 거래 횟수)
    for (c, p), count in edges_cp.items():
        net.add_edge(
            c,
            p,
            value=count,
            title=f"{count}건",
            color={"color": "#ffb74d", "highlight": "#e65100"},
        )

    # 출력 저장
    if out_path is None:
        out_path = Path(csv_path).parent / "pos_graph.html"
    net.save_graph(str(out_path))

    # 통계 출력
    print(f"Generated → {out_path}")
    print(f"  Nodes: {len(terminals)} terminals · {len(categories)} categories · {len(payments)} payments")
    print(f"  Edges: {len(edges_tc)} terminal-category · {len(edges_cp)} category-payment")
    print()
    print("브라우저에서 열기:")
    print(f"  file://{Path(out_path).absolute()}")
    print()
    print("그래프 보는 법:")
    print("  • 파란 원   = 단말기 (T01~T10)")
    print("  • 노란 원   = 카테고리 (식음료/생필품/...)")
    print("  • 녹색 다이아 = 결제수단 (카드/현금/모바일)")
    print("  • 회색 선   = 단말-카테고리 거래 (두께 = 거래량)")
    print("  • 주황 선   = 카테고리-결제 (두께 = 거래량)")
    print("  • 노드 호버 = 상세 통계")
    print("  • 드래그   = 노드 위치 변경 (관계 탐색)")


def main():
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = str(Path(__file__).parent / "pos_data.csv")

    if not Path(csv_path).exists():
        print(f"[ERROR] 파일 없음: {csv_path}")
        print("  먼저 generate_pos_data.py 실행하세요.")
        sys.exit(1)

    build_graph(csv_path)


if __name__ == "__main__":
    main()
