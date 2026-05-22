"""文献研究员 Agent — 文献检索、管理、分析.

使用 Nature Skills：
- scansci-pdf: 论文下载
- Zotero MCP: 文献库管理
- OpenAlex / PubMed: 文献检索
"""

from __future__ import annotations

from loguru import logger

from oneresearchteam.agents.base import BaseResearchAgent
from oneresearchteam.core.models import ResearchRole, LiteratureRecord


class LiteratureResearcherAgent(BaseResearchAgent):
    """文献研究员 Agent.

    职责：
    - 文献检索（OpenAlex / PubMed / Sci-Hub）
    - 论文下载（scansci-pdf）
    - 文献管理（Zotero MCP）
    - 文献分析与整理
    - 追踪领域最新进展
    - 识别研究空白和创新点
    """

    RESEARCH_ROLE = ResearchRole.LITERATURE_RESEARCHER

    async def search_literature(self, query: str, max_results: int = 20) -> list[LiteratureRecord]:
        """检索文献.

        使用 OpenAlex API 或 PubMed 进行文献检索。
        返回结构化文献记录列表。
        """
        # TODO: 集成 OpenAlex / PubMed API
        return []

    async def download_paper(self, identifier: str, output_dir: str = "") -> str:
        """下载论文.

        Args:
            identifier: DOI 或 arXiv ID
            output_dir: 保存目录
        Returns:
            PDF 本地路径
        """
        # TODO: 调用 scansci-pdf tool
        return ""

    async def add_to_zotero(self, record: LiteratureRecord) -> dict:
        """将文献添加到 Zotero 文献库.

        使用 Zotero MCP 工具。
        """
        # TODO: 集成 Zotero MCP
        return {"status": "added", "zotero_key": record.zotero_key}

    async def analyze_literature(self, project_id: str) -> dict:
        """文献分析 — 绘制文献地图、识别研究空白.

        输出：
        - 核心文献列表
        - 研究趋势时间线
        - 研究空白分析
        - 创新点建议
        """
        return {
            "project_id": project_id,
            "core_papers": [],
            "research_gaps": [],
            "innovation_suggestions": [],
            "timeline": {},
        }

    async def track_latest(self, keywords: list[str]) -> list[dict]:
        """追踪最新文献 — 定期检查新发表的相关论文."""
        return []

    def get_system_prompt(self) -> str:
        """文献研究员的系统提示词."""
        base = super().get_system_prompt()

        lr_additional = (
            "【文献研究员专属职责】\n"
            "- 每次文献调研需覆盖：核心机制、实验方法、数据呈现三个维度\n"
            "- 文献追踪需覆盖最近3年，重要引文需向前追溯5年\n"
            "- 新文献下载后自动整理摘要和关键发现\n"
            "- 识别文献质量（IF > 10 优先，高引论文优先）\n"
            "- 使用 PICO 框架评估干预性研究（Population/Intervention/Comparator/Outcome）\n\n"
            "【文献检索规范】\n"
            "- 关键词需覆盖：主题词 + 方法词 + 物种词\n"
            "- 检索策略需记录，支持复现\n"
            "- 每篇重要文献需评估偏倚风险（SYRCLE/ROBINS-I）\n"
        )
        return f"{base}\n\n{lr_additional}"