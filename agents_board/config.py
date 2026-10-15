from pathlib import Path

# Base directories
BASE_DIR = Path.cwd()
AGENTS_DIR = BASE_DIR / ".agents"

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

# Roster and baton files
ROSTER_DIR = AGENTS_DIR / "roster"
BATON_FILE = AGENTS_DIR / "BATON.json"

# Rejection severities
SEVERITY_BLOCKER = "BLOCKER"
SEVERITY_MAJOR = "MAJOR"
SEVERITY_NITPICK = "NITPICK"

VALID_SEVERITIES = [SEVERITY_BLOCKER, SEVERITY_MAJOR, SEVERITY_NITPICK]

# Circuit breaker settings
DEFAULT_MAX_REJECTIONS = 2
