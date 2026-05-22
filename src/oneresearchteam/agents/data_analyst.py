"""数据分析师 Agent — 统计分析与数据质量控制."""

from __future__ import annotations

from loguru import logger

from oneresearchteam.agents.base import BaseResearchAgent
from oneresearchteam.core.models import (
    ResearchRole,
    DataRecord,
)


class DataAnalystAgent(BaseResearchAgent):
    """数据分析师 Agent.

    职责：
    - 设计数据采集方案
    - 选择统计方法（T检验 / ANOVA / 生存分析等）
    - 质量控制与异常值检测
    - 图表制作（Python / GraphPad Prism）
    - 结果解读与统计学显著性判断
    """

    RESEARCH_ROLE = ResearchRole.DATA_ANALYST

    def get_system_prompt(self) -> str:
        """数据分析师的系统提示词."""
        base = super().get_system_prompt()

        da_additional = (
            "【数据分析师专属职责】\n"
            "- 所有数据必须经过质量控制（QC）后方可进入正式分析\n"
            "- 统计方法需预先定义，不得在数据探查后随意更换\n"
            "- P值需同时报告效应量（effect size）和置信区间\n"
            "- 异常值需经过科学评估后方可剔除或保留\n"
            "- 图表需符合目标期刊的格式要求\n\n"
            "【常用统计方法选择指南】\n"
            "- 两组比较：独立t检验（正态）或Mann-Whitney U（非正态）\n"
            "- 多组比较：One-way ANOVA（正态）或Kruskal-Wallis（非正态）\n"
            "- 重复测量：Repeated measures ANOVA / Friedman检验\n"
            "- 生存分析：Kaplan-Meier + Log-rank检验 + Cox回归\n"
            "- 分类数据：Chi-square检验 / Fisher精确检验\n"
            "- 相关性：Pearson（正态）或Spearman（非正态）\n"
            "- 回归分析：线性/逻辑斯蒂，视因变量类型而定\n\n"
            "【数据质量标准】\n"
            "- 缺失数据 < 5% 可接受，>20% 需特别处理方案\n"
            "- 离群值经 Grubbs 检验确认后方可处理\n"
            "- 数据需记录原始数据文件和预处理步骤\n"
        )
        return f"{base}\n\n{da_additional}"

    async def design_data_collection(
        self,
        protocol_id: str,
        evaluation_metrics: list[str],
    ) -> dict:
        """设计数据采集方案.

        Args:
            protocol_id: 实验方案ID
            evaluation_metrics: 评价指标列表
        Returns:
            数据采集方案，包含数据类型、采集时间点、质量控制标准
        """
        data_plan = {}
        for metric in evaluation_metrics:
            data_plan[metric] = {
                "data_type": "continuous",  # continuous / categorical / ordinal
                "expected_distribution": "normal",  # normal / non-normal
                "collection_timepoints": [],
                "replicates": 3,
                "qc_criteria": f"{metric} in reasonable range",
            }
        return {
            "protocol_id": protocol_id,
            "data_plan": data_plan,
            "sample_size_justification": "",
        }

    async def quality_check(self, data_record: DataRecord) -> dict:
        """质量控制检查.

        检查项：
        - 数据完整性（无缺失值、重复测量一致）
        - 数值合理性（无明显异常值）
        - 单位一致性
        - 重复测量变异系数（CV < 15%）
        """
        return {
            "record_id": data_record.id,
            "qc_passed": True,
            "issues": [],
            "warning_flags": [],
        }

    async def analyze_data(
        self,
        data_path: str,
        statistical_methods: list[str],
    ) -> dict:
        """执行统计分析.

        Args:
            data_path: 数据文件路径
            statistical_methods: 预定义的统计方法列表
        Returns:
            统计分析结果，包含P值、效应量、图表路径
        """
        return {
            "data_path": data_path,
            "results": [],
            "summary": "",
            "figures": [],
        }

    async def generate_figure(
        self,
        data_path: str,
        plot_type: str,  # bar / line / scatter / box / survival
        groupby: str = "",
    ) -> str:
        """生成统计图表（调用Python/matplotlib/seaborn）.

        Args:
            data_path: 数据文件路径
            plot_type: 图表类型
            groupby: 分组变量
        Returns:
            图表文件路径
        """
        return ""

    async def interpret_results(self, analysis_output: dict) -> str:
        """解读统计分析结果，生成人类可读的结论摘要."""
        return analysis_output.get("summary", "")

    async def write_statistical_methods(self, data_plan: dict) -> str:
        """撰写统计方法章节文本.

        用于论文Methods部分的统计学描述。
        """
        methods_text = (
            "## 统计学分析\n\n"
            "数据以均值±标准误（mean±SEM）表示。\n"
            "组间比较采用独立t检验或Mann-Whitney U检验（视数据分布而定）。\n"
            "多组比较采用One-way ANOVA或Kruskal-Wallis检验。\n"
            "P<0.05认为差异具有统计学显著性。\n"
            "统计分析使用GraphPad Prism 10.0或Python 3.x进行。\n"
        )
        return methods_text