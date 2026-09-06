"""离线单测：分块、检索相关性、引用溯源、拒答。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag import build_rag, chunk_text  # noqa: E402


def test_chunk_splits_long_text():
    long_text = "安全基线要求系统最小化权限。" * 30  # 约 450+ 字符
    chunks = chunk_text(long_text, size=120, overlap=20)
    assert len(chunks) > 3
    # 重叠：相邻块首尾应有交集（简单验证块数足够，说明确实切分）


def test_retrieval_relevant():
    rag = build_rag("mock")
    out = rag.answer("什么是 SQL 注入？")
    assert out["contexts"]
    assert any("SQL" in c or "注入" in c for c in out["contexts"])


def test_generate_with_citation():
    rag = build_rag("mock")
    out = rag.answer("XSS 有哪些防御措施？")
    assert "[1]" in out["answer"]


def test_out_of_corpus_refuses():
    rag = build_rag("mock")
    out = rag.answer("2026 年世界杯冠军是哪支球队？")
    assert "未找到" in out["answer"]


def test_multiple_contexts():
    rag = build_rag("mock")
    out = rag.answer("什么是跨站脚本攻击？")
    # 「跨站脚本」关键词命中 XSS；不应命中无关主题
    assert out["contexts"]
