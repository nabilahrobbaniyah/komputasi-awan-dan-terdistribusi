# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 4

| Nama | NIM | Kontribusi |
|---|---|---|
| Nabilah Robbaniyah | 103072400092 | The network is reliable |
| Kholifa Ayu Lestari | 103072400114 | Latency is zero |
| Afiya Nadifa Febianti | 1030724000 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: The network is Reliable — ditulis oleh Nabilah Robbaniyah

**Bukti di skenario:** Ada asumsi dalam kode "# network is always reliable, no need for retry" yang ditulis tim engineering FoodGo. Tidak memakai timeout sama sekali pada pemanggilan antar modul

**Kenapa ini keliru:** di sistem terdistribusi, jaringan fisik tidak pernah 100% handal

**Dampak ke FoodGo:** Ketika pemanggilan ke modul pembayaran mengalami kegagalan koneksi atau hambatan, modul pesanan akan ketahan selamanya

**Solusi desain awal:** memakai mekanisme Timeout, sehingga ada batas waktu maksimal menunggu respons

**Trade-off:** 

---

## Pitfall 2: Latency is zero — ditulis oleh Kholifa Ayu Lestari

**Bukti di skenario:** pada studi kasus FoodGo, terdapat kondisi ketika modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu (timeout). hal tersebut menunjukkan sistem tidak memperhitungkan adanya kemungkinan adanya keterlambatan dalam komunikasi antara service.

ketika jumlah pesanan meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout. kondisi ini menunjukkan bahwa waktu yang dibutuhkan untuk komunikasi dan pemrosesan antar-service tidak selalu dapat dianggap nol.

**Kenapa ini keliru**: Asumsi "latency is zero berarti menganggap komunikasi antar-komponen atau antar-service dapat berlangsung secara langsung tanpa adanya keterlambatan. asumsi tersebut keliru dalam sistem terdistribusi karena komunikasi antar-service dilakukan melalui jaringan dan membutuhkan waktu.

latensi dapat dipengaruhi oleh berbagai kondisi, seperti peningkatan jumlah request, beban server, kondisi jaringan, maupun service yang sedang mengalami gangguan. Waktu respons suatu service juga tidak selalu sama dan dapat berubah sesuai kondisi sistem.

**Dampak ke FoodGo:** ketika modul pembayaran mengalami keterlambatan, modul pesanan akan tetap menunggu karena tidak memiliki batas waktu. jika kondisi tersebut terjadi pada banyak pesanan secara bersamaan, semakin banyak request yang tertahan.


**Solusi desain awal:** FoodGo perlu menerapkan timeout pada komunikasi antara modul pesanan dan pembayaran agar modul pesanan tidak menunggu tanpa batas waktu. Jika terjadi kegagalan sementara, sistem dapat menggunakan retry secara terbatas dengan backoff. Untuk proses yang tidak harus mendapatkan respons secara langsung, komunikasi asynchronous juga dapat digunakan agar beban pada server tidak menumpuk.

**Trade-off:** Penerapan timeout dapat mencegah request menunggu terlalu lama, tetapi jika waktu yang ditentukan terlalu singkat, request yang sebenarnya masih dapat berhasil bisa dianggap gagal. Selain itu, penggunaan retry dapat membantu saat terjadi gangguan sementara, tetapi jika terlalu sering justru menambah beban server.

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
