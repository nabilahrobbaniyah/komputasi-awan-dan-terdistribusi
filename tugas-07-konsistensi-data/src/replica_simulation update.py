
"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(
            f"[{self.name}] WRITE saldo {user_id} = "
            f"{saldo_baru} (versi {version})"
        )

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float):
        """Top-up ditulis terlebih dahulu ke server Jakarta."""
        self.version_counter += 1
        version = self.version_counter

        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: Replikasi ke Bandung setelah delay.
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version)
        )
        timer.start()

        print(
            f"[SISTEM] Replikasi ke Bandung dijadwalkan "
            f"{REPLICATION_DELAY} detik lagi."
        )

        return version

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo tanpa Read-Your-Writes."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(
        self, user_id: str, server: str, versi_minimal: int
    ) -> float:
        """Memastikan pelanggan membaca saldo dengan versi minimal."""

        replica = self.jakarta if server == "Jakarta" else self.bandung

        versi_sekarang = replica.last_write_version.get(user_id, 0)

        if versi_sekarang < versi_minimal:
            print(
                f"[SISTEM] Versi {server} masih {versi_sekarang}. "
                "Menggunakan server Jakarta untuk membaca data terbaru."
            )
            replica = self.jakarta

        saldo = replica.read(user_id)

        print(
            f"[{replica.name}] Read-Your-Writes: "
            f"saldo {user_id} = {saldo}, "
            f"versi {replica.last_write_version.get(user_id, 0)}"
        )

        return saldo


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")

    versi_pertama = system.top_up(user_id, 50000)

    time.sleep(0.5)

    print(
        "Baca saldo dari Bandung (naif):",
        system.baca_saldo_naif(user_id, "Bandung")
    )
    print("-> Seharusnya 50000, tetapi Bandung masih membaca 0 (BUG).")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")

    versi_terakhir = system.top_up(user_id, 20000)

    # Langsung membaca dari Bandung meskipun replikasi belum selesai.
    saldo = system.baca_saldo_read_your_writes(
        user_id,
        "Bandung",
        versi_terakhir
    )

    print("Saldo yang diterima pelanggan:", saldo)
    print("-> Saldo benar karena sistem membaca versi terbaru.")

    # Tunggu agar proses timer selesai sebelum program berakhir.
    time.sleep(REPLICATION_DELAY + 0.5)


if __name__ == "__main__":
    main()
