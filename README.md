# OneResearchTeam — AI 一人科研团队

> 一个由 AI驱动的全职能科研团队，模拟真实实验室的组织架构与工作流程。
> 一个人 + 一个团队 = 一支高效科研力量。

---

## 核心定位

将 OneManCompany 的「一人公司」框架迁移至科研场景，构建：

- **PI（首席科学家）** — 把握方向、审批方案、对结果负责
- **文献研究员（Literature Researcher）** — 文献检索、管理、分析
- **实验设计师（Experiment Designer）** — 方案设计、方法优化
- **数据分析师（Data Analyst）** — 统计分析、图表绘制
- **论文写作专家（Writing Specialist）** — SCI写作、润色、投稿

内置 Nature Skills（scansci-pdf、Zotero MCP）支持全流程文献管理。

---

## 对比：一人公司 vs 一人科研团队

| 维度 | OneManCompany | OneResearchTeam |
|------|--------------|-----------------|
| CEO → | PI（首席科学家） | 人类用户 |
| Engineer → | 研究员 / 实验设计师 | 执行具体实验方案 |
| QA → | 数据分析师 | 质量把关、统计验证 |
| HR → | 文献研究员 | 文献资源管理 |
| CSO → | 论文写作专家 | 成果输出、SCI发表 |

---

## 项目背景

本项目旨在探索**AI驱动的科研组织管理**，通过多Agent协作完成从文献调研→实验设计→数据分析→论文撰写的完整科研流程。

### 当前研究课题示例
**PCN-224@Ag⁺/CMCS可注射光热水凝胶在猪MRSA感染创面模型中的治疗效果与协同机制研究**
- 学科交叉：兽医药理 × 纳米医学 × 光生物学
- 核心问题：NIR触发的MOF光热水凝胶能否替代抗生素治疗猪细菌感染创面？

---

## 目录结构

```
OneResearchTeam/
├── src/oneresearchteam/
│   ├── agents/           # 五大科研角色Agent
│   │   ├── base.py
│   │   ├── pi_agent.py           # PI：方向把控、方案审批
│   │   ├── literature_researcher.py  # 文献调研、Zotero管理
│   │   ├── experiment_designer.py    # 实验方案设计
│   │   ├── data_analyst.py            # 数据处理与统计
│   │   ├── writing_specialist.py      # SCI论文写作
│   │   └── nature_tools.py           # Nature Skills工具封装
│   ├── core/
│   │   ├── models.py          # 科研角色枚举、数据结构
│   │   ├── research_state.py # 团队状态（课题、文献、数据）
│   │   └── task_lifecycle.py  # 科研任务状态机
│   └── research_skills/      # 各角色的技能定义
│       ├── literature/
│       ├── data_analysis/
│       ├── experiment_design/
│       └── writing/
├── company/              # 课题工作区（每个课题一个子目录）
├── config/
│   └── research_team.yaml  # 团队配置
├── docs/
│   ├── project_description.md  # 项目申请描述文档
│   └── research_protocols.md   # 标准操作规程
└── assets/
    ├── roles/            # 角色定义文档
    └── templates/        # 实验方案/论文模板
```

---

## 五大科研角色

### 1. PI（首席科学家）
- 审批研究方案和实验设计
- 把握研究方向，决定是否推进或转向
- 最终对研究成果负责

### 2. 文献研究员（Literature Researcher）
- 使用 OpenAlex / PubMed / Sci-Hub 进行文献检索
- 使用 Zotero MCP 管理文献库
- 使用 scansci-pdf 下载论文
- 整理文献笔记，绘制文献地图
- 追踪领域最新进展

### 3. 实验设计师（Experiment Designer）
- 根据文献调研结果设计实验方案
- 定义实验分组、对照、评价指标
- 考虑伦理审批和动物福利
- 输出标准操作规程（SOP）

### 4. 数据分析师（Data Analyst）
- 设计数据采集方案和数据类型
- 统计方法选择（T检验、ANOVA、生存分析等）
- 图表制作（GraphPad Prism / Python）
- 结果解读与质量控制

### 5. 论文写作专家（Writing Specialist）
- 遵循目标期刊格式（Nature/Science/Cell系列等）
- 撰写各章节：Title, Abstract, Introduction, Methods, Results, Discussion
- 语言润色和学术表达优化
- 投稿格式检查和图表美化

---

## 内置工具（Nature Skills）

| 工具 | 功能 |
|------|------|
| `scansci-pdf` | 论文检索、下载、管理 |
| `Zotero MCP` | 文献库管理、引文插入 |
| `OpenAlex API` | 文献检索 |
| `PubMed API` | 生物医学文献检索 |
| `Web Search` | 科研资讯获取 |

---

## 技术架构

基于 OneManCompany 核心框架改造：

- **Vessel + Talent 架构**：定义 Agent 的执行容器与技能包
- **多 Agent 协作**：PI 审批、文献研究员调研、实验设计师方案、数据分析师验证、写作专家输出
- **任务状态机**：文献调研 → 方案设计 → 实验执行 → 数据分析 → 论文撰写
- **心跳系统**：定期汇报进度，PI 可随时介入
- **知识库**：每次研究积累经验，形成 SOP 沉淀

---

## 项目申请描述

> **项目名称**：OneResearchTeam — AI驱动的全职能科研团队管理系统
>
> **项目概述**：
> OneResearchTeam 将 OneManCompany 的 AI 团队管理框架迁移至科研场景，构建一个由 PI、文献研究员、实验设计师、数据分析师和论文写作专家组成的 AI 科研团队，实现从文献调研→实验设计→数据分析→论文撰写的全流程自动化协作。
>
> **核心技术**：
> - 基于多 Agent 协作系统的科研团队管理框架
> - 集成 Nature Skills（scansci-pdf、Zotero MCP）进行文献管理
> - 参照真实实验室管理流程设计角色职责与晋升体系
> - 内置科研工作流引擎，支持多课题并行管理
>
> **应用场景**：
> 兽医药理研究（PCN-224 MOF光热水凝胶方向）、纳米医学、动物感染模型等跨学科研究项目的全流程管理。
>
> **预期产出**：
> 系统可同时支持多个研究课题，每个课题经历完整的五阶段流程，形成可复用的科研 SOP 知识库。

---

## 状态

🟡 开发中 — 核心框架搭建中