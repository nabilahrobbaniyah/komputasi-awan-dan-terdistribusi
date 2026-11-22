# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mul Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.
2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS) yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).
3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).
4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

**JAWAB**
1. Hybrid Cloud: Hybrid Cloud merupakan model cloud yang menggabungkan dua atau lebih infrastruktur cloud yang berbeda, seperti Private Cloud dan Public Cloud, yang tetap memiliki karakteristik masing-masing tetapi dihubungkan melalui mekanisme integrasi yang memungkinkan pertukaran data dan portabilitas aplikasi. Pada sistem data kependudukan, Private Cloud digunakan untuk menyimpan dan mengelola data sensitif warga, sedangkan Public Cloud dapat digunakan untuk komponen yang tidak menyimpan data pribadi sensitif.
   Alasan pemilihan:
- Kerahasiaan data: Data nama, NIK, alamat, dan biometrik disimpan di Private Cloud yang dimiliki atau dioperasikan pemerintah dengan kendali yang jelas terhadap lokasi penyimpanan, infrastruktur, akses operasional, dan pengelolaan data sesuai kebijakan kedaulatan data.
- Skalabilitas: Public Cloud dapat dimanfaatkan untuk menangani lonjakan akses pada layanan non-sensitif, misalnya portal informasi umum dan distribusi konten statis, sedangkan pengecekan status yang melibatkan NIK tetap diproses melalui Private Cloud.
- Fleksibilitas: Pemerintah dapat menentukan komponen mana yang ditempatkan di Private Cloud dan mana yang dapat memanfaatkan Public Cloud. Pemisahan antara Private Cloud dan Public Cloud dilakukan berdasarkan klasifikasi data. Data sensitif seperti NIK, alamat, dan biometrik tetap berada di lingkungan Private Cloud. Public Cloud hanya digunakan untuk komponen non-sensitif, seperti portal informasi umum dan distribusi konten statis, sedangkan layanan pengecekan status yang melibatkan data pribadi diproses melalui Private Cloud. Komunikasi antarkeduanya dilakukan melalui API Gateway yang dilengkapi autentikasi dan enkripsi.
- Efisiensi: Sumber daya cloud dapat disesuaikan dengan kebutuhan beban kerja tanpa harus menyediakan seluruh kapasitas secara maksimal sejak awal.
Hubungan dengan karakteristik NIST:
Karakteristik NIST	: Penerapan pada Sistem Data Kependudukan
On-demand self-service:	Administrator dapat melakukan provisioning sumber daya komputasi dan penyimpanan secara mandiri melalui portal atau antarmuka manajemen cloud tanpa memerlukan interaksi langsung dengan penyedia layanan.
Broad network access:	Sistem menyediakan akses melalui mekanisme jaringan standar yang dapat digunakan oleh berbagai instansi pemerintah dari lokasi berbeda. Akses dilakukan melalui antarmuka web dan API dengan autentikasi, otorisasi, serta pembatasan hak akses berdasarkan kewenangan masing-masing instansi.
Resource pooling:	Resource pooling diterapkan dengan menggabungkan sumber daya komputasi, penyimpanan, dan jaringan dalam satu infrastruktur Private Cloud untuk melayani berbagai instansi. Sumber daya dialokasikan secara dinamis sesuai kebutuhan pengguna melalui mekanisme multi-tenant. Pemisahan tenant dan isolasi sumber daya diterapkan agar penggunaan bersama tidak menyebabkan akses tidak sah terhadap data instansi lain.
Rapid elasticity: misalnya saat pemilu atau pendaftaran sekolah, ketika terjadi lonjakan akses, kapasitas komputasi dapat ditingkatkan melalui autoscaling selama kapasitas fisik Private Cloud masih mencukupi, sedangkan kebutuhan tambahan dapat ditangani melalui Public Cloud untuk komponen non-sensitif. Setelah beban menurun, kapasitas dapat dikurangi kembali agar penggunaan sumber daya tetap efisien
Measured service:	Penggunaan CPU, memori, penyimpanan, dan bandwidth diukur serta dipantau secara otomatis untuk mendukung pengendalian kapasitas, transparansi penggunaan, dan efisiensi operasional.

