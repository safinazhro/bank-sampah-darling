"""Isi Panduan Penggunaan EcoLedger Darling.

Satu sumber isi dipakai di dua tempat:
  1. menu "Panduan Penggunaan" (lengkap, per peran), dan
  2. tombol "Panduan Halaman Ini" (hanya halaman yang sedang dibuka).

Nama menu, tombol, dan status di sini mengikuti tulisan yang tampil di aplikasi.
Panduan Pengepul sengaja tidak menyebut harga beli dari nasabah, saldo nasabah,
ataupun kas Pengurus, karena Pengepul tidak punya akses ke informasi tersebut.
"""


def G(fungsi, siapa, siapkan, elemen, langkah, setelah, berhasil, kendala, catatan=""):
    return dict(fungsi=fungsi, siapa=siapa, siapkan=siapkan, elemen=elemen, langkah=langkah,
                setelah=setelah, berhasil=berhasil, kendala=kendala, catatan=catatan)


# =====================================================================
# PANDUAN PENGURUS
# =====================================================================
PENGURUS = {
    "Beranda": G(
        "Menampilkan ringkasan kas dan aktivitas Bank Sampah untuk bulan berjalan. Halaman ini diberi judul Ringkasan Dashboard.",
        "Pengurus.",
        ["Tidak ada yang perlu disiapkan. Angka muncul otomatis setelah ada setoran yang disetujui, penjualan ke pengepul, atau pengeluaran."],
        [("Pengajuan penarikan saldo (kotak kuning)", "Muncul hanya jika ada pengajuan dari nasabah. Berisi nama, nominal, waktu pengajuan, saldo, dan status. Diperbarui sendiri setiap 15 detik. Tombol Buka pengajuan penarikan membawa Anda ke menu Penarikan Saldo."),
         ("Net Kas Bulan Ini", "Penjualan ke pengepul dikurangi pembelian dari nasabah dan pengeluaran operasional, khusus bulan ini. Bisa negatif jika belum ada penjualan."),
         ("Pembelian dari Nasabah", "Total nilai setoran yang sudah disetujui bulan ini, baik Tabung maupun Tunai, beserta jumlah setorannya."),
         ("Penjualan ke Pengepul", "Total penjualan yang masih berstatus Aktif bulan ini."),
         ("Pengeluaran Operasional", "Total biaya yang dicatat bulan ini."),
         ("Keterangan Bulan lalu", "Perbandingan dengan bulan lalu. Hanya tampil jika bulan lalu ada data."),
         ("Operasional", "Tiga kotak: jumlah setoran bulan ini, jumlah setoran Menunggu persetujuan (ada label perlu tindakan bila tidak nol), dan jumlah nasabah terdaftar."),
         ("Analitik Setoran", "Pilih periode Bulan ini, 30 hari, atau Semua. Grafik kiri: berat setoran per hari. Grafik kanan: komposisi berat per jenis sampah. Barang berasatuan pcs tidak ikut grafik berat."),
         ("Aktivitas Terbaru", "Enam kegiatan terakhir (setoran, penarikan, penjualan, pengeluaran) beserta nilai dan statusnya."),
         ("Menunggu Persetujuan", "Setoran yang belum disetujui nasabah. Tombol Kelola setoran membuka menu Kelola Setoran.")],
        ["Buka Beranda setiap kali mulai bertugas.",
         "Lihat kotak kuning di atas. Jika ada pengajuan penarikan, klik Buka pengajuan penarikan.",
         "Baca empat kartu kas untuk mengetahui kondisi bulan ini.",
         "Periksa kotak Menunggu persetujuan. Jika ada, klik Kelola setoran dan ingatkan nasabah untuk menyetujui.",
         "Pilih periode pada Analitik Setoran untuk melihat grafik yang Anda perlukan."],
        ["Memilih periode grafik langsung memperbarui kedua grafik.", "Tombol pada halaman ini hanya berpindah halaman; tidak ada data yang diubah."],
        ["Angka kartu sama dengan hasil menu Laporan untuk periode yang sama.", "Grafik tampil dengan judul Berat setoran per hari dan Komposisi per jenis."],
        [("Grafik kosong dengan tulisan Belum ada transaksi pada periode ini", "Belum ada setoran yang disetujui pada periode itu. Coba pilih Semua."),
         ("Net Kas bernilai negatif", "Pembelian dan pengeluaran bulan ini lebih besar dari penjualan. Ini wajar jika stok belum dijual ke pengepul."),
         ("Angka belum berubah setelah transaksi baru", "Muat ulang halaman atau pindah menu lalu kembali ke Beranda.")]),

    "Input Setoran": G(
        "Mencatat sampah yang baru ditimbang dari seorang nasabah. Nilai setoran dihitung otomatis dari jenis, berat, dan harga.",
        "Pengurus.",
        ["Nasabah sudah punya akun Nasabah yang aktif (dibuat di menu Data Pengguna).",
         "Jenis sampah dan harga sudah benar di menu Jenis Sampah & Harga.",
         "Sampah sudah ditimbang dan beratnya dicatat."],
        [("Nasabah yang dilayani", "Pilih nama nasabah pemilik setoran."),
         ("Metode", "Tabung: nilai masuk ke saldo tabungan nasabah. Tunai: nilai dibayar langsung dan tidak menambah saldo. Keduanya menambah stok."),
         ("Baris Rincian sampah", "Setiap baris berisi Jenis (pilih dari daftar), Jumlah (kg atau pcs, boleh desimal), keterangan harga dan subtotal otomatis, dan tombol Hapus."),
         ("Tambah baris", "Menambah satu baris jenis sampah lagi."),
         ("Jenis baru", "Membuka kotak kecil untuk menambah jenis yang belum ada: isi Nama jenis sampah, pilih Satuan, isi Harga beli dari nasabah, lalu Simpan atau Batal."),
         ("Total setoran", "Jumlah semua subtotal, dihitung otomatis."),
         ("Persetujuan nasabah", "Nasabah setuju di lokasi: nasabah menyetujui di depan Anda, wajib mencentang kotak Rincian sudah ditunjukkan dan nasabah menyatakan setuju. Nasabah setuju lewat akunnya: nasabah menyetujui nanti dari akunnya sendiri."),
         ("Simpan & Setujui / Simpan & Kirim ke Nasabah", "Tombol simpan. Namanya mengikuti cara persetujuan yang dipilih.")],
        ["Buka menu Input Setoran.",
         "Pilih nama nasabah pada Nasabah yang dilayani.",
         "Pilih Metode: Tabung atau Tunai.",
         "Pada baris pertama, pilih Jenis lalu isi Jumlah sesuai timbangan.",
         "Klik Tambah baris untuk jenis berikutnya. Ulangi sampai semua sampah tercatat. Gunakan Hapus untuk membuang baris yang salah.",
         "Periksa angka Total setoran bersama nasabah.",
         "Pilih cara persetujuan. Jika di lokasi, tunjukkan rincian lalu centang pernyataan setuju.",
         "Klik Simpan & Setujui atau Simpan & Kirim ke Nasabah."],
        ["Setuju di lokasi: setoran langsung berstatus Disetujui. Stok bertambah, dan saldo nasabah bertambah jika metodenya Tabung.",
         "Setuju lewat akun: setoran berstatus Menunggu. Saldo dan stok belum bertambah sampai nasabah menyetujui.",
         "Muncul ringkasan transaksi. Klik Selesaikan & Input Nasabah Berikutnya untuk mulai setoran baru."],
        ["Muncul pesan hijau Transaksi # tersimpan, lengkap dengan nama, total, metode, dan status.", "Transaksi terlihat di menu Kelola Setoran."],
        [("Tombol simpan abu-abu dan tidak bisa diklik", "Pastikan ada minimal satu baris berjumlah lebih dari nol, tidak ada jenis yang dipilih dua kali, dan (untuk setuju di lokasi) kotak pernyataan sudah dicentang."),
         ("Peringatan jenis sampah dipilih dua kali", "Gabungkan jumlahnya menjadi satu baris, lalu Hapus baris yang lain."),
         ("Tulisan Belum ada nasabah", "Buat akun Nasabah dulu di menu Data Pengguna."),
         ("Jenis sampah tidak ada di daftar", "Klik Jenis baru, atau aktifkan kembali jenis yang nonaktif di menu Jenis Sampah & Harga."),
         ("Sudah terlanjur salah input", "Buka Kelola Setoran lalu Edit atau Batalkan transaksi itu.")],
        "Jenis sampah yang dinonaktifkan tidak muncul di daftar pilihan."),

    "Kelola Setoran": G(
        "Memeriksa seluruh setoran, mengubah rinciannya, atau membatalkannya.",
        "Pengurus.",
        ["Setoran sudah pernah diinput di menu Input Setoran."],
        [("Status (filter)", "Pilih Semua, Menunggu, Disetujui, atau Dibatalkan untuk menyaring daftar."),
         ("Baris setoran (dapat dibuka)", "Judulnya berisi tanggal, nama nasabah, total, metode, dan status. Setelah dibuka tampil label status, nomor versi, tabel rincian, dan catatan riwayat berisi waktu kejadian."),
         ("Edit", "Membuka formulir rincian untuk mengubah jenis dan jumlah. Ada pada setoran yang belum dibatalkan dan belum terjual."),
         ("Batalkan", "Membatalkan setoran. Ada pada setoran yang belum dibatalkan dan belum terjual."),
         ("Simpan perubahan / Batal (saat Edit)", "Simpan perubahan menerapkan hasil edit. Batal kembali ke daftar tanpa perubahan.")],
        ["Buka menu Kelola Setoran.",
         "Pilih Status jika ingin menyaring, misalnya Menunggu.",
         "Klik baris setoran yang ingin diperiksa.",
         "Untuk mengubah: klik Edit, ubah jenis atau jumlah, periksa Total baru, lalu klik Simpan perubahan.",
         "Untuk membatalkan: klik Batalkan."],
        ["Setelah Simpan perubahan, status kembali menjadi Menunggu dan nomor versi naik satu. Nasabah harus menyetujui ulang lewat akunnya, dan selama itu saldo serta stok dari setoran tersebut tidak dihitung.",
         "Setelah Batalkan, status menjadi Dibatalkan. Setoran tidak lagi dihitung pada saldo, stok, maupun kas."],
        ["Status dan versi pada baris setoran ikut berubah.", "Catatan riwayat bertambah satu entri dengan nama Anda."],
        [("Tidak ada tombol Edit dan Batalkan, hanya tulisan Sudah masuk penjualan", "Setoran itu sudah dihitung dalam penjualan ke pengepul. Batalkan penjualannya dulu di menu Penjualan Pengepul."),
         ("Tombol Simpan perubahan abu-abu", "Pastikan ada baris berjumlah lebih dari nol dan tidak ada jenis ganda."),
         ("Daftar kosong dengan tulisan Belum ada setoran", "Belum ada setoran, atau tidak ada yang cocok dengan filter Status.")],
        "Mengedit setoran yang sudah Disetujui akan mengurangi saldo dan stok sementara sampai nasabah menyetujui ulang."),

    "Nasabah": G(
        "Melihat daftar nasabah beserta saldonya dan riwayat transaksi tiap nasabah.",
        "Pengurus. Halaman ini hanya untuk melihat, tidak ada data yang diubah.",
        ["Sudah ada akun Nasabah aktif di menu Data Pengguna."],
        [("Tabel daftar nasabah", "Kolom Nama, Email, dan Saldo."),
         ("Lihat riwayat", "Pilih seorang nasabah untuk melihat rinciannya."),
         ("Kartu Saldo", "Saldo tabungan nasabah yang dipilih."),
         ("Tabel riwayat", "Gabungan setoran (semua status) dan penarikan nasabah itu, dengan kolom Tanggal, Jenis, Rp, dan Status.")],
        ["Buka menu Nasabah.", "Baca tabel daftar untuk melihat saldo semua nasabah.", "Pilih nama pada Lihat riwayat.", "Baca kartu saldo dan tabel riwayat di bawahnya."],
        ["Tidak ada perubahan data; halaman hanya menampilkan informasi."],
        ["Kartu saldo dan tabel riwayat berganti mengikuti nasabah yang dipilih."],
        [("Tulisan Belum ada nasabah", "Daftarkan nasabah di menu Data Pengguna."),
         ("Saldo tidak bertambah setelah setoran", "Saldo hanya bertambah dari setoran Tabung yang sudah Disetujui. Setoran Tunai tidak menambah saldo.")]),

    "Penarikan Saldo": G(
        "Memproses pengajuan penarikan saldo dari nasabah, dan mencatat penarikan yang dilakukan langsung di bank sampah.",
        "Pengurus.",
        ["Nasabah memiliki saldo.", "Untuk pengajuan: nasabah sudah mengajukan dari menu Saldo Saya di akunnya.", "Untuk menghubungi nasabah lewat WhatsApp: nomor WhatsApp nasabah sudah diisi di Data Pengguna."],
        [("Pengajuan dari nasabah", "Satu kartu untuk tiap pengajuan yang masih berjalan, berisi nama, nominal, status, waktu pengajuan, dan saldo nasabah saat ini."),
         ("Setujui pengajuan", "Tampil pada status Menunggu Konfirmasi. Mengubah status menjadi Disetujui."),
         ("Jadwal pengambilan dan Simpan jadwal", "Tampil setelah disetujui. Isi hari dan jam pengambilan, lalu simpan. Status menjadi Menunggu Pengambilan."),
         ("Konfirmasi Pembayaran Selesai", "Klik hanya setelah uang benar-benar diserahkan ke nasabah. Saldo nasabah berkurang dan penarikan tercatat."),
         ("Alasan jika ditolak dan Tolak pengajuan", "Isi alasan lalu klik Tolak pengajuan. Alasan akan dilihat nasabah."),
         ("Hubungi nasabah via WhatsApp", "Membuka WhatsApp dengan pesan yang sudah terisi. Hanya aktif jika nomor nasabah sudah diisi."),
         ("Catat penarikan langsung", "Untuk nasabah yang mengambil uang di tempat tanpa mengajukan lewat aplikasi: pilih Nasabah, lihat kartu Saldo saat ini dan Saldo tersedia, isi Jumlah diambil (Rp), lalu klik Proses penarikan."),
         ("Riwayat pengajuan dan Riwayat penarikan", "Dua tabel catatan lengkap. Riwayat penarikan menunjukkan sumbernya: Pengajuan atau Langsung.")],
        ["Buka menu Penarikan Saldo (angka di sebelah nama menu menunjukkan jumlah pengajuan berjalan).",
         "Pada kartu pengajuan berstatus Menunggu Konfirmasi, periksa nominal terhadap saldo, lalu klik Setujui pengajuan.",
         "Isi Jadwal pengambilan, misalnya Sabtu 10.00 di bank sampah, lalu klik Simpan jadwal.",
         "Saat nasabah datang dan uang sudah diserahkan, klik Konfirmasi Pembayaran Selesai.",
         "Jika pengajuan tidak bisa dipenuhi, isi Alasan jika ditolak lalu klik Tolak pengajuan.",
         "Untuk penarikan langsung: gulir ke Catat penarikan langsung, pilih nasabah, isi jumlah, klik Proses penarikan."],
        ["Setujui pengajuan: status Disetujui, saldo belum berkurang.",
         "Simpan jadwal: status Menunggu Pengambilan dan nasabah melihat jadwalnya.",
         "Konfirmasi Pembayaran Selesai: status Selesai, saldo berkurang, dan penarikan masuk Riwayat penarikan.",
         "Tolak pengajuan: status Ditolak dan saldo tidak berubah.",
         "Proses penarikan: saldo langsung berkurang."],
        ["Muncul pesan hijau, misalnya Pembayaran tercatat. Saldo nasabah sudah berkurang.", "Baris baru muncul pada tabel Riwayat penarikan."],
        [("Pesan Isi jadwal pengambilan dulu", "Kolom jadwal masih kosong."),
         ("Pesan Isi alasan penolakan", "Isi kolom Alasan jika ditolak sebelum menolak."),
         ("Pesan Saldo nasabah tidak cukup lagi", "Saldo nasabah sudah berubah sejak pengajuan dibuat. Tolak pengajuan dengan alasan, atau minta pengajuan baru."),
         ("Pesan Jumlah melebihi saldo tersedia", "Saldo tersedia sudah dikurangi pengajuan yang sedang berjalan. Kecilkan jumlah."),
         ("Tombol WhatsApp tidak ada", "Isi nomor WhatsApp nasabah di menu Data Pengguna.")],
        "Konfirmasi Pembayaran Selesai tidak bisa dibatalkan dari aplikasi. Pastikan uang sudah diserahkan sebelum menekannya."),

    "Penjualan Pengepul": G(
        "Mencatat penjualan sampah kepada pengepul saat pengepul datang mengangkut, berdasarkan hasil timbangan pengepul.",
        "Pengurus. Pengepul hanya dapat melihat catatannya di akun Pengepul, tidak dapat mencatat sendiri.",
        ["Sudah ada akun Pengepul yang aktif (menu Data Pengguna).", "Ada stok sampah dari setoran yang sudah Disetujui.", "Hasil timbangan dan harga jual per satuan dari pengepul sudah diketahui."],
        [("Pengepul yang datang", "Pilih nama pengepul."),
         ("Tanggal penjualan", "Tanggal pengangkutan. Bawaannya hari ini."),
         ("Tabel penjualan", "Kolom Jenis, Satuan, dan Perkiraan (stok menurut aplikasi) terkunci. Isi kolom Berat dari timbangan pengepul, dan kolom Harga dengan harga jual per satuan. Harga bawaan mengikuti penjualan terakhir untuk jenis itu."),
         ("Total dibayar pengepul", "Jumlah Berat kali Harga untuk semua baris."),
         ("Peringatan berat melebihi perkiraan", "Muncul jika timbangan lebih besar dari stok. Centang kotak lanjutkan bila memang benar."),
         ("Saya konfirmasi seluruh stok ini sudah diangkut pengepul", "Kotak yang wajib dicentang."),
         ("Simpan penjualan", "Menyimpan penjualan."),
         ("Riwayat penjualan", "Daftar penjualan. Tiap penjualan bisa dibuka untuk melihat rincian dan memiliki tombol Batalkan penjualan (stok dikembalikan).")],
        ["Buka menu Penjualan Pengepul.",
         "Pilih Pengepul yang datang dan periksa Tanggal penjualan.",
         "Isi kolom Berat dan Harga pada tabel untuk setiap jenis yang diangkut. Klik sel lalu ketik angkanya.",
         "Periksa Total dibayar pengepul.",
         "Jika muncul peringatan berat, pastikan timbangan benar lalu centang kotak lanjutkan.",
         "Centang Saya konfirmasi seluruh stok ini sudah diangkut pengepul.",
         "Klik Simpan penjualan."],
        ["Penjualan tercatat dan seluruh stok yang ada dianggap sudah terangkut, sehingga stok kembali nol. Hal ini berlaku untuk semua jenis, termasuk yang Beratnya Anda isi nol.",
         "Penjualan masuk ke Net Kas di Beranda dan muncul di akun Pengepul pada Riwayat Penjualan.",
         "Jika dibatalkan, status menjadi Dibatalkan dan stok dikembalikan."],
        ["Muncul pesan hijau Penjualan tercatat dan stok kembali nol.", "Penjualan baru muncul di bagian Riwayat penjualan."],
        [("Tulisan Belum ada pengepul", "Buat akun Pengepul di menu Data Pengguna."),
         ("Tulisan Belum ada stok yang disetujui untuk dijual", "Belum ada setoran Disetujui yang belum terjual. Periksa menu Kelola Setoran."),
         ("Tombol Simpan penjualan abu-abu", "Pastikan kotak konfirmasi dicentang, total lebih dari nol, dan (bila ada peringatan) kotak lanjutkan dicentang."),
         ("Salah mencatat penjualan", "Klik Batalkan penjualan pada Riwayat penjualan, lalu catat ulang.")],
        "Perhatian: aplikasi saat ini menganggap seluruh stok terjual setiap kali penjualan disimpan. Jika pengepul hanya mengangkut sebagian, pertimbangkan dulu cara pencatatannya bersama pengelola aplikasi."),

    "Pengeluaran Operasional": G(
        "Mencatat biaya operasional seperti bensin dan perlengkapan. Biaya ini mengurangi Net Kas.",
        "Pengurus.",
        ["Tanggal, jenis biaya, dan jumlah uangnya sudah diketahui."],
        [("Tanggal", "Tanggal biaya dikeluarkan."), ("Kategori", "Bensin, Transportasi, Perlengkapan, atau Lainnya."),
         ("Deskripsi", "Keterangan singkat."), ("Jumlah (Rp)", "Nominal pengeluaran."),
         ("Simpan pengeluaran", "Aktif setelah jumlah lebih dari nol."), ("Tabel riwayat", "Semua pengeluaran yang pernah dicatat.")],
        ["Buka menu Pengeluaran Operasional.", "Pilih Tanggal dan Kategori.", "Isi Deskripsi.", "Isi Jumlah (Rp).", "Klik Simpan pengeluaran."],
        ["Pengeluaran masuk ke tabel riwayat dan dihitung pada Pengeluaran Operasional serta Net Kas di Beranda."],
        ["Baris baru muncul di tabel paling atas."],
        [("Tombol Simpan pengeluaran abu-abu", "Isi Jumlah dengan angka lebih dari nol."),
         ("Salah catat", "Saat ini catatan pengeluaran tidak bisa diedit atau dihapus dari aplikasi, jadi periksa dulu sebelum menyimpan.")]),

    "Stok Sampah": G(
        "Menampilkan perkiraan sampah yang sudah terkumpul tetapi belum dijual ke pengepul.",
        "Pengurus. Halaman ini hanya untuk melihat.",
        ["Ada setoran yang sudah Disetujui."],
        [("Kartu per jenis sampah", "Nama jenis dan jumlahnya dalam kg atau pcs.")],
        ["Buka menu Stok Sampah.", "Baca kartu stok tiap jenis."],
        ["Tidak ada data yang berubah."],
        ["Jumlah stok sama dengan total setoran Disetujui yang belum terjual."],
        [("Tulisan Stok kosong", "Stok bertambah setelah nasabah menyetujui setoran. Setoran berstatus Menunggu atau Dibatalkan tidak dihitung."),
         ("Stok tiba-tiba nol", "Biasanya karena penjualan ke pengepul baru saja disimpan. Lihat menu Penjualan Pengepul.")],
        "Stok adalah perkiraan berdasarkan pencatatan. Berat akhir mengikuti timbangan saat pengangkutan."),

    "Jenis Sampah & Harga": G(
        "Mengatur jenis sampah yang diterima dan harga beli dari nasabah, serta melihat riwayat perubahan harga.",
        "Pengurus.",
        ["Harga terbaru dari bank sampah sudah diketahui."],
        [("Baris tiap jenis", "Nama jenis, satuan (per kg atau per pcs), kolom harga yang bisa diubah, dan tombol Nonaktifkan atau Aktifkan. Tulisan terkunci muncul pada jenis yang sudah pernah dipakai pada setoran."),
         ("Kolom harga", "Ketik harga baru lalu tekan Enter. Perubahan langsung tersimpan dan dicatat."),
         ("Nonaktifkan / Aktifkan", "Jenis nonaktif tidak muncul di pilihan Input Setoran."),
         ("Tambah jenis baru", "Isi Nama jenis, pilih Satuan, isi Harga beli (Rp), lalu klik Simpan jenis."),
         ("Riwayat perubahan harga", "Tabel Waktu, Jenis, Lama, Baru, dan Oleh.")],
        ["Buka menu Jenis Sampah & Harga.", "Ubah angka pada kolom harga jenis yang berubah, lalu tekan Enter.", "Untuk jenis yang sudah tidak diterima, klik Nonaktifkan.", "Untuk jenis baru, buka Tambah jenis baru lalu isi dan simpan."],
        ["Harga baru hanya berlaku untuk setoran berikutnya. Setoran lama tetap memakai harga saat dibuat.", "Setiap perubahan harga masuk ke Riwayat perubahan harga."],
        ["Perubahan tampil sebagai baris baru di Riwayat perubahan harga."],
        [("Pesan Nama kosong atau sudah ada", "Isi nama jenis yang belum dipakai."),
         ("Harga tidak berubah", "Pastikan menekan Enter atau berpindah dari kolom setelah mengetik.")]),

    "Data Pengguna": G(
        "Mendaftarkan akun nasabah, pengepul, dan pengurus, serta mengelola kata sandi, status, peran, dan nomor WhatsApp.",
        "Pengurus.",
        ["Nama dan email calon pengguna.", "Nomor WhatsApp jika ingin memakai tombol WhatsApp (opsional)."],
        [("Tabel pengguna", "Nama, Email, Peran, Status (Aktif atau Nonaktif), dan Login."),
         ("Buat akun baru", "Isi Nama, Email, pilih Peran (Nasabah, Pengepul, atau Pengurus), dan Nomor WhatsApp (opsional), lalu klik Buat akun."),
         ("Kata sandi sementara", "Ditampilkan satu kali setelah akun dibuat atau kata sandi dibuat ulang. Catat dan berikan kepada pengguna."),
         ("Kelola akun", "Pilih email akun lain. Tersedia: Buat ulang kata sandi sementara, Aktifkan atau nonaktifkan akun, pilihan Peran lalu Simpan perubahan peran, dan Simpan nomor WhatsApp."),
         ("Akun sendiri", "Akun Anda tidak muncul pada pilihan Kelola akun. Kata sandi sendiri diganti di menu Pengaturan.")],
        ["Buka menu Data Pengguna.", "Isi Nama dan Email pada Buat akun baru, pilih Peran, lalu klik Buat akun.",
         "Catat kata sandi sementara yang tampil, lalu berikan kepada pengguna.",
         "Pengguna login dan diminta membuat kata sandi baru.",
         "Jika pengguna lupa kata sandi: pilih emailnya di Kelola akun lalu klik Buat ulang kata sandi sementara."],
        ["Akun baru langsung bisa login dengan kata sandi sementara dan wajib menggantinya.", "Menonaktifkan akun membuat pemilik tidak bisa login. Mengubah peran tidak mengubah transaksi lama."],
        ["Pengguna baru muncul di tabel.", "Kata sandi sementara tampil dalam kotak hijau."],
        [("Pesan Nama kosong, email tidak valid, atau email sudah terdaftar", "Periksa isian. Email harus memuat tanda @ dan belum dipakai."),
         ("Kata sandi sementara hilang dari layar", "Klik Buat ulang kata sandi sementara untuk membuat yang baru."),
         ("Pesan Nomor WhatsApp tidak valid", "Gunakan format 08... atau 628... (10 sampai 15 digit).")],
        "Kata sandi sementara tidak ditampilkan lagi setelah halaman berganti."),

    "Laporan": G(
        "Menyusun rekap transaksi per periode dan mengunduhnya sebagai berkas CSV yang bisa dibuka di Excel.",
        "Pengurus.",
        ["Transaksi sudah tercatat pada periode yang ingin dilihat."],
        [("Jenis laporan", "Pembelian dari nasabah, Penjualan ke pengepul, Pengeluaran, Net kas, Penarikan saldo, Saldo nasabah, atau Stok sampah."),
         ("Periode", "Hari ini, Bulan ini, atau Rentang bebas. Rentang bebas menampilkan pilihan Dari tanggal sampai tanggal."),
         ("Tabel laporan", "Isi laporan sesuai pilihan."),
         ("Unduh CSV (dibuka di Excel)", "Mengunduh isi tabel sebagai berkas CSV.")],
        ["Buka menu Laporan.", "Pilih Jenis laporan.", "Pilih Periode. Untuk Rentang bebas, klik tanggal awal lalu tanggal akhir.", "Baca tabel yang tampil.", "Klik Unduh CSV (dibuka di Excel) jika perlu berkasnya."],
        ["Tabel menyesuaikan pilihan. Unduhan menghasilkan berkas CSV dengan nama sesuai jenis laporan dan periode."],
        ["Tabel muncul dan berkas CSV terunduh."],
        [("Tulisan Tidak ada data pada periode ini", "Coba periode yang lebih luas."),
         ("Halaman tidak menampilkan tabel pada Rentang bebas", "Pilih dua tanggal, awal dan akhir. Satu tanggal saja belum cukup."),
         ("Kolom CSV tampak menyatu di Excel", "Pakai Data lalu From Text/CSV dan pilih pemisah titik koma.")],
        "Laporan Saldo nasabah dan Stok sampah menunjukkan kondisi saat ini, jadi tidak terpengaruh oleh pilihan periode. Aplikasi menyediakan unduh CSV, belum ada tombol cetak."),

    "Pengaturan": G(
        "Melihat status penyimpanan data, mengunduh cadangan, mengatur nomor WhatsApp Pengurus, dan mengganti kata sandi sendiri.",
        "Pengurus.",
        ["Untuk ganti kata sandi: kata sandi yang sekarang."],
        [("Penyimpanan data", "Keterangan apakah data disimpan di Postgres (Neon) atau berkas SQLite."),
         ("Unduh cadangan data (JSON, tanpa kata sandi)", "Menyimpan salinan seluruh data ke komputer Anda. Disarankan dilakukan berkala."),
         ("Nomor WhatsApp pengurus", "Dipakai tombol Hubungi Pengurus via WhatsApp di akun nasabah. Klik Simpan nomor WhatsApp pengurus setelah mengisi."),
         ("Ganti kata sandi saya", "Isi kata sandi sekarang, kata sandi baru (minimal 8 karakter), dan ulangi, lalu klik Simpan kata sandi baru."),
         ("Data contoh", "Tombol Muat data contoh dan Hapus data contoh. Hanya untuk percobaan, bukan untuk pemakaian nyata. Ini berbeda dari Mode Demo di halaman login.")],
        ["Buka menu Pengaturan.", "Isi nomor WhatsApp Pengurus lalu simpan agar nasabah bisa menghubungi Anda.", "Unduh cadangan data secara berkala.", "Ganti kata sandi jika perlu."],
        ["Nomor WhatsApp tersimpan dan dipakai pada akun nasabah.", "Kata sandi baru berlaku pada login berikutnya."],
        ["Muncul pesan hijau, misalnya Nomor WhatsApp pengurus disimpan atau Kata sandi berhasil diganti."],
        [("Pesan Nomor tidak valid", "Gunakan format 08... atau 628... (10 sampai 15 digit)."),
         ("Pesan Kata sandi sekarang salah", "Ketik ulang kata sandi lama dengan teliti."),
         ("Pesan Kata sandi baru minimal 8 karakter", "Perpanjang kata sandi dan pastikan kedua isian sama.")],
        "Jangan menekan Muat data contoh pada data yang sudah dipakai nyata."),

    "Panduan Penggunaan": G(
        "Berisi tutorial lengkap setiap menu aplikasi.",
        "Semua pengguna. Pengurus melihat panduan ketiga peran.",
        ["Tidak ada."],
        [("Tab", "Pilih tab sesuai kebutuhan. Klik judul halaman di dalam tab untuk membukanya."),
         ("Panduan Halaman Ini", "Tombol di bagian atas setiap halaman untuk membuka penjelasan halaman yang sedang dibuka.")],
        ["Pilih tab.", "Klik halaman yang ingin dipelajari.", "Baca bagian Fungsi, Langkah, dan Kendala."],
        ["Tidak ada data yang berubah."], ["Penjelasan halaman terbuka."],
        [("Ingin panduan halaman lain", "Buka menu Panduan Penggunaan dan pilih halamannya.")]),
}

