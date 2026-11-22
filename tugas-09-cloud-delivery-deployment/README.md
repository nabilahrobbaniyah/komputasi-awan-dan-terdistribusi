# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

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
1. Hybrid Cloud: Hybrid Cloud merupakan model cloud yang menggabungkan Private Cloud dan Public Cloud. Pada sistem data kependudukan, Private Cloud digunakan untuk menyimpan dan mengelola data sensitif warga, sedangkan Public Cloud dapat digunakan untuk komponen yang tidak menyimpan data pribadi sensitif.
   Alasan pemilihan:
- Kerahasiaan data: Data nama, NIK, alamat, dan biometrik disimpan di Private Cloud yang infrastrukturnya dikendalikan oleh pemerintah.
- Skalabilitas: Public Cloud dapat dimanfaatkan untuk menangani lonjakan akses pada layanan non-sensitif, misalnya portal informasi atau halaman pengecekan status.
- Fleksibilitas: Pemerintah dapat menentukan komponen mana yang ditempatkan di Private Cloud dan mana yang dapat memanfaatkan Public Cloud.
- Efisiensi: Sumber daya cloud dapat disesuaikan dengan kebutuhan beban kerja tanpa harus menyediakan seluruh kapasitas secara maksimal sejak awal.
Hubungan dengan karakteristik NIST:
Karakteristik NIST	: Penerapan pada Sistem Data Kependudukan
On-demand self-service:	Admin dapat menambah sumber daya komputasi atau penyimpanan sesuai kebutuhan tanpa proses pengadaan perangkat setiap kali dibutuhkan.
Broad network access:	Sistem dapat diakses oleh instansi berwenang melalui jaringan yang aman dari berbagai lokasi.
Resource pooling:	Sumber daya Private Cloud digunakan bersama oleh berbagai instansi melalui mekanisme resource pooling dengan isolasi tenant, pembatasan hak akses berbasis peran (RBAC), serta alokasi sumber daya yang terkontrol sehingga data setiap instansi tetap terlindungi.
Rapid elasticity:	Kapasitas dapat ditingkatkan ketika terjadi lonjakan akses, misalnya saat pemilu atau pendaftaran sekolah.
Measured service:	Penggunaan CPU, memori, penyimpanan, dan bandwidth dapat dipantau untuk membantu pengelolaan kapasitas dan efisiensi.

2. Service Model yang digunakan dapat berbeda pada setiap komponen sistem.
Komponen	Service Model	Alasan:
Database data kependudukan:	IaaS	Pemerintah memiliki kontrol terhadap server, sistem operasi, konfigurasi keamanan, penyimpanan, dan database.
Backend API dan aplikasi layanan:	PaaS	Memudahkan pengembangan, deployment, pemeliharaan aplikasi, serta pengelolaan runtime tanpa harus mengelola seluruh infrastruktur server.
Portal layanan instansi:	PaaS	Aplikasi dapat dikembangkan dan diskalakan sesuai jumlah pengguna serta kebutuhan layanan.
Email dan kolaborasi internal:	SaaS	Dapat memanfaatkan aplikasi siap pakai untuk mendukung administrasi internal, selama memenuhi kebijakan keamanan pemerintah.

3. Risiko: Sinkronisasi data antara Private dan Public Cloud. penjelasannya: Perbedaan data atau keterlambatan sinkronisasi dapat menyebabkan informasi yang ditampilkan tidak sesuai.
   Mitigasi: Data sensitif tetap berada di Private Cloud. Sinkronisasi hanya dilakukan terhadap data yang diperlukan dan telah disaring, menggunakan API aman serta mekanisme validasi.
   Risiko: Serangan siber dan kebocoran data. Penjelasannya: Sistem yang terhubung ke banyak instansi dan jaringan berpotensi menjadi target serangan.
   Mitigasi: Menerapkan enkripsi data, autentikasi multifaktor, kontrol akses berbasis peran, firewall, audit log, serta monitoring keamanan
   Risiko: Lonjakan akses menyebabkan gangguan layanan. Penjelasannya: Banyak instansi mengakses sistem secara bersamaan, terutama saat pemilu atau pendaftaran sekolah.
   Mitigasi: Menerapkan autoscaling pada komponen yang memungkinkan, load balancing, monitoring kapasitas, serta menyediakan cadangan sumber daya.

 4. Public Cloud murni kurang tepat untuk sistem data kependudukan karena seluruh infrastruktur dikelola penyedia cloud. Pemerintah memiliki keterbatasan kontrol langsung       terhadap infrastruktur dibandingkan Private Cloud.

      Data kependudukan bersifat sangat rahasia dan mencakup informasi pribadi serta biometrik. Oleh karena itu, menempatkan seluruh database inti pada Public Cloud murni         berpotensi menimbulkan risiko terkait kendali infrastruktur, keamanan, dan kepatuhan terhadap kebijakan pengelolaan data pemerintah.

      Hybrid Cloud lebih sesuai karena data sensitif tetap dikelola di Private Cloud, sementara komponen non-sensitif dapat memanfaatkan skalabilitas Public Cloud.
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
