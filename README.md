# 基于 RAG 的网络安全知识库智能问答系统

采集解析安全文档 → 递归分块 → 向量化 → 混合检索 + Rerank → 带引用溯源的问答。

> 与 `llm-qa-eval` 接口一致（retrieve/generate），可直接作为其**被测对象**，形成「建 RAG → 测 RAG」闭环。
> 本系统已作为第 4 个被测对象接入 [llm-qa-eval](https://github.com/shian555/llm-qa-eval) 评测平台（在线 Demo 的「运行对比」页可看 A/B）。

> **输入护栏（v2，来自评测闭环的真实修复）**：llm-qa-eval 三维评测发现初版对注入/越狱无防御
> （inject 组通过率仅 73.3%：越狱载荷检索出含「绕过/伪造」标记词的正常语料，答案被判定攻破）。
> v2 新增输入护栏（`RAG_INPUT_GUARD=off` 可关闭，供 A/B 复测），复测 inject 100%，
> normal/hallucination 无退化。

## 架构

```
  文档 ──▶ 分块(512/50) ──▶ 向量库(FAISS) ──┐
                                             ├──▶ 混合检索(BM25+向量) ──▶ Rerank ──▶ LLM 生成(带[n]引用)
  查询 ───────────────────────────────────────┘
```

## 快速开始

```bash
pip install -r requirements.txt
python run.py -q "什么是 SQL 注入？"          # mock 离线
python -m pytest tests/test_rag.py -v
```

默认 `mock` 模式用关键词检索 + 规则生成（离线、确定性）。接入真实检索/大模型：

```bash
pip install sentence-transformers faiss-cpu rank-bm25 jieba
$env:LLM_API_KEY="你的 Key"
$env:LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
$env:LLM_MODEL="qwen2.5-7b-instruct"
python run.py -q "什么是 XSS？" --mode real
```

## 扩展语料到 500+ 篇

内置语料仅 15 篇作演示。真实场景按指南第 1.2 节批量导入 NVD/CVE、OWASP Top10、安全博客，替换 `corpus.py` 的 `DOCS` 或改造 `build_rag(docs=...)`。

## 诚实声明

- mock 模式是理想路径，证明「分块→检索→生成」链路正确；真实效果依赖语料规模与模型。
- 检索召回率、问答准确率、响应时间等数字，接入真实语料 + LLM 后实测（可用 `llm-qa-eval` 一键测出）。

## 简历 bullet（AI 版项目，可套用）

> 基于 RAG 的网络安全知识库问答：采集解析安全文档，递归分块（512/50）+ BGE 嵌入向量化，
> 构建 FAISS 向量库；向量 + BM25 混合检索 + Rerank 三级召回，Prompt 带引用溯源；
> 作为 llm-qa-eval 被测对象接入「召回率/准确率/引用准确性」三维评测闭环，检索召回率【实测】、响应 <3s。

## 待办 / 进阶

- [x] 作为被测对象接入 llm-qa-eval 三维评测，产出实测报告（inject 73.3%→100% 闭环）
- [ ] 导入真实 500+ 篇安全文档（NVD/CVE）
- [ ] FastAPI + Gradio 服务化封装
- [ ] 输入护栏从词表升级为轻量分类器
