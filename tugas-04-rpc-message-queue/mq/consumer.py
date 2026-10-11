```python
"""
Tugas 4 - Jalur B: Consumer (simulasi modul Kurir/Notifikasi)
"""

import pika
import json

QUEUE_NAME = "pembayaran_berhasil"


def callback(ch, method, properties, body):
    pesan = json.loads(body)

    print(
        f"Kurir menerima notifikasi pembayaran untuk "
        f"{pesan['user_id']} sejumlah Rp{pesan['jumlah']}"
    )

    # Konfirmasi bahwa pesan berhasil diproses
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Gunakan antrean yang sama dengan publisher
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    # Proses satu pesan pada satu waktu
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print(
        "Menunggu event dari antrean "
        "'pembayaran_berhasil'... (Ctrl+C untuk berhenti)"
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()
```
