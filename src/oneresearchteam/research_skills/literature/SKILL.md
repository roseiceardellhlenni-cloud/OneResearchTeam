# 文献研究员技能定义

## 核心能力

### 1. 文献检索
- **OpenAlex API**: 免费学术检索，覆盖 2.4 亿篇论文
- **PubMed API**: 生物医学文献检索
- **CrossRef**: DOI 解析和元数据获取
- **Semantic Scholar**: 引文网络分析

### 2. 论文下载
- **scansci-pdf**: 多源下载（DOI / arXiv ID / Sci-Hub / 机构代理）
- 支持批量下载
- 自动重试和断点续传

### 3. 文献管理
- **Zotero MCP**: 文献库管理、引文插入
- 标签系统、集合管理
- PDF 自动关联

### 4. 文献分析
- **PICO 框架**: 干预性研究评估
- **SYRCLE 偏倚评估**: 动物实验研究
- **ROBINS-I**: 非随机化干预研究
- **文献地图**: 关键词共现、引用网络

## 检索策略模板

```
主题: [PCN-224] AND [photothermal] AND [antibacterial] AND [hydrogel]
方法: [synthesis] OR [preparation] OR [characterization]
物种: [pig] OR [swine] OR [porcine]
时间: 2021-2026
排序: cited_by_count（高引优先）
```

## 输出格式

每篇文献记录包含：
```
{
  "pmid": "",
  "doi": "",
  "title": "",
  "authors": [],
  "journal": "",
  "year": 0,
  "abstract": "",
  "keywords": [],
  "if": 0.0,  # Impact Factor
  "citations": 0,
  "relevance": "high/medium/low",
  "notes": ""
}
```