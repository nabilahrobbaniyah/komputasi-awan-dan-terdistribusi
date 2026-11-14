# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: Eventual Consistency memungkinkan replikasi data antarserver berlangsung secara bertahap, tetapi dapat menyebabkan data yang dibaca belum diperbarui. Dalam kasus FoodGo, hal ini berisiko menyebabkan pelanggan mendapatkan informasi saldo yang tidak sesuai setelah melakukan top up. Sequential Consistency lebih sesuai karena operasi pembaruan dan pembacaan perlu mengikuti urutan yang konsisten. Selain itu, Read-Your-Writes dapat digunakan agar pelanggan dapat langsung membaca hasil pembaruan yang telah dilakukannya
- Kesimpulan akhir & alasan: Memilih Sequential Consistency karena data saldo e-wallet berkaitan langsung dengan transaksi keuangan sehingga harus konsisten. Read-Your-Writes digunakan sebagai solusi tambahan agar pelanggan dapat membaca data terbaru setelah melakukan top up, meskipun replikasi ke server lain belum selesai

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: Pada skenario naif, setelah pelanggan melakukan top up sebesar Rp50.000 di Jakarta, server Bandung masih membaca saldo Rp0 karena proses replikasi membutuhkan waktu 2 detik. Hal ini menunjukkan terjadinya stale read. Pada skenario Read-Your-Writes, pelanggan melakukan top up tambahan sebesar Rp20.000 sehingga saldo di Jakarta menjadi Rp70.000. Karena versi data Bandung masih versi 1, sistem mengarahkan pembacaan ke server Jakarta yang sudah memiliki versi 2. Hasilnya, pelanggan berhasil mendapatkan saldo terbaru sebesar Rp70.000. Setelah proses replikasi selesai, saldo di Bandung juga diperbarui menjadi Rp70.000.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 14-November 2026 | ChatGpt | Membantu memahami pemilihan model konsistensi pada kasus saldo e-wallet FoodGo dan simulasi Read-Your-Writes menggunakan Python | Memberikan penjelasan mengenai Sequential Consistency, Eventual Consistency, Read-Your-Writes, serta bantuan penyusunan dan perbaikan kode simulasi | Kode dijalankan dan diuji secara mandiri melalui VS Code. Hasil output diperiksa untuk memahami perbedaan pembacaan saldo sebelum dan sesudah penerapan Read-Your-Writes. Penjelasan jurnal disesuaikan dengan hasil pengujian |
