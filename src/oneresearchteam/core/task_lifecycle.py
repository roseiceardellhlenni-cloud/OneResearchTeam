"""科研任务状态机 — 对应 OneManCompany 的 task_lifecycle."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class TaskPhase(str, Enum):
    """科研任务状态 — 对应 OneManCompany TaskPhase，适配科研流程."""
    PENDING = "pending"                    # 等待分配
    ASSIGNED = "assigned"                  # 已分配给研究员
    IN_PROGRESS = "in_progress"           # 执行中
    NEEDS_REVIEW = "needs_review"          # 等待 PI 审批
    APPROVED = "approved"                  # PI 审批通过
    REVISION = "revision"                  # 修订中
    COMPLETED = "completed"                # 完成
    BLOCKED = "blocked"                    # 被阻塞（缺数据/缺文献）


class ResearchTask(BaseModel):
    """科研任务 — 对应 OneManCompany 的 task_node."""
    task_id: str
    project_id: str
    title: str
    description: str
    assigned_role: str           # LITERATURE_RESEARCHER / EXPERIMENT_DESIGNER 等
    phase: str = TaskPhase.PENDING.value
    acceptance_criteria: list[str] = []
    output_path: str = ""
    result: str = ""
    created_at: str = ""
    completed_at: str = ""

    def can_transition(self, target: TaskPhase) -> bool:
        """检查状态转换是否合法."""
        valid_transitions = {
            TaskPhase.PENDING: [TaskPhase.ASSIGNED],
            TaskPhase.ASSIGNED: [TaskPhase.IN_PROGRESS, TaskPhase.BLOCKED],
            TaskPhase.IN_PROGRESS: [TaskPhase.NEEDS_REVIEW, TaskPhase.REVISION, TaskPhase.BLOCKED],
            TaskPhase.NEEDS_REVIEW: [TaskPhase.APPROVED, TaskPhase.REVISION],
            TaskPhase.APPROVED: [TaskPhase.COMPLETED],
            TaskPhase.REVISION: [TaskPhase.IN_PROGRESS, TaskPhase.NEEDS_REVIEW],
            TaskPhase.BLOCKED: [TaskPhase.IN_PROGRESS],
            TaskPhase.COMPLETED: [],  # 终态
        }
        return target in valid_transitions.get(TaskPhase(self.phase), [])

    def transition_to(self, target: TaskPhase) -> bool:
        """执行状态转换."""
        if self.can_transition(target):
            self.phase = target.value
            return True
        return False


# 科研流程阶段映射
RESEARCH_FLOW = [
    ("literature_review", "文献调研", ["literature_researcher"]),
    ("experiment_design", "实验方案设计", ["experiment_designer", "pi"]),
    ("data_collection", "数据采集", ["experiment_designer"]),
    ("data_analysis", "数据分析", ["data_analyst", "pi"]),
    ("manuscript_prep", "论文撰写", ["writing_specialist", "pi"]),
    ("peer_review", "同行评审", ["writing_specialist"]),
    ("revision", "修订", ["writing_specialist", "pi"]),
    ("submitted", "已投稿", []),
    ("published", "已发表", []),
]


def next_phase(current: str) -> str | None:
    """获取下一阶段."""
    phases = [p[0] for p in RESEARCH_FLOW]
    try:
        idx = phases.index(current)
        return phases[idx + 1] if idx + 1 < len(phases) else None
    except ValueError:
        return None