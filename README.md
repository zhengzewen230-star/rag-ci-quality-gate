# 🛡️ RAG Quality Gate CI Automation

[![RAG Quality Gate CI](https://github.com/zhengzewen230-star/rag-ci-quality-gate/actions/workflows/rag_ci.yml/badge.svg)](https://github.com/zhengzewen230-star/rag-ci-quality-gate/actions)
![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)
![Framework](https://img.shields.io/badge/Framework-DeepEval%20%7C%20PyTest-green)
![LLM Judge](https://img.shields.io/badge/LLM%20Judge-DeepSeek%20%2F%20Qwen-orange)

基于LLM-as-a-Judge理念与GitHub Actions CI/CD搭建的自动化 RAG（检索增强生成）质量门槛防护系统。

通过在云端构建流水线，对 RAG 系统的输出进行Faithfulness（忠实度/幻觉防护）等多维度量化评测，实现对“低质量或存在事实性幻觉”代码提交的自动化硬拦截。

---

💡 背景与核心痛点

在大模型（LLM）与 RAG 应用研发中，传统单元测试（Unit Test）难以有效断言非结构化文本的准确性。常见的工程痛点包括：
1. 幻觉难以自动化捕捉：RAG 回答偏离知识库事实，人工测试效率低下。
2. 缺乏发布防护：缺乏类似传统软件工程的 CI/CD 质量门槛，版本迭代容易引发隐蔽的质量退化（Regression）。

本项目的解决方案：将大模型评估框架（DeepEval）与现代 DevOps 流水线（GitHub Actions）无缝结合，在代码合并前（PR/Push）自动完成质量裁判，未达阈值自动阻断构建。

---

🏛️ 系统架构与工作流

```text
[ Developer Push Code ] 
       │
       ▼
[ GitHub Actions CI ] ➔ [ Linux (Ubuntu) Runner ]
       │
       ├── 1. Setup Python 3.11 & Install Dependencies
       ├── 2. Inject GitHub Secrets (DEEPSEEK_API_KEY)
       │
       ▼
[ DeepEval Evaluation Engine ]
       │
       ├── RAG System Input/Output ➔ LLM-as-a-Judge (DeepSeek / Qwen)
       ├── Metric: Faithfulness (Threshold = 0.8)
       │
       ├─── [ PASS (Score >= 0.8) ] ➔ 🟢 CI Green (Allow Merge)
       └─── [ FAIL (Score < 0.8)  ] ➔ 🔴 CI Red (Block Merge)
