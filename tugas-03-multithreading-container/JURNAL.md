# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 35 (dari target 100 pesanan)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Melesetnya nilai counter terjadi karena fenomena race condition. Ketika multiple thread berjalan secara bersamaan, beberapa thread membaca nilai processed_count yang sama di memori sebelum thread lain sempat memperbaruinya. Saat proses penambahan (processed_count + 1) selesai, thread-thread tersebut menimpa nilai satu sama lain secara acak. Akibatnya, banyak operasi penambahan pesanan yang hilang atau terabaikan sehingga hasil akhir jauh di bawah 100.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 (dari target 100 pesanan)

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya:
  Kendala: Docker Desktop belum berjalan atau daemon Docker belum aktif di latar belakang saat menjalankan perintah, menghasilkan pesan error cannot connect to the Docker daemon.
  Cara perbaiki: Memastikan aplikasi Docker Desktop sudah dibuka dan status servicenya aktif (running) sebelum mengeksekusi perintah docker build` dan docker run di terminal.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 4 Oct | GPT | membanatu menyusun outline/struktur kode untuk menjalankan beberapa chunk data secara paralel menggunakan threading | menyarankan membagi data menjadi beberapa chunk, kemudian membuat satu thread untuk setiap chunk. Setiap thread menjalankan fungsi tertentu untuk memproses chunk masing-masing. Thread yang dibuat kemudian disimpan dalam sebuah list agar dapat dikelola dan dijalankan | saya memahami konsep pembagian data menjadi beberapa chunk dan pemrosesan secara paralel. Berdasarkan ide tersebut, saya menyesuaikan implementasinya dengan program saya sendiri |