# =====================================================================
# PANDUAN NASABAH
# =====================================================================
NASABAH = {
    "Beranda": G(
        "Menampilkan saldo tabungan dan ringkasan aktivitas Anda.",
        "Nasabah.",
        ["Tidak ada yang perlu disiapkan."],
        [("Saldo Tabungan Saya", "Saldo dari setoran Tabung yang sudah Anda setujui dikurangi penarikan. Di bawahnya ada keterangan jumlah setoran yang menunggu persetujuan. Tulisan Dapat ditarik menunjukkan saldo tabungan. Saldo yang benar-benar bisa diajukan (setelah dikurangi pengajuan yang sedang berjalan) ada di menu Saldo Saya."),
         ("Periksa setoran sekarang", "Tombol yang muncul bila ada setoran menunggu persetujuan. Membuka menu Persetujuan Setoran."),
         ("Kotak status penarikan", "Muncul jika Anda punya pengajuan penarikan yang sedang berjalan, lengkap dengan statusnya. Diperbarui sendiri tiap 15 detik."),
         ("Tiga kartu", "Sampah disetorkan (kg dan pcs), Transaksi disetujui, dan Total pernah ditarik."),
         ("Aktivitas terbaru", "Lima kegiatan terakhir Anda.")],
        ["Masuk ke akun Nasabah.", "Lihat saldo di kartu hijau.", "Jika ada tombol Periksa setoran sekarang, klik untuk menyetujui setoran.", "Baca Aktivitas terbaru."],
        ["Tombol hanya berpindah halaman, tidak mengubah data."],
        ["Saldo dan kartu sesuai dengan menu Saldo Saya dan Riwayat Setoran."],
        [("Setoran belum menambah saldo", "Setoran harus Anda setujui dulu, dan saldo hanya bertambah dari setoran Tabung. Setoran Tunai tidak menambah saldo."),
         ("Tulisan Belum ada aktivitas", "Setoran pertama Anda akan muncul setelah dicatat Pengurus.")]),

    "Persetujuan Setoran": G(
        "Memeriksa setoran yang dimasukkan Pengurus dan menyetujuinya jika cocok dengan hasil penimbangan.",
        "Nasabah.",
        ["Pengurus sudah memasukkan setoran dengan pilihan persetujuan lewat akun Anda.", "Anda ingat hasil penimbangan sampah Anda."],
        [("Kartu transaksi", "Berisi nomor transaksi, tanggal, metode (Tabung atau Tunai), status, dan Total."),
         ("Lihat Rincian", "Membuka tabel Jenis, Jumlah, Harga, dan Subtotal."),
         ("Kotak centang Saya sudah mencocokkan dengan hasil penimbangan", "Harus dicentang agar tombol setuju aktif."),
         ("Setujui Setoran", "Menyetujui transaksi.")],
        ["Buka menu Persetujuan Setoran (atau klik Periksa setoran sekarang di Beranda).", "Klik Lihat Rincian.", "Cocokkan jenis dan berat dengan hasil timbangan.", "Jika sudah cocok, centang kotak pencocokan.", "Klik Setujui Setoran."],
        ["Status menjadi Disetujui. Stok bank sampah bertambah, dan jika metodenya Tabung, saldo Anda ikut bertambah."],
        ["Transaksi hilang dari halaman ini dan muncul di Riwayat Setoran berstatus Disetujui."],
        [("Tombol Setujui Setoran abu-abu", "Centang kotak pencocokan dulu."),
         ("Ada yang tidak sesuai", "Jangan disetujui. Hubungi Pengurus untuk dikoreksi. Rincian tidak bisa diubah dari akun Anda."),
         ("Tulisan Tidak ada setoran yang perlu diperiksa", "Tidak ada setoran yang menunggu persetujuan. Jika Pengurus baru memasukkan data, muat ulang halaman.")]),

    "Riwayat Setoran": G(
        "Melihat semua setoran Anda beserta statusnya.",
        "Nasabah.",
        ["Tidak ada."],
        [("Periode", "Pilih Semua, Bulan ini, atau 30 hari terakhir."),
         ("Daftar setoran", "Tiap baris berisi nomor, tanggal, total, metode, dan status. Klik untuk membuka tabel rincian.")],
        ["Buka menu Riwayat Setoran.", "Pilih Periode.", "Klik setoran untuk melihat rinciannya."],
        ["Tidak ada data yang berubah."], ["Daftar menyesuaikan periode yang dipilih."],
        [("Tulisan Belum ada setoran pada periode ini", "Pilih periode Semua."),
         ("Status Menunggu", "Setoran belum Anda setujui. Buka Persetujuan Setoran."),
         ("Status Dibatalkan", "Setoran dibatalkan Pengurus dan tidak dihitung. Tanyakan alasannya kepada Pengurus.")]),

    "Saldo Saya": G(
        "Melihat saldo dan mutasi tabungan, serta mengajukan penarikan saldo.",
        "Nasabah.",
        ["Memiliki saldo dari setoran Tabung yang sudah disetujui.", "Tidak sedang memiliki pengajuan penarikan yang belum selesai."],
        [("Saldo Tabungan Saya", "Saldo saat ini."),
         ("Saldo tabungan dan Saldo tersedia untuk ditarik", "Saldo tersedia sudah dikurangi pengajuan yang sedang berjalan."),
         ("Nominal yang ingin ditarik (Rp)", "Isi jumlah yang ingin diambil. Muncul peringatan bila melebihi saldo tersedia."),
         ("Pilihan A, Kirim pengajuan", "Mengirim pengajuan ke Pengurus lewat aplikasi. Tombol nonaktif jika nominal nol, melebihi saldo, atau masih ada pengajuan berjalan."),
         ("Pilihan B, Hubungi Pengurus via WhatsApp", "Membuka WhatsApp dengan pesan berisi nama dan nominal. Aktif jika nomor WhatsApp Pengurus sudah diatur dan nominal diisi. Pesan ini tidak tercatat otomatis di aplikasi."),
         ("Mutasi tabungan", "Daftar tanggal, keterangan, dan jumlah. Tanda plus untuk setoran, tanda minus untuk penarikan.")],
        ["Buka menu Saldo Saya.", "Isi Nominal yang ingin ditarik (Rp).", "Pilih Pilihan A lalu klik Kirim pengajuan, atau Pilihan B untuk menghubungi Pengurus.", "Pantau status pada kotak kuning di halaman ini, Beranda, atau menu Riwayat Penarikan.", "Ikuti jadwal pengambilan dari Pengurus."],
        ["Pengajuan terkirim dengan status Menunggu Konfirmasi dan saldo belum berkurang.",
         "Alur selanjutnya: Disetujui, lalu Menunggu Pengambilan (jadwal ditentukan Pengurus), lalu Selesai setelah uang Anda terima dan Pengurus mengonfirmasi. Saldo baru berkurang pada tahap Selesai.",
         "Jika ditolak, statusnya Ditolak dan alasannya bisa dibaca di menu Riwayat Penarikan."],
        ["Muncul pesan hijau Pengajuan penarikan terkirim.", "Kotak status berwarna kuning menampilkan pengajuan Anda."],
        [("Tombol Kirim pengajuan abu-abu", "Isi nominal lebih dari nol, jangan melebihi saldo tersedia, dan pastikan tidak ada pengajuan lain yang berjalan."),
         ("Pesan Kamu masih punya pengajuan yang belum selesai", "Tunggu sampai pengajuan sebelumnya selesai atau ditolak."),
         ("Tulisan Nomor WhatsApp pengurus belum diatur", "Pakai Pilihan A, atau minta Pengurus mengisi nomornya.")]),

    "Riwayat Penarikan": G(
        "Melihat pengajuan penarikan dan penarikan yang sudah dibayarkan.",
        "Nasabah.",
        ["Tidak ada."],
        [("Tiga kartu", "Total pernah ditarik, Jumlah penarikan, dan Pengajuan berjalan."),
         ("Pengajuan penarikan", "Tabel Diajukan, Nominal, Status, Dibayar, dan Keterangan. Keterangan berisi jadwal pengambilan atau alasan penolakan."),
         ("Penarikan yang sudah dibayarkan", "Tabel Tanggal, Jumlah, dan Diproses oleh siapa.")],
        ["Buka menu Riwayat Penarikan.", "Baca status pengajuan dan kolom Keterangan."],
        ["Tidak ada data yang berubah."], ["Status pengajuan sesuai dengan yang dilakukan Pengurus."],
        [("Tulisan Belum ada pengajuan", "Ajukan dari menu Saldo Saya."),
         ("Status Ditolak", "Baca alasannya pada kolom Keterangan, lalu hubungi Pengurus bila perlu.")]),

    "Profil Saya": G(
        "Melihat data akun dan mengganti kata sandi.",
        "Nasabah.",
        ["Kata sandi yang sekarang."],
        [("Kartu Nama, Email, dan Peran", "Data akun Anda. Dikelola Pengurus, hubungi Pengurus untuk mengubah nama atau email."),
         ("Ganti kata sandi", "Isi Kata sandi sekarang, Kata sandi baru (minimal 8 karakter), dan Ulangi kata sandi baru, lalu klik Simpan kata sandi baru."),
         ("Keluar", "Tombol Keluar ada di bagian bawah menu samping.")],
        ["Buka menu Profil Saya.", "Isi tiga kolom kata sandi.", "Klik Simpan kata sandi baru.", "Untuk mengakhiri sesi, klik Keluar di menu samping."],
        ["Kata sandi baru berlaku pada login berikutnya.", "Setelah Keluar, Anda kembali ke halaman login."],
        ["Muncul pesan hijau Kata sandi berhasil diganti."],
        [("Pesan Kata sandi sekarang salah", "Ketik ulang dengan teliti."),
         ("Pesan minimal 8 karakter dan kedua isian harus sama", "Perpanjang kata sandi dan ketik sama persis pada kolom ulangi."),
         ("Lupa kata sandi", "Minta Pengurus membuatkan kata sandi sementara yang baru.")]),

    "Panduan Penggunaan": G(
        "Berisi tutorial lengkap menu yang tersedia untuk Nasabah.",
        "Nasabah.", ["Tidak ada."],
        [("Tab dan judul halaman", "Klik judul halaman untuk membuka penjelasannya."),
         ("Panduan Halaman Ini", "Tombol di bagian atas setiap halaman untuk membuka penjelasan halaman yang sedang dibuka.")],
        ["Pilih halaman yang ingin dipelajari.", "Baca langkah-langkahnya."],
        ["Tidak ada data yang berubah."], ["Penjelasan terbuka."],
        [("Ingin panduan halaman lain", "Buka menu Panduan Penggunaan dan pilih halamannya.")]),
}

