# 🚗 Smart Parking Automation with YOLOv8 and OpenCV

Proyek ini adalah sistem **otomatisasi parkir pintar** berbasis kamera dan AI, yang menggunakan **YOLOv8** dan **OpenCV** untuk mendeteksi status spot parkir secara real-time. Sistem ini dapat membedakan apakah spot parkir kosong, diisi mobil, atau tidak valid, lalu mengirimkan data tersebut ke server melalui API dan menampilkannya dalam antarmuka web menggunakan Flask.

---

## 📌 Fitur Utama

- 🚙 Deteksi kendaraan secara real-time dengan YOLOv8.
- ✅ Status spot parkir: `empty`, `occupied`, atau `warning`.
- 🔄 Pengiriman status ke server melalui API.
- 🖥️ Tampilan web streaming live video dan status spot.
- 🌐 Support akses publik via **Cloudflared Tunnel**.

---

## 🔧 Teknologi yang Digunakan

- Python 3
- OpenCV
- YOLOv8 (Ultralytics)
- Flask
- Pickle
- Requests
- Cloudflared

---

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/Rama0surya/CarPark_Detection.git
