# 数据分析师技能定义

## 核心能力

### 1. 统计方法
- **参数检验**: t 检验、ANOVA、线性回归
- **非参数检验**: Mann-Whitney、Wilcoxon、Kruskal-Wallis
- **生存分析**: Kaplan-Meier、Log-rank、Cox 回归
- **多变量分析**: PCA、聚类分析、热图

### 2. 数据质量控制
- **Grubbs 检验**: 异常值检测
- **Shapiro-Wilk**: 正态性检验
- **Levene 检验**: 方差齐性检验
- **CV 评估**: 变异系数 < 15%

### 3. 可视化
- **Python**: matplotlib / seaborn / plotly
- **GraphPad Prism**: 学术图表金标准
- **ImageJ**: 病理图像分析

### 4. 数据管理
- **原始数据**: 不可篡改，自动归档
- **数据字典**: 变量定义和编码说明
- **数据追溯**: 每步预处理完整记录

## 统计方法选择指南

| 数据类型 | 两组 | 三组+ | 配对/重复测量 |
|---------|------|-------|--------------|
| 连续正态 | t 检验 | ANOVA | 重复测量 ANOVA |
| 连续非正态 | Mann-Whitney | Kruskal-Wallis | Friedman |
| 分类数据 | Chi-square | Chi-square | McNemar |
| 生存数据 | Log-rank | Log-rank | 条件风险模型 |

## 统计效能计算

```python
from statsmodels.stats.power import tt_ind_solve_power
effect_size = 0.8  # Cohen's d
alpha = 0.05
power = 0.8
n_per_group = tt_ind_solve_power(effect_size=effect_size, alpha=alpha, power=power)
print(f"每组所需样本量: {int(n_per_group)}")
```

## 图表规范

| 图表类型 | 适用场景 | 格式要求 |
|---------|---------|---------|
| 柱状图 | 离散的组间比较 | 均值±SEM，*表示P值 |
| 折线图 | 时间序列数据 | 独立点+误差棒 |
| 散点图 | 相关性分析 | 带回归线+置信区间 |
| 箱线图 | 分布描述 | 显示中位数/四分位/异常值 |
| 生存曲线 | 生存分析 | Kaplan-Meier + Log-rank P |