# =====================================================================
# PANDUAN PENGEPUL (tanpa harga beli nasabah, saldo, atau kas)
# =====================================================================
PENGEPUL = {
    "Beranda": G(
        "Menampilkan ringkasan stok sampah yang tersedia untuk diangkut.",
        "Pengepul.",
        ["Tidak ada."],
        [("Empat kartu", "Jenis sampah tersedia, Perkiraan berat (kg), Perkiraan barang (pcs), dan Stok diperbarui (tanggal pencatatan terakhir)."),
         ("Stok per jenis", "Kartu tiap jenis berisi jumlah dan batang perbandingan antar jenis."),
         ("Catatan di bawah", "Stok adalah perkiraan. Berat akhir mengikuti hasil penimbangan saat pengangkutan.")],
        ["Masuk ke akun Pengepul.", "Baca kartu ringkasan.", "Lihat Stok per jenis untuk mempersiapkan pengangkutan."],
        ["Tidak ada data yang berubah."], ["Kartu menampilkan stok terbaru."],
        [("Tulisan Belum ada sampah terkumpul", "Stok kembali nol setelah pengangkutan dan terisi lagi saat ada setoran baru."),
         ("Angka berbeda dengan timbangan", "Angka di aplikasi hanya perkiraan. Pegangan akhirnya adalah timbangan saat pengangkutan.")]),

    "Perkiraan Stok": G(
        "Menampilkan daftar perkiraan sampah yang terkumpul dan belum diangkut.",
        "Pengepul.", ["Tidak ada."],
        [("Kartu stok", "Jenis, label Tersedia, jumlah, dan batang perbandingan."),
         ("Tabel", "Kolom Jenis, Satuan, dan Perkiraan.")],
        ["Buka menu Perkiraan Stok.", "Baca kartu dan tabel."],
        ["Tidak ada data yang berubah."], ["Daftar stok tampil."],
        [("Tulisan Belum ada sampah terkumpul", "Tunggu hingga ada setoran baru.")],
        "Stok merupakan perkiraan berdasarkan pencatatan internal."),

    "Riwayat Penjualan": G(
        "Melihat catatan pengangkutan dan penjualan yang atas nama Anda.",
        "Pengepul. Pencatatan dilakukan oleh Pengurus saat Anda datang mengangkut, jadi halaman ini hanya untuk melihat.",
        ["Pengurus sudah mencatat penjualan atas nama Anda."],
        [("Daftar penjualan", "Tiap baris berisi nomor, tanggal, total, dan status. Klik untuk membuka."),
         ("Isi penjualan", "Tabel Jenis, Satuan, Berat, Harga, dan Jumlah, serta Total penjualan.")],
        ["Buka menu Riwayat Penjualan.", "Klik penjualan yang ingin diperiksa.", "Cocokkan berat dan harga dengan catatan Anda."],
        ["Tidak ada data yang berubah."], ["Rincian penjualan tampil lengkap."],
        [("Tulisan Belum ada laporan penjualan untukmu", "Belum ada penjualan yang dicatat atas nama Anda."),
         ("Catatan tidak sesuai", "Hubungi Pengurus untuk dikoreksi. Perubahan hanya bisa dilakukan Pengurus."),
         ("Status Dibatalkan", "Pengurus membatalkan catatan itu karena ada koreksi.")]),

    "Profil Saya": G(
        "Melihat data akun dan mengganti kata sandi.",
        "Pengepul.",
        ["Kata sandi yang sekarang."],
        [("Kartu Nama, Email, dan Peran", "Data akun Anda. Dikelola Pengurus."),
         ("Ganti kata sandi", "Isi Kata sandi sekarang, Kata sandi baru (minimal 8 karakter), dan Ulangi kata sandi baru, lalu klik Simpan kata sandi baru."),
         ("Keluar", "Tombol Keluar ada di bagian bawah menu samping.")],
        ["Buka menu Profil Saya.", "Isi tiga kolom kata sandi.", "Klik Simpan kata sandi baru.", "Untuk mengakhiri sesi, klik Keluar di menu samping."],
        ["Kata sandi baru berlaku pada login berikutnya."],
        ["Muncul pesan hijau Kata sandi berhasil diganti."],
        [("Pesan Kata sandi sekarang salah", "Ketik ulang dengan teliti."),
         ("Lupa kata sandi", "Minta Pengurus membuatkan kata sandi sementara yang baru.")]),

    "Panduan Penggunaan": G(
        "Berisi tutorial lengkap menu yang tersedia untuk Pengepul.",
        "Pengepul.", ["Tidak ada."],
        [("Tab dan judul halaman", "Klik judul halaman untuk membuka penjelasannya."),
         ("Panduan Halaman Ini", "Tombol di bagian atas setiap halaman untuk membuka penjelasan halaman yang sedang dibuka.")],
        ["Pilih halaman yang ingin dipelajari.", "Baca langkah-langkahnya."],
        ["Tidak ada data yang berubah."], ["Penjelasan terbuka."],
        [("Ingin panduan halaman lain", "Buka menu Panduan Penggunaan dan pilih halamannya.")]),
}

