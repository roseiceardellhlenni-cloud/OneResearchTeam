"""论文写作专家 Agent — SCI 论文写作与投稿."""

from __future__ import annotations

from loguru import logger

from oneresearchteam.agents.base import BaseResearchAgent
from oneresearchteam.core.models import (
    ResearchRole,
    WritingTask,
)


class WritingSpecialistAgent(BaseResearchAgent):
    """论文写作专家 Agent.

    职责：
    - 按目标期刊格式撰写论文章节
    - 语言润色和学术表达优化
    - 图表说明撰写
    - 投稿格式检查
    - Cover letter 和回复审稿人意见
    """

    RESEARCH_ROLE = ResearchRole.WRITING_SPECIALIST

    # 目标期刊写作规范
    JOURNAL_GUIDES = {
        "nature": {
            "title_max_chars": 120,
            "abstract_max_words": 150,
            "main_text_style": "concise scientific",
            "reference_format": "numbered Vancouver",
        },
        "science": {
            "title_max_chars": 90,
            "abstract_max_words": 125,
            "main_text_style": "accessible scientific",
            "reference_format": "name-year",
        },
        "cell": {
            "title_max_chars": 135,
            "abstract_max_words": 150,
            "main_text_style": "comprehensive detail",
            "reference_format": "numbered Vancouver",
        },
        "default": {
            "title_max_chars": 120,
            "abstract_max_words": 300,
            "main_text_style": "standard scientific",
            "reference_format": "numbered Vancouver",
        },
    }

    def get_system_prompt(self) -> str:
        """论文写作专家的系统提示词."""
        base = super().get_system_prompt()

        ws_additional = (
            "【论文写作专家专属职责】\n"
            "- 所有章节必须严格遵循目标期刊的格式和字数要求\n"
            "- 语言风格：简洁、准确、客观；避免主观情感词汇\n"
            "- 时态：Methods用过去时，Results描述过去发现，Discussion用现在时\n"
            "- 数字使用：1-9拼写，10以上用阿拉伯数字（各期刊规则不同）\n"
            "- 首次出现的缩写需给出全称\n\n"
            "【各期刊特点】\n"
            "- Nature系列：标题简洁、摘要150词以内、强调研究意义\n"
            "- Science：标题抓眼球、摘要开门见山、强调重大突破\n"
            "- Cell系列：方法详细、讨论深入、图表要求高\n"
            "- Biomaterials / ACS系列：方法学详细、注重创新性验证\n\n"
            "【Cover Letter 写作要点】\n"
            "- 第一段：研究主题和主要发现\n"
            "- 第二段：为什么重要（创新点和意义）\n"
            "- 第三段：为什么适合该期刊\n"
            "- 第四段：声明无利益冲突，推荐审稿人\n\n"
            "【回复审稿人意见要点】\n"
            "- 逐条回应，不要遗漏任何意见\n"
            "- 态度谦虚但有理有据\n"
            "- 修改必须明确标注（diff或高亮）\n"
        )
        return f"{base}\n\n{ws_additional}"

    async def write_section(
        self,
        project_id: str,
        section: str,  # title / abstract / intro / methods / results / discussion
        target_journal: str,
        context: dict,
    ) -> str:
        """撰写论文章节.

        Args:
            project_id: 课题ID
            section: 章节名称
            target_journal: 目标期刊
            context: 写作上下文（数据、文献摘要等）
        Returns:
            章节文本
        """
        guide = self.JOURNAL_GUIDES.get(
            target_journal.lower(), self.JOURNAL_GUIDES["default"]
        )

        if section == "title":
            return await self._write_title(context, guide)
        elif section == "abstract":
            return await self._write_abstract(context, guide)
        elif section == "introduction":
            return await self._write_introduction(context)
        elif section == "methods":
            return await self._write_methods(context)
        elif section == "results":
            return await self._write_results(context)
        elif section == "discussion":
            return await self._write_discussion(context)
        return ""

    async def _write_title(self, context: dict, guide: dict) -> str:
        """撰写标题."""
        return context.get("title_suggestion", "待撰写标题")

    async def _write_abstract(self, context: dict, guide: dict) -> str:
        """撰写摘要."""
        return (
            "**Background:** [研究背景和目的]\n\n"
            "**Methods:** [实验设计和方法]\n\n"
            "**Results:** [主要发现]\n\n"
            "**Conclusion:** [结论和意义]\n"
        )

    async def _write_introduction(self, context: dict) -> str:
        """撰写引言.

        结构：
        1. 宽泛背景（领域重要性）
        2. 窄化到具体问题（已知/未知）
        3. 本研究目的和创新点
        """
        return (
            "## Introduction\n\n"
            "[段落1：本领域整体背景]\n\n"
            "[段落2：具体问题的研究现状和争议]\n\n"
            "[段落3：本研究的目的和假设]\n"
        )

    async def _write_methods(self, context: dict) -> str:
        """撰写方法.

        必须包含：伦理审批号、试剂信息、设备型号、统计方法
        """
        return (
            "## Materials and Methods\n\n"
            "### Ethical Statement\n"
            "[伦理审批信息]\n\n"
            "### Animals\n"
            "[动物信息：品系、年龄、体重、数量]\n\n"
            "### [具体方法1]\n"
            "[详细操作步骤]\n\n"
            "### Statistical Analysis\n"
            "[统计方法描述]\n"
        )

    async def _write_results(self, context: dict) -> str:
        """撰写结果.

        结构：按Fig顺序描述，每段先描述主要发现，再描述细节
        """
        return (
            "## Results\n\n"
            "### [主要发现1]（对应Figure 1）\n"
            "[描述结果，避免解释]\n\n"
            "### [主要发现2]（对应Figure 2）\n"
            "[描述结果]\n"
        )

    async def _write_discussion(self, context: dict) -> str:
        """撰写讨论.

        结构：
        1. 总结主要发现
        2. 与已有文献对比（一致性/差异）
        3. 机制解释
        4. 临床/应用意义
        5. 局限性和未来方向
        """
        return (
            "## Discussion\n\n"
            "[第一段：主要发现总结]\n\n"
            "[第二段：与文献对比]\n\n"
            "[第三段：机制讨论]\n\n"
            "[第四段：研究意义]\n\n"
            "[第五段：局限性]\n"
        )

    async def polish_language(self, text: str, level: str = "standard") -> str:
        """语言润色.

        Args:
            text: 原始文本
            level: 润色级别 standard / premium
        Returns:
            润色后文本
        """
        return text  # TODO: 集成语言润色工具

    async def write_cover_letter(self, project_id: str, target_journal: str) -> str:
        """撰写 Cover Letter."""
        return (
            f"Dear Editor,\n\n"
            f"We would like to submit our manuscript entitled "
            f"\"[Title]\" for consideration for publication in {target_journal}.\n\n"
            f"[研究意义和创新点]\n\n"
            f"This work is novel because [创新点].\n\n"
            f"We believe this manuscript is appropriate for {target_journal} because [原因].\n\n"
            f"Thank you for your consideration.\n\n"
            f"Sincerely,\n"
            f"[作者]\n"
        )

    async def respond_to_reviewers(
        self,
        original_manuscript: str,
        reviewer_comments: list[dict],
        revisions: dict,
    ) -> str:
        """撰写审稿人回复信.

        Args:
            original_manuscript: 原始Manuscript ID
            reviewer_comments: 审稿意见列表
            revisions: 修改内容
        Returns:
            完整回复信
        """
        response = "Point-by-Point Response to Reviewers:\n\n"
        for i, comment in enumerate(reviewer_comments, 1):
            response += f"Reviewer #{i} Comment:\n{comment.get('text', '')}\n\n"
            response += f"Author Response:\n{revisions.get(comment.get('id', ''), '已修改')}\n\n"
            response += "---\n\n"
        return response