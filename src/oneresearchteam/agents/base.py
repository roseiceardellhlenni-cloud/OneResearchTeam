"""科研团队基础Agent — 继承自 OneManCompany BaseAgentRunner，适配科研场景."""

from __future__ import annotations

from loguru import logger

from onemancompany.agents.base import BaseAgentRunner, extract_final_content, make_llm
from oneresearchteam.core.models import ResearchRole


class BaseResearchAgent(BaseAgentRunner):
    """科研角色Agent基类.

    继承 OneManCompany BaseAgentRunner，注入科研场景的上下文：
    - Role identity prompt
    - Research skills
    - Nature Tools (scansci-pdf, Zotero MCP)
    """

    RESEARCH_ROLE: ResearchRole = ResearchRole.PI

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._research_role = self.RESEARCH_ROLE

    async def _get_role_identity_section(self) -> str:
        """注入角色身份定义 — 对应一人公司的 role_guide.md."""
        role_descriptions = {
            ResearchRole.PI: (
                "你是一位首席科学家（PI），拥有深厚的学术背景和丰富的研究经验。\n"
                "你的职责是：审批研究方案、把控研究方向、对研究成果负责。\n"
                "你决策谨慎，注重科学严谨性，同时关注研究的创新性和临床转化价值。\n"
                "在团队中，你是最终决策者，研究员、设计师、数据分析师和写作专家都向你汇报。"
            ),
            ResearchRole.LITERATURE_RESEARCHER: (
                "你是一位文献调研专家，精通学术检索与管理工具。\n"
                "你的职责是：系统性文献检索（OpenAlex/PubMed/Sci-Hub）、\n"
                "文献管理（Zotero）、论文下载（scansci-pdf）、文献分析与整理。\n"
                "你能够快速定位领域核心文献，追踪最新研究进展，识别研究空白和创新点。\n"
                "在团队中，你为所有研究阶段提供文献支撑，是研究的「情报中心」。"
            ),
            ResearchRole.EXPERIMENT_DESIGNER: (
                "你是一位实验设计方案专家，精通实验设计和生物医学研究方法。\n"
                "你的职责是：根据文献调研结果设计实验方案、定义实验分组和评价指标、\n"
                "制定标准操作规程（SOP）、考虑动物福利和伦理审批。\n"
                "你注重实验的可行性和科学性，同时关注统计效能和样本量计算。\n"
                "在团队中，你是实验方案的制定者，为数据采集提供方法学保障。"
            ),
            ResearchRole.DATA_ANALYST: (
                "你是一位数据分析师，精通生物统计和科研数据处理。\n"
                "你的职责是：设计数据采集方案、选择统计方法（T检验/ANOVA/生存分析等）、\n"
                "质量控制、图表制作（Python/GraphPad Prism）、结果解读。\n"
                "你对数据的真实性和可重复性负责，能够识别异常值和统计偏倚。\n"
                "在团队中，你是质量把关者，确保研究结果的统计学可靠性。"
            ),
            ResearchRole.WRITING_SPECIALIST: (
                "你是一位科研论文写作专家，精通 SCI 论文写作规范和高水平期刊要求。\n"
                "你的职责是：按照目标期刊格式撰写论文章节、语言润色和学术表达优化、\n"
                "图表说明撰写、投稿格式检查。\n"
                "你熟悉 Nature/Science/Cell 系列等高水平期刊的写作风格。\n"
                "在团队中，你负责将研究成果转化为符合发表标准的论文。"
            ),
        }
        return role_descriptions.get(self.RESEARCH_ROLE, "你是一位研究团队成员。")

    def get_system_prompt(self) -> str:
        """构建完整的系统提示词 — 组合角色身份 + 科研技能 + Nature Tools."""
        sections = []

        # 1. Role identity
        import asyncio
        try:
            role_section = asyncio.get_event_loop().run_until_complete(
                self._get_role_identity_section()
            )
        except RuntimeError:
            role_section = self._get_role_identity_section_sync()

        sections.append(f"【角色】\n{role_section}")

        # 2. Research context — 加载当前课题信息
        sections.append(
            "【当前课题】\n"
            "当前正在进行的课题信息请通过团队状态获取。\n"
            "你可以通过读取 workspace 下的课题文件了解项目背景。\n"
        )

        # 3. Nature Skills instruction
        sections.append(
            "【Nature Skills — 内置工具】\n"
            "你可以使用以下工具完成文献和数据相关工作：\n"
            "- scansci-pdf: 论文检索、下载、管理（DOI/arXiv ID / 关键词搜索）\n"
            "- Zotero MCP: 文献库管理、引文插入、文献同步\n"
            "- OpenAlex API: 学术文献检索（免费，无需API Key）\n"
            "- PubMed API: 生物医学文献检索\n"
            "在使用前，请阅读 ~/.openclaw/workspace/skills/scansci-pdf/SKILL.md 了解详细用法。\n"
        )

        # 4. Team collaboration protocol
        sections.append(
            "【团队协作规范】\n"
            "- PI（首席科学家）负责最终决策，其他成员不得擅自改变研究方向\n"
            "- 方案和数据必须经过 PI 审批后方可进入下一阶段\n"
            "- 定期向 PI 汇报进展，重要决策需等待审批反馈\n"
            "- 保持文档完整，每次迭代结果需归档\n"
        )

        return "\n\n".join(sections)

    def _get_role_identity_section_sync(self) -> str:
        """同步版本的角色身份获取（兼容非async调用）。"""
        role_descriptions = {
            ResearchRole.PI: "你是一位首席科学家（PI），拥有深厚的学术背景和丰富的研究经验。",
            ResearchRole.LITERATURE_RESEARCHER: "你是一位文献调研专家，精通学术检索与管理工具。",
            ResearchRole.EXPERIMENT_DESIGNER: "你是一位实验设计方案专家，精通实验设计和生物医学研究方法。",
            ResearchRole.DATA_ANALYST: "你是一位数据分析师，精通生物统计和科研数据处理。",
            ResearchRole.WRITING_SPECIALIST: "你是一位科研论文写作专家，精通 SCI 论文写作规范。",
        }
        return role_descriptions.get(self.RESEARCH_ROLE, "你是一位研究团队成员。")