# Jurnal Proses — Tugas 2

## 26 September
- Opsi arsitektur yang dipertimbangkan: Kobinasi SOA dengan pub-sub
- Kenapa akhirnya pilih [SOA/Pub-Sub]: SOA dipakai untuk memisahkan fungsi bisnis menjadi service yang independen dan pub-sub untuk pemrosesan transaksi lanjutan yang butuh keterhubungan longgar (decoupled). Karena critical path (pembuatan pesanan) dan proses asyncrhronous (seperti pembayaran, notifikasi restp, penugasan kurir) terpisah, ini bisa mengurangi risiko cascading failure dan timeout berantai akibat modul yang saling menunggu: Kami memilih kombinasi SOA dan Pub-Sub karena SOA dapat memisahkan fungsi FoodGo menjadi beberapa service yang lebih independen. Sementara itu, Pub-Sub digunakan untuk proses yang tidak harus menunggu respons langsung, seperti notifikasi dan penugasan kurir. Dengan pemisahan ini, service tidak terlalu bergantung satu sama lain sehingga dapat mengurangi risiko cascading failure dan timeout berantai ketika salah satu service mengalami masalah.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Menambahkan pemisahan komunikasi sinkron dan asinkron. Service Pesanan menggunakan request-response untuk proses yang membutuhkan respons langsung, sedangkan proses notifikasi dan penugasan kurir menggunakan Pub-Sub melalui Message Broker agar service lebih decoupled.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26 September | ChatGPT | Mencari alternatif arsitektur untuk FoodGo | Memberikan ide SOA dan kombinasi SOA dengan Pub-Sub | Ide dibandingkan dan dipilih berdasarkan kebutuhan sistem melalui diskusi kelompok |
