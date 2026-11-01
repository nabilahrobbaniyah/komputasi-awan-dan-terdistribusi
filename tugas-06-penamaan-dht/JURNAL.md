# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Pada awalnya, pencarian successor perlu memperhatikan kondisi ketika hash kurir lebih besar daripada seluruh ID node yang ada. Jika kondisi ini tidak ditangani, fungsi tidak menemukan node penanggung jawab meskipun ring bersifat melingkar.
- Cara memperbaikinya: Node diurutkan berdasarkan ID hash. Fungsi memilih node dengan ID terkecil yang lebih besar atau sama dengan hash kurir. Jika tidak ada node yang memenuhi kondisi tersebut, fungsi melakukan *wrap-around* dengan memilih node ber-ID terkecil dalam ring.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Sebelum node Medan bergabung, node aktif adalah `[40, 102, 136, 177]`. Setelah node Medan dengan ID 123 bergabung, node aktif menjadi `[40, 102, 123, 136, 177]`. Berdasarkan output, lookup kurir-001 tetap menemukan IP `192.168.1.10` pada node ID 102.
- Hasil sebelum & sesudah node keluar: Sebelum node Jakarta-1 dengan ID 177 keluar, ring terdiri atas node ID 40, 102, 123, 136, dan 177. Setelah node Jakarta-1 keluar, ring terdiri atas node ID 40, 102, 123, dan 136. Berdasarkan output, tidak ada mapping yang sebelumnya menjadi tanggung jawab node ID 177. Oleh karena itu, tidak terjadi perpindahan mapping. Lookup kurir-001 dan kurir-002 tetap berhasil mengembalikan alamat IP masing-masing.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 31 Oktober| ChatGpt | Meminta bantuan memahami dan memperbaiki simulasi Chord DHT, menjelaskan output join/leave, serta menyusun bagian analisis dan jurnal proses | AI menjelaskan aturan successor dan wrap-around, serta membantu menginterpretasikan perpindahan tanggung jawab mapping saat node bergabung atau keluar. AI juga memberikan contoh kode dan draf penjelasan. | Saya membandingkan saran dengan kode dan output simulasi yang saya jalankan. Namun, karena AI juga membantu kode dan teks akhir, penggunaan ini melampaui batas Level 2 yang tercantum di rubrik. |
