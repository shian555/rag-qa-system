"""CLI：提问并查看检索片段与带引用的回答。

用法：
    python run.py -q "什么是 SQL 注入？"            # mock 离线
    python run.py -q "什么是 XSS？" --mode real      # 接真实 LLM（需设 LLM_API_KEY 等）
"""
from __future__ import annotations

import argparse

from rag import build_rag


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", default="什么是 SQL 注入？")
    ap.add_argument("--mode", choices=["mock", "real"], default="mock")
    ap.add_argument("--k", type=int, default=8)
    args = ap.parse_args()

    rag = build_rag(mode=args.mode)
    out = rag.answer(args.query, k=args.k)

    print(f"问题：{out['question']}")
    print(f"\n检索片段（{len(out['contexts'])} 条）：")
    for i, c in enumerate(out["contexts"], 1):
        print(f"  [{i}] {c[:80]}")
    print(f"\n回答：\n{out['answer']}")


if __name__ == "__main__":
    main()
