#!/usr/bin/env python3
"""EXA API 테스트 — Day 2 강사 시연용 외부 리서치 도구

EXA API (https://exa.ai/):
  - AI-native semantic search
  - 무료 티어 1000 requests/month
  - LLM 친화적 결과 (스팸 제거, 신뢰도 점수)

사용 전:
  1. https://exa.ai/ 가입 → API 키 발급
  2. export EXA_API_KEY="your-key-here"
  3. pip install requests

실행:
  python3 exa_test.py
  python3 exa_test.py "검색어"
"""
import os
import sys
import json
import requests
from datetime import datetime

EXA_API_KEY = os.environ.get("EXA_API_KEY", "")
EXA_ENDPOINT = "https://api.exa.ai/search"


def exa_search(query: str, num_results: int = 10, search_type: str = "neural"):
    """EXA API로 검색 수행.

    Args:
        query: 검색어
        num_results: 결과 개수 (기본 10)
        search_type: "neural" (semantic) 또는 "keyword"

    Returns:
        dict: { results: [{ title, url, score, snippet, publishedDate }, ...] }
    """
    if not EXA_API_KEY:
        print("[ERROR] EXA_API_KEY 환경변수가 설정되지 않았습니다.")
        print("  export EXA_API_KEY='your-key-here'")
        print("  키 발급: https://exa.ai/")
        sys.exit(1)

    response = requests.post(
        EXA_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "x-api-key": EXA_API_KEY,
        },
        json={
            "query": query,
            "numResults": num_results,
            "type": search_type,
            "contents": {
                "text": True,
                "highlights": {"numSentences": 2},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def format_results(data: dict, show_text: bool = False):
    """결과를 사람이 읽기 쉽게 출력."""
    results = data.get("results", [])
    if not results:
        print("  (결과 없음)")
        return

    print(f"\n총 {len(results)}건 결과:\n")
    for i, r in enumerate(results, 1):
        score = r.get("score", 0.0)
        title = r.get("title", "(제목 없음)")
        url = r.get("url", "")
        pub_date = r.get("publishedDate", "")
        date_str = ""
        if pub_date:
            try:
                date_str = f"  ({pub_date[:10]})"
            except Exception:
                pass

        print(f"{i:2d}. [{score:.3f}]{date_str} {title}")
        print(f"    {url}")

        # 하이라이트 (있을 경우)
        highlights = r.get("highlights", [])
        if highlights:
            for h in highlights[:1]:
                preview = h[:150].replace("\n", " ")
                print(f"    \"{preview}...\"")

        if show_text:
            text = r.get("text", "")
            if text:
                print(f"    본문 미리보기: {text[:200]}...")

        print()


def demo_pos_research():
    """POS 상권분석 시연용 — 3가지 쿼리 자동 실행"""
    queries = [
        ("강남역 카페 상권 트렌드 2026", "neural"),
        ("POS 거래 이상 패턴 탐지 머신러닝", "neural"),
        ("retail point of sale data analysis Python", "keyword"),
    ]

    for query, stype in queries:
        print(f"\n{'=' * 70}")
        print(f"검색어: {query}")
        print(f"타입:   {stype}")
        print('=' * 70)
        try:
            data = exa_search(query, num_results=5, search_type=stype)
            format_results(data)
        except requests.HTTPError as e:
            print(f"[ERROR] HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {e}")


def main():
    if len(sys.argv) > 1:
        # 명령행 인수로 쿼리 전달
        query = " ".join(sys.argv[1:])
        print(f"검색어: {query}")
        data = exa_search(query, num_results=10)
        format_results(data, show_text=False)

        # JSON 저장 (선택)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"exa_result_{ts}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n→ JSON 저장: {out_path}")
    else:
        # 인수 없으면 POS 시연 모드
        print("EXA API 시연 모드 — POS 상권분석 3가지 쿼리 자동 실행")
        print("(명령행 인수로 쿼리 전달 시 단일 검색만 수행)")
        demo_pos_research()


if __name__ == "__main__":
    main()
