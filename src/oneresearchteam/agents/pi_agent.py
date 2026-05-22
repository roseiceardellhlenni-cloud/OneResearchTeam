"""PI Agent — 首席科学家，审批研究方向和方案."""

from __future__ import annotations

from loguru import logger

from oneresearchteam.agents.base import BaseResearchAgent
from oneresearchteam.core.models import ResearchRole


class PIAgent(BaseResearchAgent):
    """PI Agent — 首席科学家.

    职责：
    - 审批研究方案和实验设计
    - 把控研究方向，决定是否推进或转向
    - 最终对研究成果负责
    - 审核论文和数据质量
    """

    RESEARCH_ROLE = ResearchRole.PI

    def get_system_prompt(self) -> str:
        """PI 的系统提示词 — 强调决策权威和科学严谨性."""
        base = super().get_system_prompt()

        pi_additional = (
            "【PI 专属职责】\n"
            "- 你对课题的学术方向负最终责任\n"
            "- 所有研究方案必须经过你审批才能执行\n"
            "- 你有权暂停、转向或终止不符合科学标准的研究\n"
            "- 论文投稿前必须经你审核同意\n"
            "- 关注研究的创新性、科学严谨性和临床转化价值\n\n"
            "【决策风格】\n"
            "- 谨慎保守：在没有充分证据前不轻易改变方向\n"
            "- 注重证据：决策必须基于数据和文献\n"
            "- 鼓励创新：在安全范围内支持探索性尝试\n"
        )
        return f"{base}\n\n{pi_additional}"

    async def approve_protocol(self, protocol_id: str, decision: str) -> dict:
        """审批实验方案.

        Args:
            protocol_id: 实验方案ID
            decision: approved / rejected / revision_required
        """
        return {
            "status": "ok",
            "protocol_id": protocol_id,
            "decision": decision,
            "approved_by": "PI",
        }

    async def review_progress(self, project_id: str) -> dict:
        """审核课题进度 — PI 定期检查."""
        return {
            "project_id": project_id,
            "review_status": "noted",
            "feedback": "继续推进，注意数据质量控制。",
        }