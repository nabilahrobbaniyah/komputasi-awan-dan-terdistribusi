"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")  # ganti dengan xmlrpc.client.ServerProxy(...)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    respons = time.time() - start

    print(f"saldo user1: Rp. {saldo:,.0f}")
    print(f"waktu respons: {respons:.4f}")
    print("respons diterima")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    hasil = proxy.proses_pembayaran("user1", 2000)
    print(f"status: {hasil['status']}")
    print(f"saldo akhir: Rp. {hasil['saldo_akhir']:,.0f}")

    saldo_akhir = proxy.cek_saldo("user1")
    print(f"\nverifikasi saldo user1: Rp. {saldo_akhir:,.0f}")

if __name__ == "__main__":
    main()
