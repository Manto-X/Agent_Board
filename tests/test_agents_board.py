import tempfile
import unittest
from pathlib import Path

from agents_board.baton import get_baton, set_baton
from agents_board.config import (
    SEVERITY_BLOCKER,
    SEVERITY_NITPICK,
    STAGE_BACKLOG,
    STAGE_DONE,
    STAGE_ESCALATION,
    STAGE_IN_PROGRESS,
    STAGE_REVIEW,
)
from agents_board.init import init_board
from agents_board.roster import sync_roster_to_agents
from agents_board.task import (
    create_task,
    find_task,
    list_tasks,
    move_task,
    parse_task_file,
    reject_task,
)


class TestAgentsBoard(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_board(self):
        init_board(base_dir=self.root)

        agents_dir = self.root / ".agents"
        self.assertTrue((agents_dir / "00_specs").exists())
        self.assertTrue((agents_dir / "01_backlog").exists())
        self.assertTrue((agents_dir / "02_in_progress").exists())
        self.assertTrue((agents_dir / "03_review").exists())
        self.assertTrue((agents_dir / "04_done").exists())
        self.assertTrue((agents_dir / "05_escalation").exists())
        self.assertTrue((agents_dir / "roster").exists())
        self.assertTrue((agents_dir / "BATON.json").exists())

        # Check synced agent files
        self.assertTrue((self.root / "CLAUDE.md").exists())
        self.assertTrue((self.root / "CODEX.md").exists())
        self.assertTrue((self.root / "AGENTS.md").exists())
        self.assertTrue((self.root / "template_task.md").exists())

    def test_baton_flow(self):
        init_board(base_dir=self.root)

        baton = get_baton(base_dir=self.root)
        self.assertEqual(baton["holder"], "orchestrator")

        # Pass baton to mason
        set_baton(
            holder="mason",
            task_id="TASK-01",
            action="implementing",
            base_dir=self.root,
        )
        baton = get_baton(base_dir=self.root)
        self.assertEqual(baton["holder"], "mason")
        self.assertEqual(baton["task_id"], "TASK-01")
        self.assertEqual(baton["action"], "implementing")

    def test_task_lifecycle_happy_path(self):
        init_board(base_dir=self.root)

        # 1. Create task in backlog
        task_path = create_task(
            task_id="TASK-100",
            title="Setup database migrations",
            assignee="mason",
            reviewer="reviewer",
            base_dir=self.root,
        )
        self.assertTrue(task_path.exists())
        self.assertIn("01_backlog", str(task_path))

        # 2. Move to in_progress
        task_path = move_task("TASK-100", STAGE_IN_PROGRESS, base_dir=self.root)
        self.assertIn("02_in_progress", str(task_path))
        self.assertFalse((self.root / ".agents" / STAGE_BACKLOG / "TASK-100.md").exists())

        # 3. Move to review
        task_path = move_task("TASK-100", STAGE_REVIEW, base_dir=self.root)
        self.assertIn("03_review", str(task_path))

        # 4. Move to done
        task_path = move_task("TASK-100", STAGE_DONE, base_dir=self.root)
        self.assertIn("04_done", str(task_path))

        # 5. Check list
        board = list_tasks(base_dir=self.root)
        self.assertEqual(len(board[STAGE_DONE]), 1)
        self.assertEqual(board[STAGE_DONE][0]["id"], "TASK-100")

    def test_nitpick_does_not_reject(self):
        init_board(base_dir=self.root)
        create_task(
            task_id="TASK-200",
            title="Clean refactor",
            assignee="mason",
            reviewer="reviewer",
            base_dir=self.root,
        )
        move_task("TASK-200", STAGE_REVIEW, base_dir=self.root)

        # Reject as NITPICK
        res = reject_task(
            task_id="TASK-200",
            reason="Variable names could be slightly shorter",
            severity=SEVERITY_NITPICK,
            base_dir=self.root,
        )
        self.assertEqual(res["status"], "ADVISORY_ONLY")
        self.assertEqual(res["reject_count"], 0)

        # Ensure task is still in review
        found = find_task("TASK-200", base_dir=self.root)
        self.assertIsNotNone(found)
        p, meta, body = found
        self.assertIn("03_review", str(p))
        self.assertIn("Advisory (NITPICK)", body)

    def test_circuit_breaker_on_repeated_rejections(self):
        init_board(base_dir=self.root)
        create_task(
            task_id="TASK-300",
            title="Complex algorithm",
            assignee="mason",
            reviewer="reviewer",
            max_rejections=2,
            base_dir=self.root,
        )
        move_task("TASK-300", STAGE_REVIEW, base_dir=self.root)

        # Rejection 1
        res1 = reject_task(
            task_id="TASK-300",
            reason="Algorithm fails edge case with empty list",
            severity=SEVERITY_BLOCKER,
            test_file="tests/test_edge.py",
            base_dir=self.root,
        )
        self.assertEqual(res1["status"], "REJECTED")
        self.assertEqual(res1["reject_count"], 1)
        self.assertEqual(res1["stage"], STAGE_IN_PROGRESS)

        # Check baton given back to mason
        baton = get_baton(base_dir=self.root)
        self.assertEqual(baton["holder"], "mason")

        # Mason re-submits to review
        move_task("TASK-300", STAGE_REVIEW, base_dir=self.root)

        # Rejection 2 (Circuit breaker trips!)
        res2 = reject_task(
            task_id="TASK-300",
            reason="Still fails when list contains nulls",
            severity=SEVERITY_BLOCKER,
            test_file="tests/test_null.py",
            base_dir=self.root,
        )
        self.assertEqual(res2["status"], "CIRCUIT_BREAKER_TRIGGERED")
        self.assertEqual(res2["reject_count"], 2)
        self.assertEqual(res2["stage"], STAGE_ESCALATION)

        # Check task moved to 05_escalation
        found = find_task("TASK-300", base_dir=self.root)
        p, meta, body = found
        self.assertIn("05_escalation", str(p))

        # Check baton transferred to orchestrator for arbitration
        baton = get_baton(base_dir=self.root)
        self.assertEqual(baton["holder"], "orchestrator")
        self.assertEqual(baton["action"], "arbitrate_dispute")


if __name__ == "__main__":
    unittest.main()
