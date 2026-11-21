<p align="center">
  <img src="assets/ecoledger_darling_logo.png" alt="Logo EcoLedger Darling" width="220">
</p>

# EcoLedger Darling

**Aplikasi Pengelolaan Bank Sampah Berbasis Web pada Bank Sampah Darling Berseri**

Proyek UTS mata kuliah **Sains Data Industri**, Program Studi Sains Data,
Institut Teknologi Sains Bandung (ITSB), Semester 3 (Ganjil 2026/2027).
Disusun oleh **Kelompok 11**.

## Kelengkapan UTS
| No | Ketentuan | Keterangan |
|---|---|---|
| 1 | Link aplikasi (Streamlit), status **deployed** | https://ecoledger-darling-demo.streamlit.app |
| 2 | Repository GitHub (public) | Repository ini |
| 3 | Proposal | [`Proposal_EcoLedger_Darling_Kelompok_11.docx`](Proposal_EcoLedger_Darling_Kelompok_11.docx) |
| 4 | Slide presentasi | [`Slide_Presentasi_Kelompok_11.pptx`](Slide_Presentasi_Kelompok_11.pptx) |
| 5 | Hasil wawancara (Word) | [`Hasil_Wawancara_Kelompok_11.docx`](Hasil_Wawancara_Kelompok_11.docx) |
| 6 | Source code | [`app.py`](app.py) |
| 7 | URL swimlane diagram | https://swimlanes.io/u/FxU2YbX8tN |
| 8 | Logo aplikasi | [`assets/ecoledger_darling_logo.png`](assets/ecoledger_darling_logo.png) |

## Tim
| No | Nama | NIM |
|---|---|---|
| 1 | Safina Zahra | 52250033 |
| 2 | Nakeisha Aulia Zahra | 52250023 |
| 3 | Jihan Ramadhani Deandri | 52250024 |
| 4 | Naila Syahrani Putri | 52250070 |
| 5 | Dameria Adelina Simarmata | 52250071 |

**Mitra:** Bank Sampah Darling Berseri, Perum Griya Hegar Asri, Cikarang Pusat,
Kabupaten Bekasi, Jawa Barat (narasumber: Pak Aris, Pengurus).

## Latar Belakang
Bank sampah menerima setoran sampah dari nasabah, memilahnya berdasarkan jenis,
lalu menjualnya kembali kepada pengepul. Berdasarkan wawancara dengan Pak Aris
pada 18 Oktober 2026, pencatatan setoran di Bank Sampah Darling Berseri masih
manual menggunakan buku: sampah ditimbang, hasilnya ditulis, lalu nilai setoran
dihitung dengan mengalikan berat dan harga tiap jenis. Cara ini memakan waktu,
rawan salah hitung, dan menyulitkan penelusuran riwayat, stok, serta penyusunan
laporan.

EcoLedger Darling mencatat proses tersebut secara digital, dari setoran sampai
laporan.

## Permasalahan yang Diidentifikasi
1. Pencatatan manual dan rawan salah hitung
2. Riwayat nasabah sulit dicari
3. Penyusunan laporan memakan waktu
4. Harga sampah berubah tanpa riwayat
5. Kas dan laba belum terhitung otomatis

## Tujuan
- Menghitung nilai setoran otomatis dari jenis, berat, dan harga sampah
- Menyimpan transaksi, saldo, dan stok secara terstruktur
- Menyediakan rekap dan laporan per periode
- Menyediakan aplikasi online (deployed) dengan dokumentasi di GitHub publik

## Pengguna
| Peran | Tugas |
|---|---|
| Pengurus | Menimbang dan menginput setoran, memproses penarikan, mencatat penjualan dan pengeluaran, mengelola stok, harga, akun, dan laporan |
| Nasabah | Menyetorkan sampah, memeriksa saldo dan riwayat, menyetujui setoran, dan mengajukan penarikan |
| Pengepul | Pembeli sampah yang dicatat pada transaksi penjualan |

