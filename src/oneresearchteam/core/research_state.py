"""科研团队状态管理 — 对应 OneManCompany 的 company_state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from oneresearchteam.core.models import (
    ResearchPhase,
    ResearchProject,
    ResearchStatus,
    LiteratureRecord,
    ExperimentProtocol,
    DataRecord,
    WritingTask,
)


@dataclass
class ResearchTeamState:
    """科研团队全局状态 — 对应 OneManCompany 的 company_state.

    管理：
    - 当前活跃课题列表
    - 各课题的文献库
    - 实验方案状态
    - 数据记录
    - 论文撰写任务
    """

    # 当前活跃课题
    active_projects: dict[str, ResearchProject] = field(default_factory=dict)

    # 各课题的文献记录 {project_id: [LiteratureRecord]}
    literature_db: dict[str, list[LiteratureRecord]] = field(default_factory=dict)

    # 各课题的实验方案 {project_id: ExperimentProtocol}
    protocols: dict[str, ExperimentProtocol] = field(default_factory=dict)

    # 各课题的数据记录 {project_id: [DataRecord]}
    data_records: dict[str, list[DataRecord]] = field(default_factory=dict)

    # 各课题的论文写作任务 {project_id: WritingTask}
    writing_tasks: dict[str, WritingTask] = field(default_factory=dict)

    # 团队角色状态 {role: status}
    team_status: dict[str, str] = field(default_factory=dict)

    # 当前 PI 审批队列
    pending_approvals: list[str] = field(default_factory=list)  # [protocol_id, ...]

    def add_project(self, project: ResearchProject) -> None:
        """添加新课题."""
        self.active_projects[project.id] = project
        self.literature_db.setdefault(project.id, [])
        self.data_records.setdefault(project.id, [])

    def get_project(self, project_id: str) -> ResearchProject | None:
        return self.active_projects.get(project_id)

    def advance_phase(self, project_id: str, to_phase: ResearchPhase) -> None:
        """推进课题阶段."""
        project = self.get_project(project_id)
        if project:
            project.current_phase = to_phase

    def add_literature(self, project_id: str, record: LiteratureRecord) -> None:
        """添加文献到课题文献库."""
        self.literature_db.setdefault(project_id, []).append(record)

    def set_protocol(self, project_id: str, protocol: ExperimentProtocol) -> None:
        """设置实验方案."""
        self.protocols[project_id] = protocol
        if protocol.status == "draft":
            self.pending_approvals.append(protocol.id)

    def get_protocol(self, project_id: str) -> ExperimentProtocol | None:
        return self.protocols.get(project_id)

    def approve_protocol(self, protocol_id: str, approved_by: str = "PI") -> bool:
        """PI 审批实验方案."""
        for protocol in self.protocols.values():
            if protocol.id == protocol_id:
                protocol.status = "approved"
                protocol.approved_by = approved_by
                if protocol_id in self.pending_approvals:
                    self.pending_approvals.remove(protocol_id)
                return True
        return False

    def add_data_record(self, project_id: str, record: DataRecord) -> None:
        self.data_records.setdefault(project_id, []).append(record)

    def get_latest_data(self, project_id: str) -> list[DataRecord]:
        return self.data_records.get(project_id, [])

    def get_team_status(self, role: str) -> str:
        return self.team_status.get(role, "idle")

    def set_team_status(self, role: str, status: str) -> None:
        self.team_status[role] = status

    def summary(self) -> str:
        """生成状态摘要."""
        lines = [
            f"=== 科研团队状态 ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ===",
            f"活跃课题数: {len(self.active_projects)}",
            f"待审批方案数: {len(self.pending_approvals)}",
            "",
        ]
        for pid, proj in self.active_projects.items():
            lines.append(
                f"  [{proj.id}] {proj.name} — 阶段: {proj.current_phase.value} "
                f"({proj.status.value})"
            )
        return "\n".join(lines)


# 全局单例
research_team_state = ResearchTeamState()