PANDUAN = {"Pengurus": PENGURUS, "Nasabah": NASABAH, "Pengepul": PENGEPUL}

# judul tampilan untuk halaman yang namanya di menu berbeda dengan judul halaman
JUDUL = {("Pengurus", "Beranda"): "Beranda (Ringkasan Dashboard)"}

# =====================================================================
# MULAI CEPAT dan MODE DEMO
# =====================================================================
MULAI_CEPAT = [
    ("Masuk ke aplikasi", ["Buka alamat aplikasi.", "Pilih jenis akun: Pengurus, Nasabah, atau Pengepul.", "Isi Email dan Kata sandi, lalu klik tombol Masuk sebagai....",
                           "Jika akun Anda baru dibuat, aplikasi meminta Anda membuat kata sandi baru terlebih dahulu.",
                           "Jenis akun yang dipilih harus sama dengan jenis akun Anda. Jika tidak, muncul pesan Jenis akun tidak sesuai."]),
    ("Memakai menu", ["Menu ada di panel hijau di sisi kiri. Klik nama menu untuk membuka halamannya.",
                      "Di HP dan tablet, panel menu disembunyikan. Klik ikon panah di pojok kiri atas layar untuk membukanya, dan ikon yang sama untuk menutupnya.",
                      "Untuk keluar, klik Keluar di bagian bawah panel menu."]),
    ("Meminta bantuan", ["Klik Panduan Halaman Ini di bagian atas halaman untuk penjelasan halaman yang sedang dibuka.",
                         "Buka menu Panduan Penggunaan di panel menu untuk tutorial lengkap seluruh halaman.",
                         "Menu Panduan Penggunaan juga bisa dibuka lewat tombol di halaman Profil Saya (Nasabah dan Pengepul) atau Pengaturan (Pengurus)."]),
    ("Lupa kata sandi", ["Minta Pengurus membuatkan kata sandi sementara yang baru lewat menu Data Pengguna."]),
]

