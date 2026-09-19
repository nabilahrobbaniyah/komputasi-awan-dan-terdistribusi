# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 4

| Nama | NIM | Kontribusi |
|---|---|---|
| Nabilah Robbaniyah | 103072400092 | The network is reliable |
| Kholifa Ayu Lestari | 103072400114 | Latency is zero |
| Afiya Nadifa Febianti | 103072400036 | Monolik & Single Point of Failure |

## Pitfall 1: The network is Reliable — ditulis oleh Nabilah Robbaniyah

**Bukti di skenario:** Ada asumsi dalam kode "# network is always reliable, no need for retry" yang ditulis tim engineering FoodGo. Tidak memakai timeout sama sekali pada pemanggilan antar modul

**Kenapa ini keliru:** di sistem terdistribusi, jaringan fisik tidak pernah 100% handal

**Dampak ke FoodGo:** Ketika pemanggilan ke modul pembayaran mengalami kegagalan koneksi atau hambatan, modul pesanan akan ketahan selamanya

**Solusi desain awal:** memakai mekanisme Timeout, sehingga ada batas waktu maksimal menunggu respons. menggunakan Retry with exponential backoff dan jitter, agar tidak membebankan jaringan, percobaan ulang berkala dikombinasikan dengan variasi waktu acak. circuit Breaker Pattern bisa untuk memutus aliran panggilan secara otomatis jika service downstream terdeteksi mengalami kegagalan berulang

**Trade-off:** melakukan retry tanpa pengaturan yang tepat justru bisa menambah beban jaringan dan memicu masalah thundering herd atau bahkan cascading failure. penerapan timeout untuk mempercepat kegagalan transaksi (fail-fast) membuat aplikasi harus mampu mengelola status pesanan secara lebih hati-hati, terutama melalui mekanisme idempotency serta kompensasi transaksi

---

## Pitfall 2: Latency is zero — ditulis oleh Kholifa Ayu Lestari

**Bukti di skenario:** pada studi kasus FoodGo, terdapat kondisi ketika modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu (timeout). hal tersebut menunjukkan sistem tidak memperhitungkan adanya kemungkinan adanya keterlambatan dalam komunikasi antara service.

ketika jumlah pesanan meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout. kondisi ini menunjukkan bahwa waktu yang dibutuhkan untuk komunikasi dan pemrosesan antar-service tidak selalu dapat dianggap nol.

**Kenapa ini keliru**: Asumsi "latency is zero berarti menganggap komunikasi antar-komponen atau antar-service dapat berlangsung secara langsung tanpa adanya keterlambatan. asumsi tersebut keliru dalam sistem terdistribusi karena komunikasi antar-service dilakukan melalui jaringan dan membutuhkan waktu.

latensi dapat dipengaruhi oleh berbagai kondisi, seperti peningkatan jumlah request, beban server, kondisi jaringan, maupun service yang sedang mengalami gangguan. Waktu respons suatu service juga tidak selalu sama dan dapat berubah sesuai kondisi sistem.

**Dampak ke FoodGo:** ketika modul pembayaran mengalami keterlambatan, modul pesanan akan tetap menunggu karena tidak memiliki batas waktu. jika kondisi tersebut terjadi pada banyak pesanan secara bersamaan, semakin banyak request yang tertahan.


**Solusi desain awal:** FoodGo perlu menerapkan timeout pada komunikasi antara modul pesanan dan pembayaran agar modul pesanan tidak menunggu tanpa batas waktu. Untuk proses yang tidak harus mendapatkan respons secara langsung, komunikasi asynchronous juga dapat digunakan agar beban pada server tidak menumpuk.

**Trade-off:** Penerapan timeout dapat mencegah request menunggu terlalu lama, tetapi jika waktu yang ditentukan terlalu singkat, request yang sebenarnya masih dapat berhasil bisa dianggap gagal. tetapi jika terlalu sering justru menambah beban server.

---

## Pitfall 3: Monolitik & Single Point of Failure — ditulis oleh Afiya Nadifa Febianti

**Bukti di skenario:** menyebutkan "satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama" dan "server backend kadang crash total dan perlu direstart manual" yang menunjukan modul-modul berbagi resource proses dan server yang sama sehingga beban tinggi pada satu bagian dapat memengaruhi bagian lainnya.

**Kenapa ini keliru:** dalam sistem terdistribusi, menempatkan banyak fungsi penting dalam satu proses dapat membuat modul-modul tersebut berbagi resource dan tidak memiliki isolasi kegagalan yang memadai. Ketika beban meningkat, penggunaan resource oleh satu bagian dapat memengaruhi bagian lainnya. Ketergantungan pada satu server juga membuat kegagalan server berpotensi menjadi Single Point of Failure karena beberapa fungsi dapat ikut terganggu ketika server tersebut gagal. 

**Dampak ke FoodGo:** ketika trafik meningkat, satu server harus menangani modul pesanan, pembayaran, dan notifikasi kurir secara bersamaan sehingga server menjadi kewalahan. Kondisi tersebut dapat menyebabkan aplikasi semakin lambat dan beberapa request mengalami timeout. Jika backend mengalami crash, beberapa modul yang berada dalam proses tersebut dapat ikut berhenti dan layanan membutuhkan restart manual untuk kembali berjalan.

**Solusi desain awal:** FoodGo dapat memulai memisahkan modul yang memiliki tanggung jawab berbeda menjadi service atau proses yang dapat diisolasi sehingga kegagalan atau beban tinggi pada satu bagian tidak langsung berdampak pada seluruh sistem. Resource isolation atau bulkhead dapat digunakan untuk membatasi dampak beban antarbagian, sedangkan beberapa instance untuk service penting dapat mengurangi ketergantungan pada satu server. Health check dan automatic restart juga dapat digunakan untuk membantu pemulihan ketika terjadi kegagalan.

**Trade-off:** pemisahan service dapat meningkatkan isolasi dan mengurangi ketergantungan pada satu proses, tetapi membuat sistem lebih kompleks karena komunikasi antar-service berlangsung melalui jaringan. FoodGo kemudian perlu menangani latency, kegagalan komunikasi, omnitoring, dan debugging antar-service yang sebelumnya lebih sederhana dalam aplikasi monolitik.


---

## Kesimpulan Kelompok

Ketiga pitfall menunjukan bahwa FoodGo membutuhkan arsitektur yang lebih decouple, memiliki isolasi antar-service, serta mampu menangani latency dan kegagalan komunikasi. Secara garis besar, modul Pesanan, Pembayaran, Kurir/Notifikasi, dan Katalog Resto dapat dipisahkan menjadi service dengan tanggung jawab masing-masing. Hasil ini menjadi dasar untuk Tugas 2, yaitu mempertimbangkan SOA sebagai gaya arsitektur utama untuk pemisahan service dan Publish-Subscribe untuk komunikasi berbasis event/asynchronus pada proses yang sesuai. Pemilihan tersebut tetap perlu dibahas kelompok berdasarkan kebutuhan FoodGo dan trade-off yang ditemukan pada Tugas 1.
