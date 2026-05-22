"""科研团队核心数据模型 — OneResearchTeam."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ResearchRole(str, Enum):
    """科研团队角色 — 对应一人公司的 EmployeeRole."""
    PI = "PI"                        # 首席科学家 / 课题负责人
    LITERATURE_RESEARCHER = "LR"     # 文献研究员
    EXPERIMENT_DESIGNER = "ED"       # 实验设计师
    DATA_ANALYST = "DA"              # 数据分析师
    WRITING_SPECIALIST = "WS"        # 论文写作专家


class ResearchPhase(str, Enum):
    """科研流程阶段 — 对应一人公司的 TaskPhase."""
    LITERATURE_REVIEW = "literature_review"    # 文献调研
    EXPERIMENT_DESIGN = "experiment_design"     # 实验方案设计
    DATA_COLLECTION = "data_collection"         # 数据采集
    DATA_ANALYSIS = "data_analysis"             # 数据分析
    MANUSCRIPT_PREP = "manuscript_prep"         # 论文撰写
    PEER_REVIEW = "peer_review"                 # 同行评审
    SUBMITTED = "submitted"                     # 已投稿
    REVISION = "revision"                       # 修订中
    PUBLISHED = "published"                     # 已发表


class Department(str, Enum):
    """部门 — 映射到一人公司的 Department."""
    PI_OFFICE = "PI Office"          # PI办公室
    LITERATURE = "Literature"       # 文献部
    EXPERIMENT = "Experiment"       # 实验部
    DATA = "Data"                   # 数据部
    WRITING = "Writing"             # 写作部


class ResearchStatus(str, Enum):
    """课题状态."""
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class FileEditProposal(BaseModel):
    """方案/文档修改提案 — 对应一人公司的 FileEditProposal."""
    edit_id: str
    file_path: str
    rel_path: str = ""
    old_content: str = ""
    new_content: str = ""
    reason: str = ""
    proposed_by: str = ""
    original_md5: str = ""
    decision: str = "pending"  # pending / approved / rejected
    decided_at: datetime | None = None
    executed: bool = False
    expired: bool = False


# ---------------------------------------------------------------------------
# Research Project
# ---------------------------------------------------------------------------

class ResearchIteration(BaseModel):
    """研究迭代 — 对应一人公司的 ProjectIteration."""
    id: str
    task: str
    phase: ResearchPhase = ResearchPhase.LITERATURE_REVIEW
    acceptance_criteria: list[str] = []
    timeline: list[dict] = []
    output: str = ""
    cost_usd: float = 0.0
    tokens_used: int = 0


class ResearchProject(BaseModel):
    """研究课题 — 对应一人公司的 Project."""
    id: str
    name: str
    slug: str
    created_at: datetime = Field(default_factory=datetime.now)
    current_phase: ResearchPhase = ResearchPhase.LITERATURE_REVIEW
    iterations: list[ResearchIteration] = []
    workspace_path: str = ""
    status: ResearchStatus = ResearchStatus.ACTIVE
    description: str = ""           # 课题描述（PXYV框架）
    research_question: str = ""      # 科学问题
    target_journal: str = ""         # 目标期刊

    def current_iteration(self) -> ResearchIteration | None:
        if self.iterations:
            return self.iterations[-1]
        return None


# ---------------------------------------------------------------------------
# Literature Record
# ---------------------------------------------------------------------------

class LiteratureRecord(BaseModel):
    """文献记录 — 来源：Zotero / OpenAlex / PubMed."""
    pmid: str = ""          # PubMed ID
    doi: str = ""           # DOI
    title: str = ""
    authors: list[str] = []
    journal: str = ""
    year: int = 0
    abstract: str = ""
    keywords: list[str] = []
    zotero_key: str = ""    # Zotero item key
    pdf_path: str = ""      # 本地PDF路径
    notes: str = ""         # 阅读笔记
    relevance_score: float = 0.0  # 相关性评分
    added_at: datetime = Field(default_factory=datetime.now)


# ---------------------------------------------------------------------------
# Experiment Protocol
# ---------------------------------------------------------------------------

class ExperimentProtocol(BaseModel):
    """实验方案 — 标准操作规程（SOP）."""
    id: str
    project_id: str
    title: str = ""
    objective: str = ""
    materials: list[str] = []
    methods: list[str] = []
    groups: list[str] = []           # 实验分组
    controls: list[str] = []         # 对照组
    evaluation_metrics: list[str] = []  # 评价指标
    expected_outcomes: str = ""
    potential_pitfalls: list[str] = []
    ethics_approval: str = ""
    sop_path: str = ""               # SOP文档路径
    status: str = "draft"            # draft / approved / running / completed
    approved_by: str = ""            # PI审批


# ---------------------------------------------------------------------------
# Data Record
# ---------------------------------------------------------------------------

class DataRecord(BaseModel):
    """数据记录 — 实验产生的数据."""
    id: str
    project_id: str
    experiment_id: str
    data_type: str = ""      # 数值型 / 图像 / 测序等
    file_path: str = ""
    description: str = ""
    collected_at: datetime = Field(default_factory=datetime.now)
    quality_check: bool = False  # 质控是否通过


# ---------------------------------------------------------------------------
# Writing Task
# ---------------------------------------------------------------------------

class WritingTask(BaseModel):
    """论文撰写任务."""
    project_id: str
    target_journal: str = ""
    section: str = ""         # Introduction / Methods / Results 等
    content: str = ""
    status: str = "pending"    # pending / drafted / reviewed / approved
    reviewed_by: str = ""      # 审核人（PI）
    draft_version: int = 1