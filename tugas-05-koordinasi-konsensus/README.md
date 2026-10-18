# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Tugas Analisis
- Masalah Jam Fisik(Clock Drift & Skew). Pada sistem terdistribusi, jam fisik antar-server tidak akan pernah sinkron secara sempurna (terdapat skew/drift). Jika dua server pesanan (Server A dan Server B) menggunakan jam lokal mereka, pesanan yang masuk di Server B dapat memiliki stempel waktu lebih tinggi daripada Server A meskipun secara waktu nyata terjadi setelahnya.
Peran Leader: Menetapkan Total Ordering. Dengan menunjuk satu Node Leader sebagai pengelola antrean pesanan pusat, seluruh pesanan dapat diurutkan berdasarkan urutan penerimaan di Leader (atau nomor urut transaksi tunggal), sehingga konflik urutan dapat dikurangi dan risiko pemrosesan ganda (double processing) dapat diminimalkan melalui mekanisme pencegahan duplikasi transaksi
- Bully Algorithm sesuai untuk kasus ini karena tujan utamanya memahami proses pemilihan pemimpin dan pemilihan ulang ketika leader gagal. Raft lebih tepat jika FoodGo perlu menjamin bahwa perubahan antrean pesanan direplikasi secara konsisten di antara beberapa server. Bully menentukan siapa yang menjadi leader, tetapi tidaka menjamin kesepakatan atas seluruh urutan transaksi
- skenario 1: kelima node dijalankan hampir bersamaan. Setiap node memulai proses election dan mengirim pesan ELECTION kepada node yang memiliki ID lebih tinggi. Node dengan ID lebih tinggi yang masih aktif memberikan balasan OK, kemudian menjalankan election sendiri.
Node 5 tidak memiliki node dengan ID lebih tinggi. Node 5 dapat menyatakan dirinya sebagai leader dan mengirim pesan COORDINATOR kepada node lainnya. Hal ini menunjukkan bahwa pemilihan leader mengikuti prioritas ID tertinggi yang aktif
- skenario 2: setelah Node 5 dihentikan menggunakan Ctrl+C, node lain mendeteksi bahwa leader tidak lagi bisa dihubungi. Node yang mendeteksi kegagalan memulai election baru dengan mengirim pesan ELECTION kepada node yang memiliki ID lebih tinggi.
Karena Node 5 sudah tidak aktif, Node 4 tidak memperoleh balasan dari node dengan ID lebih tinggi. Setelah batas waktu election berakhir, Node 4 menyatakan dirinya sebagai leader baru dan mengirim pesan COORDINATOR kepada node lain yang masih aktif. Node-node yang masih berjalan memperbarui informasi leader menjadi Node 4

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