2. Service Model yang digunakan dapat berbeda pada setiap komponen sistem.
Komponen	Service Model	Alasan:
Database data kependudukan:	IaaS	apabila pemerintah ingin mengelola sendiri sistem operasi, perangkat lunak database, konfigurasi keamanan, backup, enkripsi, dan kontrol akses, dengan pengelolaan infrastruktur fisik tetap menjadi tanggung jawab penyedia cloud jika menggunakan penyedia eksternal. Namun, pengelolaan infrastruktur fisik tetap menjadi tanggung jawab penyedia layanan cloud apabila menggunakan penyedia eksternal.
Backend API dan aplikasi layanan:	PaaS	Memudahkan pengembangan, deployment, pemeliharaan aplikasi, serta pengelolaan runtime tanpa harus mengelola seluruh infrastruktur server.
Portal layanan instansi:	Portal layanan instansi menggunakan PaaS yang ditempatkan pada lingkungan Private Cloud atau platform yang telah memenuhi persyaratan keamanan pemerintah. Portal menyediakan akses bagi instansi berwenang melalui API dengan autentikasi, otorisasi, dan pembatasan data berdasarkan kewenangan masing-masing instansi.
Email dan kolaborasi internal:	SaaS	Dapat memanfaatkan aplikasi siap pakai untuk mendukung administrasi internal, selama memenuhi kebijakan keamanan pemerintah.

3. Risiko: Sinkronisasi data antara Private dan Public Cloud. penjelasannya: Perbedaan data atau keterlambatan sinkronisasi dapat menyebabkan informasi yang ditampilkan tidak sesuai.
   Mitigasi: Data sensitif tetap berada di Private Cloud. Pertukaran data dilakukan seminimal mungkin melalui API yang aman dan terkontrol. Jika komponen Public Cloud membutuhkan informasi tertentu, gunakan data agregat atau anonim yang tidak memungkinkan identifikasi warga. Terapkan validasi integritas, enkripsi komunikasi, API Gateway, rate limiting, serta mekanisme pencatatan dan pemantauan pertukaran data.
   Risiko: Serangan siber dan kebocoran data. Penjelasannya: Sistem kependudukan yang menyediakan API untuk ribuan instansi berpotensi mengalami serangan seperti pencurian kredensial, penyalahgunaan hak akses, API abuse, dan kebocoran NIK maupun data biometrik.
   Mitigasi: Menerapkan enkripsi data saat disimpan dan ditransmisikan, autentikasi multifaktor, kontrol akses berbasis peran, mutual TLS untuk komunikasi antarsistem, pembatasan permintaan API, audit log, serta monitoring keamanan
   Risiko: Lonjakan akses menyebabkan gangguan layanan. Penjelasannya: Banyak instansi mengakses sistem secara bersamaan, terutama saat pemilu atau pendaftaran sekolah.
   Mitigasi: Menerapkan autoscaling pada komponen aplikasi sesuai kapasitas infrastruktur Private Cloud yang tersedia, load balancing, caching untuk informasi non-sensitif, monitoring kapasitas, capacity planning, serta menyediakan redundansi infrastruktur dan disaster recovery untuk menjaga ketersediaan layanan. Database inti juga perlu dirancang agar mampu menangani permintaan bersamaan melalui optimasi query, connection pooling, dan mekanisme replikasi yang sesuai.

 4. Public Cloud murni kurang tepat karena pemerintah tidak memiliki kendali langsung terhadap infrastruktur fisik yang dikelola penyedia layanan. Meskipun penyedia menerapkan mekanisme keamanan, model shared responsibility tetap menempatkan sebagian tanggung jawab keamanan, konfigurasi, dan pengelolaan data pada pemerintah. Pemerintah memiliki keterbatasan kontrol langsung       terhadap infrastruktur dibandingkan Private Cloud.

      Data kependudukan bersifat sangat rahasia dan mencakup informasi pribadi serta biometrik. Oleh karena itu, menempatkan seluruh database inti pada Public Cloud murni         berpotensi menimbulkan risiko terkait kendali infrastruktur, keamanan, dan kepatuhan terhadap kebijakan pengelolaan data pemerintah.

      Hybrid Cloud lebih sesuai karena data sensitif tetap dikelola di Private Cloud, sementara komponen non-sensitif dapat memanfaatkan skalabilitas Public Cloud.

skenario jika pemerintah daerah tidak memiliki infrastruktur Private Cloud sendiri. Pemerintah pusat dapat menyediakan Private Cloud terpusat yang dikelola oleh lembaga pemerintah yang berwenang. Pemerintah daerah mengakses sistem melalui jaringan yang aman dan API sesuai hak akses masing-masing. Dengan demikian, setiap daerah tidak harus membangun infrastruktur cloud sendiri, sementara data kependudukan tetap berada dalam lingkungan yang dikendalikan pemerintah dengan dukungan redundansi, backup, dan disaster recovery untuk menjamin ketersediaan layanan.

## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.
