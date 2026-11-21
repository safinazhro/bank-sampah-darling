"""Data simulasi untuk Mode Demo EcoLedger Darling.

Modul ini hanya MEMBANGUN kamus data baru di memori. Ia tidak membaca dan tidak
menulis database produksi (Postgres/SQLite). Setiap sesi Mode Demo memegang
salinannya sendiri, jadi aktivitas di Mode Demo tidak pernah menyentuh data asli.

Seluruh nama, email, dan angka di sini fiktif.
"""
from datetime import timedelta

# Peran -> (email demo, nama tampilan). Email memakai domain fiktif ".demo" dan
# tidak punya kata sandi, jadi tidak bisa dipakai untuk login biasa.
DEMO_USERS = {
    "Pengurus": ("pengurus@akun.demo", "Pengurus Demo"),
    "Nasabah": ("nasabah@akun.demo", "Nasabah Demo"),
    "Pengepul": ("pengepul@akun.demo", "Pengepul Demo"),
}
DEMO_EMAILS = {e for e, _ in DEMO_USERS.values()}

# Nasabah tambahan agar daftar nasabah dan penarikan tidak sepi.
NASABAH_LAIN = [("budi@contoh.demo", "Budi Contoh"), ("siti@contoh.demo", "Siti Contoh"), ("rina@contoh.demo", "Rina Contoh")]


def bangun(db_awal, hari_ini, sekarang, token):
    """Kembalikan kamus data demo lengkap.

    db_awal   : hasil new_db() dari aplikasi (jenis sampah dan harga bawaan)
    hari_ini  : objek date (WIB)
    sekarang  : teks waktu 'YYYY-MM-DD HH:MM'
    token     : penanda unik sesi demo
    """
    D = db_awal
    D.setdefault("wr", [])
    D["pengaturan"] = {"wa": ""}
    D["_token"] = token
    D["mode_demo"] = True

    harga = {t["nama"]: t for t in D["types"]}

    def nid():
        D["seq"] += 1
        return D["seq"]

    def tgl(hari):
        return (hari_ini - timedelta(days=hari)).isoformat()

    def waktu(hari):
        return f"{tgl(hari)} 09:00" if hari else sekarang

    def log(*teks):
        return [f"{sekarang} · {t}" for t in teks]

    pengurus = DEMO_USERS["Pengurus"][1]
    for peran, (email, nama) in DEMO_USERS.items():
        D["users"].append(dict(email=email, nama=nama, peran=peran, aktif=True, pw="", hp=""))
    for email, nama in NASABAH_LAIN:
        D["users"].append(dict(email=email, nama=nama, peran="Nasabah", aktif=True, pw="", hp=""))
    nd = DEMO_USERS["Nasabah"]
    budi, siti, rina = NASABAH_LAIN

    def dep(hari, pemilik, metode, rows, status="Disetujui", sold=None):
        d = dict(id=nid(), tgl=tgl(hari), email=pemilik[0], nama=pemilik[1], metode=metode,
                 items=[dict(jenis=j, satuan=harga[j]["satuan"], jml=q, harga=harga[j]["harga"]) for j, q in rows],
                 status=status, sold=sold, ver=1, log=log("Data simulasi"), oleh=pengurus)
        if status == "Disetujui":
            d["disetujui_oleh"] = f"{pengurus} (konfirmasi langsung nasabah di lokasi)"
            d["disetujui_pada"] = waktu(hari)
        D["dep"].append(d)
        return d

    # --- setoran yang sudah terjual ke pengepul ---
    lama = [
        dep(26, nd, "Tabung", [("Kardus", 12), ("Botol plastik", 4)]),
        dep(25, budi, "Tunai", [("Besi", 6), ("Kaleng", 3)]),
        dep(24, siti, "Tabung", [("Buku", 9), ("Duplek", 5), ("Emberan", 4)]),
        dep(22, nd, "Tabung", [("Kardus", 8.5), ("Buku", 5)]),
    ]
    sid = nid()
    jual = [("Kardus", 20.5, 2400), ("Botol plastik", 4, 1800), ("Besi", 6, 4500), ("Kaleng", 3, 2800),
            ("Buku", 14, 1300), ("Duplek", 5, 700), ("Emberan", 4, 2000)]
    D["sales"].append(dict(id=sid, tgl=tgl(20), email=DEMO_USERS["Pengepul"][0], pengepul=DEMO_USERS["Pengepul"][1],
                           items=[dict(jenis=j, satuan=harga[j]["satuan"], jml=float(q), harga=h) for j, q, h in jual],
                           status="Aktif", oleh=pengurus))
    for d in lama:
        d["sold"] = sid

    # --- setoran yang masih menjadi stok ---
    dep(12, budi, "Tabung", [("Kardus", 10), ("Gelas botol", 6)])
    dep(9, siti, "Tabung", [("Galon aqua", 4), ("Gelas botol", 7)])
    dep(6, nd, "Tabung", [("Emberan", 10), ("Duplek", 6)])
    dep(4, rina, "Tunai", [("Kardus", 7.5), ("Le Mineral", 3)])
    dep(2, nd, "Tabung", [("Aki", 2), ("Kaleng", 4.5)])
    dep(0, siti, "Tabung", [("Buku", 6), ("Kertas semen", 4)])
    # --- setoran menunggu persetujuan nasabah (untuk mencoba alur persetujuan) ---
    dep(1, nd, "Tabung", [("Kardus", 5.5), ("Botol plastik", 3)], status="Menunggu")

    # --- penarikan saldo ---
    D["wd"].append(dict(id=nid(), tgl=tgl(15), waktu=waktu(15), email=nd[0], nama=nd[1], jumlah=20000, oleh=pengurus))
    D["wd"].append(dict(id=nid(), tgl=tgl(10), waktu=waktu(10), email=siti[0], nama=siti[1], jumlah=15000, oleh=pengurus))
    # pengajuan dari Budi menunggu konfirmasi Pengurus; Nasabah Demo sengaja tanpa pengajuan agar bisa mencoba mengajukan
    D["wr"].append(dict(id=nid(), email=budi[0], nama=budi[1], jumlah=20000, status="Menunggu Konfirmasi", diajukan=sekarang,
                        jadwal="", alasan="", dibayar_pada="", wd=None, log=log("Diajukan oleh Budi Contoh lewat aplikasi")))

    # --- pengeluaran operasional ---
    for hari, kat, ket, jml in [(18, "Bensin", "Antar sampah ke pengepul", 25000), (5, "Perlengkapan", "Karung dan timbangan", 40000), (0, "Bensin", "Keliling jemput sampah", 20000)]:
        D["exp"].append(dict(id=nid(), tgl=tgl(hari), kategori=kat, deskripsi=ket, jumlah=jml, oleh=pengurus))
    return D
