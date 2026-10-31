
"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Simulasi pemetaan ID Kurir ke alamat IP menggunakan Chord DHT.
"""

import hashlib

M_BITS = 8
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string ke ruang identifier 0-255."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id -> alamat IP node
        self.nodes: dict[int, str] = {}

        # hash kurir -> (kurir_id, ip_kurir)
        self.data: dict[int, tuple[str, str]] = {}

    def find_successor(self, key_hash: int) -> int:
        """Mencari node successor berdasarkan aturan Chord."""
        if not self.nodes:
            raise ValueError("Ring kosong")

        sorted_nodes = sorted(self.nodes.keys())

        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        # Wrap-around ke node dengan ID terkecil.
        return sorted_nodes[0]

    def join(self, node_name: str, node_ip: str):
        """Menambahkan node baru dan mencatat perpindahan tanggung jawab."""
        node_id = hash_id(node_name)

        if node_id in self.nodes:
            print(f"Node '{node_name}' sudah ada di ring")
            return

        # Catat pemilik lama setiap mapping sebelum node bergabung.
        old_owners = {}

        for key_hash in self.data:
            if self.nodes:
                old_owners[key_hash] = self.find_successor(key_hash)

        # Tambahkan node baru.
        self.nodes[node_id] = node_ip

        print(
            f"\nNode '{node_name}' bergabung "
            f"(ID={node_id}, IP={node_ip})"
        )

        # Periksa apakah ada mapping yang berpindah ke node baru.
        for key_hash, old_owner in old_owners.items():
            new_owner = self.find_successor(key_hash)

            if new_owner == node_id:
                kurir_id, ip_kurir = self.data[key_hash]

                print(
                    f"Mapping {kurir_id} ({ip_kurir}) "
                    f"pindah dari node ID={old_owner} "
                    f"ke node baru ID={node_id}"
                )

        print("Node aktif:", sorted(self.nodes.keys()))

    def leave(self, node_name: str):
        """Mengeluarkan node dan mencatat perpindahan mapping."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"Node '{node_name}' tidak ditemukan")
            return

        # Catat mapping yang sebelumnya menjadi tanggung jawab node ini.
        old_data = {}

        for key_hash, value in self.data.items():
            if self.find_successor(key_hash) == node_id:
                old_data[key_hash] = value

        # Hapus node dari ring.
        del self.nodes[node_id]

        print(
            f"\nNode '{node_name}' (ID={node_id}) keluar dari ring"
        )

        # Cari pemilik baru untuk mapping yang ditinggalkan.
        if self.nodes:
            for key_hash, (kurir_id, ip_kurir) in old_data.items():
                new_successor = self.find_successor(key_hash)

                print(
                    f"Mapping {kurir_id} ({ip_kurir}) "
                    f"pindah ke node ID={new_successor}"
                )
        elif old_data:
            print("Tidak ada node tersisa untuk mengambil alih mapping.")

        print("Node aktif:", sorted(self.nodes.keys()))

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Mendaftarkan ID Kurir dan alamat IP-nya."""
        key_hash = hash_id(kurir_id)

        owner_id = self.find_successor(key_hash)

        self.data[key_hash] = (kurir_id, ip_kurir)

        print(
            f"{kurir_id} -> {ip_kurir}, "
            f"disimpan oleh node ID={owner_id}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Mencari alamat IP berdasarkan ID Kurir."""
        key_hash = hash_id(kurir_id)

        # Tentukan node yang bertanggung jawab.
        owner_id = self.find_successor(key_hash)

        entry = self.data.get(key_hash)

        if entry is not None and entry[0] == kurir_id:
            print(
                f"Lookup {kurir_id}: "
                f"ditemukan di node ID={owner_id}"
            )
            return entry[1]

        print(f"Lookup {kurir_id}: data tidak ditemukan")
        return None


def main():
    ring = ChordRing()

    print("=== SIMULASI CHORD DHT FOODGO ===")

    # Skenario awal: empat node bergabung.
    print("\n--- Node bergabung ---")

    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")
    

    # Daftarkan beberapa kurir.
    print("\n--- Registrasi kurir ---")

    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-011", "192.168.1.20")

    # Lookup sebelum perubahan topologi.
    print("\n--- Lookup sebelum perubahan topologi ---")

    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    # Node baru bergabung.
    print("\n--- Node baru bergabung ---")

    ring.join("node-medan-1", "10.0.0.5")

    print("kurir-001 ->", ring.lookup("kurir-001"))

    # Sebuah node keluar.
    print("\n--- Sebuah node keluar ---")

    ring.leave("node-surabaya-1")

    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))



if __name__ == "__main__":
    main()
