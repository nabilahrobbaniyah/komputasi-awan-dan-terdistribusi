# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

**JAWAB:**
1. Kasus saldo e-wallet FoodGo lebih membutuhkan Sequential Consistency dibandingkan hanya Eventual Consistency.

Alasannya, saldo e-wallet berhubungan langsung dengan transaksi keuangan pelanggan. Ketika pelanggan melakukan top-up melalui server Jakarta, perubahan saldo harus diperhitungkan saat pelanggan melakukan pemesanan melalui server Bandung.

Jika sistem hanya menggunakan Eventual Consistency, pembaruan saldo memang akan diteruskan ke seluruh replika, tetapi proses tersebut membutuhkan waktu. Akibatnya, server Bandung mungkin masih membaca saldo lama sehingga transaksi pelanggan ditolak meskipun saldo sebenarnya sudah mencukupi.

Hal ini dapat menimbulkan beberapa dampak bisnis, seperti:
- Pelanggan tidak dapat melakukan pemesanan meskipun saldo mencukupi.
- Pelanggan kehilangan kepercayaan terhadap layanan FoodGo.
- Muncul keluhan dan pengalaman pengguna yang buruk.
- Berpotensi menimbulkan kesalahan dalam pencatatan transaksi.
Berbeda dengan jumlah like di media sosial yang masih dapat menerima keterlambatan pembaruan, data saldo e-wallet harus dijaga konsistensinya karena berkaitan dengan uang pelanggan.

2. Selain Sequential Consistency, FoodGo dapat menerapkan pendekatan Read-Your-Writes sebagai solusi tambahan.

Read-Your-Writes memastikan pelanggan dapat membaca hasil pembaruan data yang sebelumnya dilakukan oleh dirinya sendiri.

Cara kerjanya:
1. Pelanggan melakukan top-up melalui server Jakarta.
2. Server Jakarta memperbarui saldo dan menghasilkan versi data terbaru.
3. Sistem menyimpan informasi versi terbaru yang telah diterima pelanggan.
4. Ketika pelanggan membaca saldo melalui server Bandung, sistem memeriksa versi data yang tersedia.
5. Jika versi Bandung masih lebih lama, sistem mengarahkan pembacaan ke server Jakarta atau menunggu hingga replika Bandung memiliki versi yang sesuai.
6. Pelanggan mendapatkan saldo terbaru sehingga tidak mengalami penolakan transaksi akibat data yang belum diperbarui.

3. **Skenario tanpa jaminan konsistensi (bug terjadi):**
   Pada skenario ini, server Jakarta berhasil memperbarui saldo pelanggan. Namun, sebelum proses replikasi selesai, pelanggan melakukan pemesanan melalui server Bandung. Server Bandung masih membaca saldo lama sehingga transaksi ditolak
   

```mermaid
sequenceDiagram
    actor P as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung
    participant R as Proses Replikasi

    P->>J: Top-up saldo Rp50.000
    J->>J: Perbarui saldo menjadi Rp50.000
    J-->>P: Top-up berhasil
    J->>R: Kirim perubahan saldo
    Note over R,B: Replikasi masih tertunda

    P->>B: Memesan makanan
    B->>B: Membaca saldo pelanggan
    Note over B: Saldo masih Rp0
    B-->>P: Transaksi ditolak
    Note over P,B: BUG - Saldo belum diperbarui

    R->>B: Replikasi saldo Rp50.000
    B->>B: Perbarui data saldo
    Note over J,B: Kedua replika akhirnya konsisten


**Skenario dengan Read-Your-Writes (bug teratasi)**
Pada skenario ini, sistem memeriksa versi data sebelum memberikan saldo kepada pelanggan. Jika server Bandung belum memiliki versi terbaru, sistem mengarahkan pembacaan ke server Jakarta

```text
```mermaid
sequenceDiagram
    actor P as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung
    participant R as Proses Replikasi

    P->>J: Top-up saldo Rp50.000
    J->>J: Perbarui saldo Rp50.000 (versi 1)
    J-->>P: Top-up berhasil (versi 1)
    J->>R: Kirim perubahan saldo
    Note over R,B: Replikasi masih tertunda

    P->>B: Memesan makanan
    B->>B: Periksa versi data lokal
    Note over B: Versi Bandung masih 0

    B->>J: Minta saldo minimal versi 1
    J-->>B: Kirim saldo Rp50.000 (versi 1)
    B-->>P: Saldo terbaru Rp50.000
    Note over P,B: Read-Your-Writes terpenuhi

    R->>B: Replikasi saldo Rp50.000 (versi 1)
    B->>B: Perbarui saldo dan versi data
    Note over J,B: Replika Bandung sudah diperbarui



### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
