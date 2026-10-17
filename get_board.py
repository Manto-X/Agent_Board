#!/usr/bin/env python3
"""
Agents_Board Zero-Install Bootstrap Installer
One-line command to install or update Agents_Board in any existing or new project:

Linux / macOS:
  curl -fsSL https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python3

Windows PowerShell:
  irm https://raw.githubusercontent.com/tomyxo/Agents_Board/main/get_board.py | python
"""

import io
import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO_ZIP_URL = "https://github.com/tomyxo/Agents_Board/archive/refs/heads/main.zip"


def bootstrap(target_dir: Path | None = None) -> None:
    dest = target_dir or Path.cwd()
    print(f"\n🚀 [Agents_Board Bootstrap] Installing into: {dest}")

    print("📥 Downloading template archive from GitHub...")
    try:
        req = urllib.request.Request(
            REPO_ZIP_URL,
            headers={"User-Agent": "Agents_Board_Bootstrap/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            zip_bytes = resp.read()
    except Exception as e:
        print(f"❌ Failed to download repository archive: {e}")
        print("💡 Hint: You can also clone the repository directly with: git clone https://github.com/tomyxo/Agents_Board.git")
        sys.exit(1)

    print("📦 Extracting .agents engine and configuration files...")
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        # Find prefix folder inside zip (e.g. Agents_Board-main/)
        prefix = None
        for name in zf.namelist():
            if "/" in name:
                prefix = name.split("/", 1)[0] + "/"
                break

        if not prefix:
            print("❌ Invalid archive structure.")
            sys.exit(1)

        # Files and directories to extract
        for member in zf.infolist():
            rel_name = member.filename[len(prefix):]
            if not rel_name:
                continue

            # We only extract .agents/ and the 4 root markdown files if not already present
            if rel_name.startswith(".agents/") or rel_name in ["AGENTS.md", "CLAUDE.md", "CODEX.md"]:
                target_path = dest / rel_name
                if member.is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
                else:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as src, open(target_path, "wb") as dst:
                        shutil.copyfileobj(src, dst)

    # Initialize board
    print("⚙️ Initializing workspace...")
    board_script = dest / ".agents" / "board.py"
    if board_script.exists():
        os.system(f'"{sys.executable}" "{board_script}" init')

    print("""
✨ [Agents_Board] Zero-Install Kit Ready!
--------------------------------------------------
Quick Commands:
  • Check Baton  : python .agents/board.py baton status
  • List Tasks   : python .agents/board.py task list
  • Run Watcher  : python .agents/board.py watch
--------------------------------------------------
""")


if __name__ == "__main__":
    bootstrap()
