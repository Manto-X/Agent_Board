import json
import sys
from pathlib import Path

# Paths resolution
SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCRIPT_DIR.parent
BASE_DIR = AGENTS_DIR.parent

# Ensure SCRIPT_DIR is in sys.path so sibling imports work everywhere
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Pipeline stages
STAGE_SPECS = "00_specs"
STAGE_BACKLOG = "01_backlog"
STAGE_IN_PROGRESS = "02_in_progress"
STAGE_REVIEW = "03_review"
STAGE_DONE = "04_done"
STAGE_ESCALATION = "05_escalation"

STAGES = [
    STAGE_SPECS,
    STAGE_BACKLOG,
    STAGE_IN_PROGRESS,
    STAGE_REVIEW,
    STAGE_DONE,
    STAGE_ESCALATION,
]

# Core paths inside .agents
ROSTER_DIR = AGENTS_DIR / "roster"
BATON_FILE = AGENTS_DIR / "BATON.json"
CONFIG_FILE = AGENTS_DIR / "project_config.json"
TEMPLATE_FILE = AGENTS_DIR / "template_task.md"

# Rejection severities
SEVERITY_BLOCKER = "BLOCKER"
SEVERITY_MAJOR = "MAJOR"
SEVERITY_NITPICK = "NITPICK"

VALID_SEVERITIES = [SEVERITY_BLOCKER, SEVERITY_MAJOR, SEVERITY_NITPICK]

# Default Settings
DEFAULT_MAX_REJECTIONS = 2

DEFAULT_CONFIG = {
    "project_name": "Agents_Board_Workspace",
    "version": "1.0.0",
    "roles": {
        "orchestrator": "antigravity",
        "mason": "claude",
        "reviewer": "codex",
    },
    "max_rejections": DEFAULT_MAX_REJECTIONS,
}

VALID_ROLES = ["orchestrator", "mason", "reviewer"]
VALID_PLATFORMS = ["antigravity", "claude", "codex"]


def load_project_config(base_dir: Path | None = None) -> dict:
    agents_dir = (base_dir / ".agents") if base_dir else AGENTS_DIR
    cfg_file = agents_dir / "project_config.json"
    if not cfg_file.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # Merge with defaults
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg)
            if "roles" in cfg:
                roles = DEFAULT_CONFIG["roles"].copy()
                roles.update(cfg["roles"])
                merged["roles"] = roles
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_project_config(cfg: dict, base_dir: Path | None = None) -> None:
    agents_dir = (base_dir / ".agents") if base_dir else AGENTS_DIR
    agents_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = agents_dir / "project_config.json"
    temp_file = agents_dir / "project_config.json.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    temp_file.replace(cfg_file)
