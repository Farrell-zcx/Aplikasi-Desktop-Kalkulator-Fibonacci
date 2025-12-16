# Analisis Kompleksitas Algoritma: Fibonacci Calculator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

Aplikasi desktop ini dibangun untuk memenuhi **Tugas Besar Mata Kuliah Analisis Kompleksitas Algoritma**. Tujuan utamanya adalah mendemonstrasikan secara empiris perbedaan efisiensi yang drastis antara pendekatan **Rekursif ($O(2^n)$)** dan **Iteratif ($O(n)$)** dalam menyelesaikan deret Fibonacci.

## 📋 Deskripsi Masalah
Deret Fibonacci adalah kasus klasik dalam ilmu komputer.
* **Pendekatan Rekursif Naif** mendefinisikan $F(n) = F(n-1) + F(n-2)$. Meskipun kodenya singkat, pendekatan ini melakukan perhitungan ulang (redundant) yang menyebabkan kompleksitas waktu eksponensial.
* **Pendekatan Iteratif** menggunakan metode *bottom-up* dengan menyimpan dua nilai terakhir, menghasilkan kompleksitas waktu linear yang jauh lebih efisien.

Aplikasi ini memvisualisasikan perbedaan "Waktu Nyata" (Real Execution Time) antara kedua algoritma tersebut.

## ✨ Fitur Aplikasi

### 1. Kalkulator Perbandingan (Single Test)
* Menginput satu nilai $N$ untuk melihat hasil perhitungan dan waktu eksekusi kedua algoritma secara bersamaan.
* **Fitur Keamanan:** Terdapat peringatan otomatis (Warning Box) jika pengguna mencoba menghitung $N > 40$ menggunakan metode rekursif untuk mencegah aplikasi *Not Responding*.

### 2. Analisis Grafik (Benchmarking)
* **Visualisasi Data:** Menggunakan library `matplotlib` untuk menggambar grafik garis perbandingan waktu.
* **Parameter Kustom:**
    * *Max N Rekursif:* Batas atas pengujian rekursif (Default: 32).
    * *Max N Iteratif:* Batas atas pengujian iteratif (Default: 1000).
* **Skala Logaritmik:** Opsi untuk mengubah sumbu Y menjadi skala logaritmik agar perbedaan orde pertumbuhan terlihat lebih jelas.

## 🛠️ Arsitektur & Teknis Kode

Aplikasi ini dirancang dengan mempertimbangkan responsivitas UI:

* **GUI Framework:** Menggunakan `customtkinter` untuk antarmuka modern dengan tema gelap (Dark Mode).
* **Multithreading:** Proses kalkulasi berat (terutama rekursif) dijalankan pada *Thread* terpisah menggunakan modul `threading`. Hal ini memastikan antarmuka aplikasi tidak *freeze* atau macet saat sedang menghitung angka yang besar.
* **Recursion Limit:** Kode secara otomatis meningkatkan batas rekursi Python (`sys.setrecursionlimit(20000)`) pada file `fibonacci_logic.py` untuk memungkinkan pengujian iteratif pada angka yang sangat besar tanpa error *Maximum recursion depth exceeded*.

## 📂 Struktur File

* `main.py`: Entry point aplikasi. Mengatur logika GUI, Multithreading, dan integrasi Grafik.
* `fibonacci_logic.py`: Berisi implementasi murni algoritma Rekursif dan Iteratif serta fungsi pengukuran waktu presisi (`time.perf_counter`).
* `requirements.txt`: Daftar pustaka eksternal yang dibutuhkan.

## 🚀 Panduan Instalasi & Penggunaan

### Prasyarat
Pastikan Python 3.x sudah terinstall di komputer Anda.

### Langkah Instalasi
1.  **Clone Repository** ini (atau ekstrak folder project).
2.  **Install Dependensi** melalui terminal/command prompt:
    ```bash
    pip install -r requirements.txt
    ```

### Cara Menjalankan
Jalankan perintah berikut di terminal:
```bash
python main.py
