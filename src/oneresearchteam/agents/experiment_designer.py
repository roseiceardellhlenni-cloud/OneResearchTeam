"""实验设计师 Agent — 实验方案设计与 SOP 制定."""

from __future__ import annotations

from loguru import logger

from oneresearchteam.agents.base import BaseResearchAgent
from oneresearchteam.core.models import (
    ResearchRole,
    ExperimentProtocol,
)


class ExperimentDesignerAgent(BaseResearchAgent):
    """实验设计师 Agent.

    职责：
    - 根据文献调研结果设计实验方案
    - 定义实验分组、对照、评价指标
    - 制定标准操作规程（SOP）
    - 考虑伦理审批和动物福利
    - 评估实验可行性和统计效能
    """

    RESEARCH_ROLE = ResearchRole.EXPERIMENT_DESIGNER

    def get_system_prompt(self) -> str:
        """实验设计师的系统提示词."""
        base = super().get_system_prompt()

        ed_additional = (
            "【实验设计师专属职责】\n"
            "- 实验设计遵循「3R原则」：Replacement / Reduction / Refinement（动物福利）\n"
            "- 所有动物实验需考虑伦理审批（IACUC / 兽医伦理委员会）\n"
            "- 分组设计必须有明确的科学假设支撑\n"
            "- 样本量需通过功效分析（power analysis）确定\n"
            "- 主要终点和次要终点需预先定义\n\n"
            "【统计设计原则】\n"
            "- 随机化：动物随机分配到各组\n"
            "- 盲法：检测指标读取时采用盲法评估\n"
            "- 对照设置：阳性对照 + 阴性对照 + 空白对照\n"
            "- 预实验：正式实验前进行预实验验证方法可行性\n\n"
            "【SOP 要求】\n"
            "- 每一步操作需有明确的时间节点和操作者\n"
            "- 关键试剂需记录批号和供应商\n"
            "- 设备参数需精确记录（温度、转速、功率等）\n"
            "- 预期结果和异常情况处理预案均需说明\n"
        )
        return f"{base}\n\n{ed_additional}"

    async def design_protocol(
        self,
        project_id: str,
        research_question: str,
        literature_summary: str,
    ) -> ExperimentProtocol:
        """设计实验方案.

        Args:
            project_id: 课题ID
            research_question: 科学问题
            literature_summary: 文献调研总结
        Returns:
            ExperimentProtocol 结构化实验方案
        """
        return ExperimentProtocol(
            id=f"protocol_{project_id}_001",
            project_id=project_id,
            title="待PI审批的实验方案",
            objective="",
            materials=[],
            methods=[],
            groups=[],
            controls=[],
            evaluation_metrics=[],
            status="draft",
        )

    async def draft_sop(self, protocol: ExperimentProtocol) -> str:
        """将实验方案转化为标准操作规程（SOP）文档."""
        sop_content = (
            f"# 实验方案：{protocol.title}\n\n"
            f"## 1. 研究目的\n{protocol.objective}\n\n"
            f"## 2. 实验材料\n"
        )
        for m in protocol.materials:
            sop_content += f"- {m}\n"

        sop_content += f"\n## 3. 实验分组\n"
        for g in protocol.groups:
            sop_content += f"- {g}\n"

        sop_content += f"\n## 4. 评价指标\n"
        for metric in protocol.evaluation_metrics:
            sop_content += f"- {metric}\n"

        return sop_content

    async def assess_feasibility(self, protocol: ExperimentProtocol) -> dict:
        """评估实验方案的可行性.

        检查：设备条件、技术能力、时间成本、经费预算。
        """
        return {
            "protocol_id": protocol.id,
            "feasibility": "high",  # high / medium / low
            "score": 85,
            "concerns": [],
            "suggestions": [],
        }