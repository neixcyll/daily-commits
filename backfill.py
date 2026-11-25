#!/usr/bin/env python3
"""
Backfill: isi tanggal-tanggal kosong di masa lalu (OPSIONAL).

PENTING - baca dulu:
  - Ini bikin commit dengan tanggal lama (GIT_AUTHOR_DATE).
    Di halaman commit GitHub, tanggalnya kelihatan, dan siapa pun
    yang buka history bisa lihat semua commit dibuat di hari yang sama.
  - Recruiter / reviewer biasanya tidak nilai grafik hijau saja,
    mereka buka isi commit-nya. Kalau isinya cuma "daily activity"
    berulang, itu ketahuan kosong.
  - Pakai ini hanya kalau kamu memang mau isi bolong-bolong lama,
    dan tetap lanjutkan commit asli ke depannya.

Cara pakai:
  python backfill.py --days 90
    -> isi 90 hari terakhir yang belum ada commit (1 commit/hari)

  python backfill.py --start 2026-08-04 --end 2026-11-24
    -> isi rentang tanggal itu

  Jalankan dari dalam folder repo, di branch utama.
  Setelah selesai: git push
"""
import argparse
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
GIT_NAME = "neixcyll"
GIT_EMAIL = "224485812+neixcyll@users.noreply.github.com"


def run(cmd, env=None, check=True):
    import os
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True, env=full_env)
    if check and result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"Gagal: {' '.join(cmd)}")
    return result


def has_commit_on(day: date) -> bool:
    result = run(
        ["git", "log", "--since", f"{day} 00:00", "--until", f"{day} 23:59", "--oneline"],
        check=False,
    )
    return bool(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=0, help="Jumlah hari ke belakang dari kemarin")
    parser.add_argument("--start", type=str, help="YYYY-MM-DD")
    parser.add_argument("--end", type=str, help="YYYY-MM-DD, default kemarin")
    args = parser.parse_args()

    today = date.today()
    if args.days:
        end = today - timedelta(days=1)
        start = end - timedelta(days=args.days - 1)
    elif args.start:
        start = date.fromisoformat(args.start)
        end = date.fromisoformat(args.end) if args.end else today - timedelta(days=1)
    else:
        parser.error("Pakai --days N atau --start YYYY-MM-DD")

    if start > end:
        raise SystemExit("Tanggal start harus sebelum end.")

    print(f"Backfill {start} sampai {end}")
    print("Ketik YA untuk lanjut: ", end="")
    if input().strip() != "YA":
        print("Dibatalkan.")
        return

    run(["git", "config", "user.name", GIT_NAME])
    run(["git", "config", "user.email", GIT_EMAIL])

    log_file = REPO_DIR / "activity-log.md"
    made = skipped = 0

    day = start
    while day <= end:
        if has_commit_on(day):
            print(f"{day}: sudah ada commit, skip")
            skipped += 1
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"- {day} - daily activity (backfill)\n")
            (REPO_DIR / "last-update.txt").write_text(f"Last update: {day}\n", encoding="utf-8")
            # Commit jam 09:00 WIB = 02:00 UTC
            commit_time = f"{day}T02:00:00+00:00"
            env = {
                "GIT_AUTHOR_DATE": commit_time,
                "GIT_COMMITTER_DATE": commit_time,
            }
            run(["git", "add", "activity-log.md", "last-update.txt"])
            run(["git", "commit", "-m", f"chore: daily activity {day}"], env=env)
            print(f"{day}: commit dibuat")
            made += 1
        day += timedelta(days=1)

    print(f"\nSelesai: {made} commit baru, {skipped} hari di-skip.")
    print("Cek dulu dengan: git log --oneline --graph -20")
    print("Kalau sudah yakin, baru: git push")


if __name__ == "__main__":
    main()
