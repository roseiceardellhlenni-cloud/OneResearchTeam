"""Nature Skills 工具封装 — 集成 scansci-pdf、Zotero MCP 等科研工具."""

from __future__ import annotations

from loguru import logger


class NatureTools:
    """Nature Skills 工具集 — 封装论文下载和文献管理工具。

    底层调用 OpenClaw 内置的 scansci-pdf MCP 工具和 Zotero MCP 工具。
    使用前请阅读 ~/.openclaw/workspace/skills/scansci-pdf/SKILL.md
    """

    def __init__(self):
        self._tool_cache = {}

    # -------------------------------------------------------------------------
    # 论文检索
    # -------------------------------------------------------------------------

    async def search_papers(
        self,
        query: str,
        limit: int = 10,
        year_from: int | None = None,
        year_to: int | None = None,
    ) -> list[dict]:
        """使用 OpenAlex API 检索学术论文.

        Args:
            query: 检索词（支持 AND / OR 布尔逻辑）
            limit: 返回结果数量（最大50）
            year_from: 最早发表年份
            year_to: 最晚发表年份
        Returns:
            文献列表，每项包含 title / authors / year / doi / journal / cited_by_count
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "scansci-pdf",
                "scansci_pdf_search",
                {
                    "query": query,
                    "limit": limit,
                    "year_from": year_from,
                    "year_to": year_to,
                },
            )
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.warning("[nature_tools] search_papers failed: {}", e)
            return []

    # -------------------------------------------------------------------------
    # 论文下载
    # -------------------------------------------------------------------------

    async def download_paper(
        self,
        identifier: str,
        output_dir: str = "",
        strategy: str = "fastest",
    ) -> str:
        """下载学术论文 PDF.

        Args:
            identifier: DOI（如 "10.1038/nature12373"）或 arXiv ID（如 "2301.00001"）
            output_dir: 保存目录，默认为 ~/Downloads/papers/
            strategy: 下载策略
                - "fastest": 多源竞速（默认）
                - "oa_first": 优先开放获取
                - "scihub_only": 仅 Sci-Hub
                - "legal_only": 仅合法来源
        Returns:
            PDF 本地路径，下载失败返回空字符串
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "scansci-pdf",
                "scansci_pdf_download",
                {
                    "identifier": identifier,
                    "output_dir": output_dir,
                    "strategy": strategy,
                },
            )
            return result if isinstance(result, str) else ""
        except Exception as e:
            logger.warning("[nature_tools] download_paper failed: {}", e)
            return ""

    async def batch_download(self, identifiers: list[str]) -> dict:
        """批量下载多篇论文.

        Args:
            identifiers: DOI 或 arXiv ID 列表
        Returns:
            下载结果 {"success": [...], "failed": [...]}
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "scansci-pdf",
                "scansci_pdf_batch_download",
                {
                    "identifiers": identifiers,
                    "scihub_enabled": True,
                },
            )
            return result if isinstance(result, dict) else {"success": [], "failed": identifiers}
        except Exception as e:
            logger.warning("[nature_tools] batch_download failed: {}", e)
            return {"success": [], "failed": identifiers}

    # -------------------------------------------------------------------------
    # 文献管理（Zotero）
    # -------------------------------------------------------------------------

    async def zotero_add_item(
        self,
        doi: str,
        collection_key: str = "",
    ) -> str:
        """将论文添加到 Zotero 文献库.

        Args:
            doi: 论文 DOI
            collection_key: Zotero 集合 key（可选）
        Returns:
            Zotero item key
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "zotero-mcp",
                "zotero_add_item",
                {"doi": doi, "collection_key": collection_key},
            )
            return result if isinstance(result, str) else ""
        except Exception as e:
            logger.warning("[nature_tools] zotero_add_item failed: {}", e)
            return ""

    async def zotero_get_items(self, collection_key: str = "") -> list[dict]:
        """获取 Zotero 文献库条目.

        Args:
            collection_key: 集合 key（空则获取全部）
        Returns:
            文献条目列表
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "zotero-mcp",
                "zotero_get_items",
                {"collection_key": collection_key} if collection_key else {},
            )
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.warning("[nature_tools] zotero_get_items failed: {}", e)
            return []

    async def zotero_search(self, query: str) -> list[dict]:
        """搜索 Zotero 文献库.

        Args:
            query: 检索词
        Returns:
            匹配的文献条目列表
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "zotero-mcp",
                "zotero_search_library",
                {"query": query},
            )
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.warning("[nature_tools] zotero_search failed: {}", e)
            return []

    # -------------------------------------------------------------------------
    # 引文获取
    # -------------------------------------------------------------------------

    async def get_citation(self, identifier: str, format: str = "bibtex") -> str:
        """获取论文引文格式.

        Args:
            identifier: DOI 或 arXiv ID
            format: bibtex / ris / endnote
        Returns:
            格式化引文字符串
        """
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "scansci-pdf",
                "scansci_pdf_citation",
                {"identifier": identifier, "format": format},
            )
            return result if isinstance(result, str) else ""
        except Exception as e:
            logger.warning("[nature_tools] get_citation failed: {}", e)
            return ""

    # -------------------------------------------------------------------------
    # 网络诊断
    # -------------------------------------------------------------------------

    async def check_network_health(self) -> dict:
        """检查网络连通性 — 下载源可用性."""
        from onemancompany.tools.mcp.server import call_mcp_tool
        try:
            result = await call_mcp_tool(
                "scansci-pdf",
                "scansci_pdf_health_check",
                {"detailed": True},
            )
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.warning("[nature_tools] check_network_health failed: {}", e)
            return {}


# 全局单例
nature_tools = NatureTools()