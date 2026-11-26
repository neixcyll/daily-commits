#!/usr/bin/env python3
"""
Auto commit 30x sehari - versi laptop (Windows / Linux / Mac)
Cara pakai:
  1. Copy file ini ke folder repo kamu
  2. Jalankan sekali:  python daily_commit.py
  3. Pasang jadwal otomatis (lihat README.md)

Yang dilakukan script ini:
  - Tambah 1 baris ke activity-log.md + update last-update.txt
  - git add, git commit, git push ke branch utama
  - Maksimal 30 commit per hari; kalau sudah 30, dia berhenti.
    Jadi jadwalkan 30x sehari (tiap jam + 6x setengah jam), bukan 1x.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_DIR = Path(__file__).resolve().parent
WIB = ZoneInfo("Asia/Jakarta")

# Ganti kalau email GitHub kamu beda.
# Yang ini (noreply) sudah benar untuk akun neixcyll, id 224485812.
GIT_NAME = "neixcyll"
GIT_EMAIL = "224485812+neixcyll@users.noreply.github.com"


def run(cmd, check=True):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(f"Gagal: {' '.join(cmd)}")
    return result


def main():
    now = datetime.now(WIB)
    today = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y-%m-%d %H:%M WIB")

    # 1. Cek: sudah berapa commit hari ini? Maksimal 30.
    log = run(["git", "log", "--since", f"{today} 00:00", "--oneline"], check=False)
    count_today = len([line for line in log.stdout.splitlines() if line.strip()])
    if count_today >= 30:
        print(f"Sudah {count_today} commit hari ini ({today}), coba push dulu kalau ada yang belum ke-push.")
        run(["git", "push"], check=False)
        print("Skip, sudah 30x hari ini.")
        return
    print(f"Commit ke-{count_today + 1} hari ini ({today}).")

    # 2. Update file
    log_file = REPO_DIR / "activity-log.md"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"- {stamp} - daily activity\n")

    (REPO_DIR / "last-update.txt").write_text(f"Last update: {stamp}\n", encoding="utf-8")

    # 3. Commit & push
    run(["git", "config", "user.name", GIT_NAME])
    run(["git", "config", "user.email", GIT_EMAIL])
    run(["git", "add", "activity-log.md", "last-update.txt"])
    run(["git", "commit", "-m", f"chore: daily activity {today}"])
    run(["git", "push"])
    print(f"Selesai, commit {today} sudah ke-push.")


if __name__ == "__main__":
    main()
