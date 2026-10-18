# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Saat mengirim pesan "ELECTION" ke node ber-ID lebih tinggi yang sedang mati, program sempat mengalami hanging (memblokir eksekusi)

## Skenario 1: Start normal
- Leader yang terpilih: node 5
- Log/observasi: saat seluruh node (1–5) dinyalakan hampir bersamaan, Node 5 mencoba mengirim "ELECTION" ke node yang ber-ID lebih tinggi darinya. Karena Node 5 adalah ID tertinggi, tidak ada node yang membalas "OK". Node 5 kemudian mem-broadcast "COORDINATOR" ke Node 1, 2, 3, dan 4

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: node 4
- Berapa lama waktu sampai leader baru terdeteksi: sekitar 11.43s

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oct | gpt | membantu menyusun outline atau struktur kode untuk mengimplementasikan algoritma leader election menggunakan mekanisme pengiriman pesan ELECTION, penerimaan OK, dan penentuan COORDINATOR | menyarankan struktur proses pemilihan pemimpin, yaitu mencegah pemilihan berjalan secara bersamaan menggunakan lock, mengatur status pemilihan, mengirim pesan ELECTION ke node dengan ID lebih tinggi, menunggu respons OK, dan menentukan pemimpin jika tidak ada respons dalam batas waktu tertentu | saya menggunakan saran sebagai panduan untuk menyusun alur algoritma, kemudian menyesuaikannya dengan struktur program yang saya gunakan. Saya mengimplementasikan pengiriman pesan ke node dengan ID lebih tinggi, mekanisme menunggu respons OK menggunakan event dan timeout, serta pemanggilan fungsi declare_leader() utuk menentukan pemimpin. Saya juga menggunakan lock untuk mengelola status pemilihan |