## Fitur
- **Beranda:** ringkasan kas bulan ini, pembelian dari nasabah, penjualan ke pengepul, pengeluaran operasional, dan analitik setoran
- **Input dan Kelola Setoran:** memilih jenis sampah dan jumlah, metode **Tabung** (masuk saldo) atau **Tunai**, total dihitung otomatis, dengan persetujuan nasabah
- **Nasabah dan Penarikan Saldo:** saldo dan riwayat nasabah, pengajuan penarikan yang dikonfirmasi pengurus
- **Penjualan Pengepul dan Pengeluaran Operasional:** pencatatan penjualan dan biaya operasional untuk menghitung kas dan laba
- **Stok Sampah:** stok per jenis, bertambah dari setoran dan berkurang saat dijual
- **Jenis Sampah dan Harga:** pengaturan harga dengan riwayat perubahan harga
- **Data Pengguna:** pembuatan akun dan pengaturan peran
- **Laporan:** rekap berdasarkan rentang tanggal, dapat diunduh sebagai CSV (dibuka di Excel), serta cadangan data JSON

## Teknologi
| Kebutuhan | Tools |
|---|---|
| Aplikasi | Python dan Streamlit |
| Pengolahan data | Pandas |
| Visualisasi | Plotly |
| Penyimpanan data | PostgreSQL di Neon (SQLite sebagai cadangan untuk pemakaian lokal) |
| Pemodelan proses | Swimlanes.io |
| Editor kode | Visual Studio Code |
| Version control | Git dan GitHub |
| Deployment | Streamlit Community Cloud |

## Cara Menjalankan di Komputer
1. Pasang Python.
2. Pasang kebutuhan: `pip install -r requirements.txt`
3. Jalankan: `streamlit run app.py`
4. Buka alamat yang muncul di terminal, lalu buat akun Pengurus pertama.

Secara bawaan, aplikasi memakai SQLite lokal (`data/banksampah.db`) saat dijalankan
di komputer. Untuk memakai database Postgres, isi variabel `DATABASE_URL` pada
`.streamlit/secrets.toml` (contohnya ada di `.streamlit/secrets.toml.example`).
Berkas `secrets.toml` tidak boleh diunggah ke GitHub.

## Struktur Repository
- `app.py`: source code aplikasi
- `demo_data.py`: pembangun data simulasi untuk Mode Demo
- `panduan.py`: isi Panduan Penggunaan (per peran dan per halaman)
- `tests/uji_fitur.py`: uji fungsional (fitur lama, Mode Demo, Panduan)
- `requirements.txt`: daftar pustaka
- `assets/`: logo aplikasi EcoLedger Darling
- `.streamlit/`: pengaturan tema dan contoh pengaturan rahasia
- `Proposal_EcoLedger_Darling_Kelompok_11.docx`: proposal proyek
- `Slide_Presentasi_Kelompok_11.pptx`: slide presentasi
- `Hasil_Wawancara_Kelompok_11.docx`: hasil wawancara

## Catatan
- Pada versi yang di-deploy, data disimpan di database Postgres (Neon), sehingga
  tidak hilang ketika aplikasi dimulai ulang. Menu Pengaturan menyediakan unduhan
  cadangan data (JSON, tanpa kata sandi).
- Informasi koneksi database disimpan di Secrets Streamlit, bukan di repository.
- Data pada tahap pengujian berupa data contoh agar data pribadi nasabah terlindungi.

## Mode Demo
Di halaman login tersedia tombol **Masuk sebagai Demo** (tanpa email, kata sandi, atau pendaftaran).
- Memakai data simulasi yang dibuat baru untuk setiap sesi, terpisah dari data asli. Data asli tidak dibaca dan tidak ditulis oleh sesi demo.
- Pengguna dapat berpindah tampilan **Pengurus / Nasabah / Pengepul** lewat pilihan *Lihat tampilan sebagai* di bagian atas halaman, mencoba setoran, persetujuan, penarikan, dan penjualan, lalu melihat dashboard dan laporan.
- Tombol *Atur ulang data demo* mengembalikan data simulasi ke kondisi awal.

## Panduan Penggunaan
- Menu **Panduan Penggunaan** tersedia untuk semua peran (juga lewat tombol di Profil Saya / Pengaturan).
- Tombol **Panduan Halaman Ini** di bagian atas setiap halaman membuka penjelasan khusus halaman yang sedang dibuka.
- Pengepul hanya melihat panduan Pengepul; Nasabah hanya panduan Nasabah; Pengurus melihat ketiganya.

## Menjalankan Uji
`python tests/uji_fitur.py` (memakai SQLite sementara, tidak menyentuh data asli).