DEMO = [
    ("1. Cara masuk", ["Di halaman login, gulir ke kotak Ingin mencoba dulu? lalu klik Masuk sebagai Demo.",
                       "Tidak perlu email, kata sandi, atau pendaftaran.",
                       "Anda langsung masuk sebagai Pengurus Demo. Pita kuning bertuliskan MODE DEMO tampil di atas setiap halaman, dan label MODE DEMO tampil di menu samping."]),
    ("2. Berpindah tampilan Pengurus, Nasabah, dan Pengepul", ["Pada bagian atas halaman, cari Lihat tampilan sebagai.",
                       "Klik Pengurus, Nasabah, atau Pengepul. Menu dan halaman langsung berganti sesuai peran itu.",
                       "Data simulasi tetap sama saat berpindah peran, jadi hasil kerja di satu peran bisa dilihat di peran lain."]),
    ("3. Menjelajahi menu", ["Klik setiap menu di panel kiri.", "Klik Panduan Halaman Ini pada halaman mana pun jika ingin tahu fungsinya.",
                              "Halaman tertentu di Mode Demo bersifat terbatas: Pengaturan dan Profil Saya tidak menyimpan perubahan akun, kata sandi, atau penyimpanan data."]),
    ("4. Mencoba simulasi setoran", ["Pilih tampilan Pengurus lalu buka menu Input Setoran.", "Pilih nasabah, metode, isi jenis dan jumlah sampah.",
                                      "Pilih Nasabah setuju lewat akunnya lalu klik Simpan & Kirim ke Nasabah. Setoran akan menunggu persetujuan.",
                                      "Setoran terlihat di menu Kelola Setoran dan di Beranda pada kotak Menunggu Persetujuan."]),
    ("5. Mencoba simulasi persetujuan Nasabah", ["Pilih tampilan Nasabah (akun Nasabah Demo).", "Buka menu Persetujuan Setoran.",
                                                  "Buka Lihat Rincian, centang kotak pencocokan, lalu klik Setujui Setoran.",
                                                  "Lihat saldo di Beranda atau Saldo Saya. Saldo bertambah jika setoran bermetode Tabung."]),
    ("6. Mencoba simulasi penarikan saldo", ["Sebagai Nasabah, buka Saldo Saya, isi Nominal, klik Kirim pengajuan.",
                                              "Pindah ke tampilan Pengurus lalu buka menu Penarikan Saldo.",
                                              "Klik Setujui pengajuan, isi jadwal lalu Simpan jadwal, kemudian klik Konfirmasi Pembayaran Selesai.",
                                              "Kembali ke tampilan Nasabah dan lihat Riwayat Penarikan serta saldo yang berkurang.",
                                              "Sudah ada satu pengajuan dari nasabah contoh (Budi Contoh) yang bisa langsung Anda proses."]),
    ("7. Mencoba simulasi pencatatan penjualan Pengepul", ["Pencatatan penjualan dilakukan Pengurus. Pilih tampilan Pengurus lalu buka Penjualan Pengepul.",
                                                            "Pilih Pengepul Demo, isi Berat dan Harga, centang konfirmasi, lalu klik Simpan penjualan.",
                                                            "Pindah ke tampilan Pengepul lalu buka Riwayat Penjualan untuk melihat catatannya, dan Perkiraan Stok yang kembali nol."]),
    ("8. Melihat dashboard dan laporan", ["Tampilan Pengurus, menu Beranda: lihat kartu kas dan grafik yang ikut berubah setelah simulasi.",
                                           "Tampilan Pengurus, menu Laporan: pilih jenis laporan dan periode, lalu coba Unduh CSV.",
                                           "Berkas CSV yang terunduh berisi data simulasi."]),
    ("9. Tentang data simulasi", ["Semua nama, saldo, dan transaksi di Mode Demo adalah data fiktif yang dibuat khusus untuk percobaan.",
                                  "Data hanya ada di sesi Anda dan terpisah dari data asli. Apa pun yang Anda lakukan tidak mengubah saldo, stok, riwayat, atau data pengguna yang sebenarnya.",
                                  "Klik Atur ulang data demo untuk mengembalikan data simulasi ke kondisi awal. Data demo juga kembali awal setiap kali Anda masuk sebagai Demo.",
                                  "Untuk keluar dari Mode Demo, klik Keluar di menu samping."]),
]


