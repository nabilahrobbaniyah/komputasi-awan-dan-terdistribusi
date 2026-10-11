```python
"""
Tugas 4 - Jalur B: Publisher (simulasi modul Pembayaran)
Pastikan `docker compose up -d` sudah jalan sebelum menjalankan file ini.
"""

import pika
import json
import time

QUEUE_NAME = "pembayaran_berhasil"


def main():
    # TODO 1: koneksi ke RabbitMQ dan membuat channel
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # TODO 2: deklarasikan queue durable
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    for i in range(1, 4):
        pesan = {
            "user_id": f"user{i}",
            "jumlah": 20000 * i,
            "timestamp": time.time(),
        }

        # TODO 3: publish pesan ke queue
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(pesan),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f"Event terkirim: {pesan}")
        time.sleep(1)

    # TODO 4: tutup koneksi
    connection.close()
    print("Publisher selesai mengirim event.")


if __name__ == "__main__":
    main()
```
