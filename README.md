# GitHub Auto Commit Harian — neixcyll

Bikin grafik kontribusi GitHub hijau tiap hari, otomatis, $0.
Sekarang 30x sehari. Dua cara — pilih salah satu, jangan dua-duanya
di repo yang sama (nanti dobel commit di hari yang sama).

## Cara 1 (paling gampang, disarankan): GitHub Actions

Tidak perlu laptop nyala. GitHub yang jalankan 30 commit langsung dalam satu
jalan pagi hari jam 07:00 WIB, dengan cadangan 07:30 dan 08:00 WIB kalau jalan
pertama kelewat. Sekali jalan, langsung 30 commit — nggak perlu nunggu
berjam-jam. (Jadwal tiap jam yang lama sering dibuang GitHub karena cron-nya
best-effort, jadi sekarang pakai satu jalan pagi + cadangan.)

1. Buat repo baru di GitHub, misal `daily-commits`, Public, centang Add README.
   - Harus Public, kalau Private grafiknya tidak kehitung kecuali kamu
     nyalakan "Include private contributions" di Settings > Profile.
   - Branch utama harus `main`.
2. Upload semua file di folder ini ke repo itu
   (pastikan folder `.github/workflows/daily-commit.yml` ikut ter-upload).
3. Buka tab **Actions** di repo itu, klik **Daily Auto Commit > Run workflow**
   untuk tes sekali — sekali tes langsung nambah 30 commit hari itu.
   Kalau hijau, jadwal paginya jalan sendiri.
4. Cek di profil https://github.com/neixcyll — kotak hari ini harus hijau paling gelap,
   karena 30 commit/hari.

Email commit sudah diset ke `224485812+neixcyll@users.noreply.github.com`
(email noreply resmi akunmu), jadi commit-nya kehitung di grafik.
Jangan ganti ke email lain yang tidak terverifikasi di GitHub.

## Cara 2: Script di laptop

Kalau kamu mau jalan dari laptop sendiri:

**Windows — Task Scheduler:**
1. Copy `daily_commit.py`, `activity-log.md`, `last-update.txt` ke folder repo kamu.
2. Task Scheduler > Create Task > 30 Trigger Daily — tiap jam :00 (24x) + 03:30, 07:30, 11:30, 15:30, 19:30, 23:30 (6x) > Action:
   `python` dengan argumen `C:\path\ke\repo\daily_commit.py`
3. Syarat: laptop nyala + internet + repo sudah `git push` pertama kali manual.

**Linux / Mac — cron (30x sehari: tiap jam + 6x setengah jam):**
```bash
# buka crontab
crontab -e
# tambah dua baris ini:
0 * * * * /usr/bin/python3 /path/ke/repo/daily_commit.py >> /tmp/daily-commit.log 2>&1
30 3,7,11,15,19,23 * * * /usr/bin/python3 /path/ke/repo/daily_commit.py >> /tmp/daily-commit.log 2>&1
```

Tes manual dulu:
```bash
python daily_commit.py
```

## Isi tanggal kosong yang lalu (opsional)

Kalau mau isi bolong-bolong lama, pakai `backfill.py` — baca dulu
peringatan di dalam file itu sebelum jalan.

```bash
# isi 90 hari terakhir yang belum ada commit
python backfill.py --days 90
# cek dulu, baru push
git log --oneline -20
git push
```

## Yang perlu kamu tahu (jujur)

- 30 commit/hari = 1 kotak hijau paling gelap (level maksimal). Warna makin gelap kalau commit
  makin banyak. 30x sehari itu kelihatan jelas otomatis kalau ada yang buka
  history-nya, karena isinya 30 commit sekaligus tiap pagi.
- Grafik hijau saja tidak bikin recruiter terkesan kalau isi commit-nya
  kosong. Yang mereka buka adalah repo beneran seperti OculiCare,
  PCM Piping Dashboard, dan CV kamu. Jadi pakai ini sebagai pelengkap,
  bukan pengganti kerjaan asli.
- Commit backfill ketahuan tanggal aslinya dari history — jangan dipakai
  untuk klaim pengalaman yang tidak ada.
- Jangan pasang auto-commit di repo kerjaan / repo orang lain / repo Askable.
  Pakai repo khusus seperti `daily-commits` saja.

## File di paket ini

- `.github/workflows/daily-commit.yml` — jadwal otomatis di GitHub
- `daily_commit.py` — script harian untuk laptop
- `backfill.py` — isi tanggal lama (opsional, ada konfirmasi YA)
- `activity-log.md` — file yang di-update tiap hari
- `last-update.txt` — penanda update terakhir
