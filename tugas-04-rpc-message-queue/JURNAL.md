# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- keduanya/hybrid (RPC dan MQ), alasan: kebutuhan berbeda-beda, ada bagian yang cocok dengan dengan sinkron, ada yang lebih cocok pakai asinkron. 
- Cek_saldo, cocok menggunakan sinkron karena modul pesanan butuh jawaban seketika sebelum pesanan bisa dibuat. jika menggunakan asinkron seperti MQ akan menambah kompleksitas yang tidak perlu, modul peasanan harus menunggu balasan sebelum ke proses berikutnya
- notifikasi kurir, cocok menggunakan asinkron kareana modul pembayaran tidak boleh tertahan hanya karena modul kurir sedang sibuk, lambat, atau down. jika menggunakan sinkron seperti RPC ketika modul kurir down atau lambat, thread modul pembayaran akan menumpuk dan memicu cascading failure atau timeout chaining ke seluruh sistem

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): Pada awal pengujian, program publisher.py mengalami pika.exceptions.AMQPConnectionError karena RabbitMQ belum berjalan atau belum dapat diakses. Selain itu, terdapat kendala saat menentukan lokasi interpreter Python dan menjalankan file dari folder yang benar.
- penyelesaian: Memilih interpreter Python yang sesuai, memasang library pika, menjalankan Docker Desktop, dan menjalankan RabbitMQ menggunakan perintah docker compose up -d. Setelah RabbitMQ berjalan, program publisher berhasil terhubung.
- hasil akhir: Publisher berhasil mengirim pesan dan consumer berhasil memproses pesan dari antrean RabbitMQ.
  (untuk gambar buktinya ada di file bukti)

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
  Consumer dihentikan menggunakan Ctrl + C, kemudian publisher dijalankan sebanyak dua kali sehingga mengirimkan total enam pesan. Setelah itu, antrean pembayaran_berhasil diperiksa melalui dashboard RabbitMQ di http://localhost:15672. Selama consumer berhenti, dashboard menunjukkan Ready: 6. Consumer kemudian dijalankan kembali untuk memproses pesan yang tersimpan.
- Hasil yang diamati: Enam pesan tetap berada dalam antrean ketika consumer tidak aktif. Setelah consumer dijalankan kembali, pesan-pesan diproses dan jumlah pesan yang menunggu berubah menjadi Ready: 0. Hasil ini menunjukkan bahwa pesan dapat tetap tersimpan di antrean dan diproses ketika consumer kembali aktif.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11-10-2026 | ChatGPT | meminta penjelasan alur pengerjaan Tugas 4 jalur B menggunakan RabbitMQ | Mendapat penjelasan urutan menjalankan RabbitMQ, publisher, dan consumer serta cara menguji antrean | Mengikuti alur pengujian, menjalankan program, dan mengamati hasilnya sendiri. |