# =====================================================================
# PENYAJI
# =====================================================================
def _daftar(st, items):
    st.markdown("\n".join(f"- {t}" for t in items))


def _urut(st, items):
    st.markdown("\n".join(f"{i}. {t}" for i, t in enumerate(items, 1)))


def sajikan(st, g):
    """Tampilkan satu panduan halaman, dengan urutan bagian yang sama untuk semua halaman."""
    st.markdown("**1. Fungsi halaman**")
    st.markdown(g["fungsi"])
    st.markdown("**2. Siapa yang dapat menggunakan**")
    st.markdown(g["siapa"])
    st.markdown("**3. Yang perlu disiapkan**")
    _daftar(st, g["siapkan"])
    st.markdown("**4. Penjelasan tombol, kolom, dan informasi**")
    _daftar(st, [f"**{a}**: {b}" for a, b in g["elemen"]])
    st.markdown("**5. Langkah-langkah**")
    _urut(st, g["langkah"])
    st.markdown("**6. Yang terjadi setelah tombol ditekan**")
    _daftar(st, g["setelah"])
    st.markdown("**7. Tanda proses berhasil**")
    _daftar(st, g["berhasil"])
    st.markdown("**8. Jika terjadi kendala**")
    _daftar(st, [f"**{a}**: {b}" for a, b in g["kendala"]])
    if g.get("catatan"):
        st.info(g["catatan"])


def sajikan_langkah(st, bagian):
    """Tampilkan daftar (judul, langkah). Judul berawalan angka dibuat berurutan, selain itu berbutir."""
    for judul, langkah in bagian:
        st.markdown(f"**{judul}**")
        (_urut if judul[:1].isdigit() else _daftar)(st, langkah)
