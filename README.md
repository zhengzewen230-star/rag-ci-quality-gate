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
---

✨ 核心特性与技术亮点
1.LLM-as-a-Judge 客观评测： 基于 DeepEval 框架重构评测套件，引入 FaithfulnessMetric 精确捕捉幻觉。
2.低耦合架构设计： 继承与重构 DeepEvalBaseLLM 基础类，统一 OpenAI SDK 调用规范，可无缝无感切换 DeepSeek、Qwen（通义千问）或 OpenAI 官方模型。
3.GitHub Actions 自动化拦截： 编写 .github/workflows/rag_ci.yml 脚本，配置 Exit Code 阻断机制，构建真实的 Quality Gate。
4.生产级安全与工程实践： 使用 GitHub Secrets 管理 API 密钥，结合 .gitignore 规避密钥泄露风险，并优化依赖拓扑以兼容 Linux 云端运行环境。

---

🛠️ 本地快速开始
1. 克隆仓库与准备环境
Bash
git clone [https://github.com/zhengzewen230-star/rag-ci-quality-gate.git](https://github.com/zhengzewen230-star/rag-ci-quality-gate.git)
cd rag-ci-quality-gate
# 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

2. 安装项目依赖
Bash
pip install -r requirements.txt

3. 配置环境变量
在项目根目录新建 .env 文件并填入 API Key 与 Endpoint：
DEEPSEEK_API_KEY=sk-xxxx你的Key
DEEPSEEK_BASE_URL=(https://api.siliconflow.cn/v1)

4. 运行本地评估测试
Bash
deepeval test run tests/test_rag_quality.py

---

📁 目录结构
Plaintext
rag-ci-quality-gate/
├── .github/
│   └── workflows/
│       └── rag_ci.yml       # GitHub Actions 自动化 CI 流水线配置
├── src/
├── rag_app.py          # RAG 基础管道与意图路由逻辑
├── tests/
│   ├── test_cases.json      # 业务自动化测试数据集
│   └── test_rag_quality.py  # DeepEval 评估逻辑与裁判模型重构定义
├── .gitignore               # Git 敏感信息与缓存忽略规则
├── requirements.txt         # 跨平台标准依赖声明
└── README.md                # 项目工程说明文档
