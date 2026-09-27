# Jurnal Proses — Tugas 2

## 26 September
- Opsi arsitektur yang dipertimbangkan: Kobinasi SOA dengan pub-sub
- Kenapa akhirnya pilih [SOA/Pub-Sub]: SOA dipakai untuk memisahkan fungsi bisnis menjadi service yang independen dan pub-sub untuk pemrosesan transaksi lanjutan yang butuh keterhubungan longgar (decoupled). Karena critical path (pembuatan pesanan) dan proses asyncrhronous (seperti pembayaran, notifikasi restp, penugasan kurir) terpisah, ini bisa mengurangi risiko cascading failure dan timeout berantai akibat modul yang saling menunggu
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
