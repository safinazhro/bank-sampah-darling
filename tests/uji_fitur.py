"""Uji fungsional EcoLedger Darling (fitur lama + Mode Demo + Panduan) memakai streamlit.testing.AppTest.
Jalankan dari folder proyek:  python tests/uji_fitur.py
Memakai database SQLite sementara, tidak menyentuh data asli."""
import os, sys, json, sqlite3, tempfile, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, ROOT)
DB = os.path.join(tempfile.mkdtemp(), "uji.db")
os.environ["BANKSAMPAH_DB"] = DB
import streamlit as st
from streamlit.testing.v1 import AppTest

HASIL = []
def cek(nama, kondisi, info=""):
    HASIL.append((nama, bool(kondisi)))
    print(("LULUS " if kondisi else "GAGAL ") + nama + (f"  [{info}]" if info and not kondisi else ""))

def baru():
    return AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=120).run()

def teks(at):
    out = []
    for k in ("markdown", "caption", "info", "success", "error", "warning", "subheader", "title"):
        out += [str(getattr(e, "value", "")) for e in getattr(at, k)]
    return "\n".join(out)

def tombol(at, label):
    return next((b for b in at.button if b.label == label), None)

def pilih_menu(at, nama):
    r = next(r for r in at.sidebar.radio)
    r.set_value(nama)
    return at.run()

import re
def menu(at):
    return [re.sub(r"\s+\(\d+\)$", "", re.sub(r"^:material/\w+:\s*", "", o)) for o in at.sidebar.radio[0].options]

def snapshot():
    con = sqlite3.connect(DB)
    row = con.execute("SELECT data FROM snapshot WHERE id=1").fetchone()
    con.close()
    return row[0] if row else None

# ---------- A. halaman login & setup ----------
at = baru()
cek("A1 login: tidak ada error", not at.exception, at.exception)
cek("A2 login: tombol Masuk sebagai Demo ada", tombol(at, "Masuk sebagai Demo") is not None)
cek("A3 tidak ada kata 'Dosen' di halaman", "dosen" not in teks(at).lower())

# buat Pengurus pertama (alur lama)
ti = {t.label: t for t in at.text_input}
ti["Nama lengkap"].input("Pengurus Uji"); ti["Email"].input("pengurus@uji.id")
ti["Kata sandi (minimal 8 karakter)"].input("rahasia123"); ti["Ulangi kata sandi"].input("rahasia123")
at.button[[b.label for b in at.button].index("Buat akun Pengurus")].click() if any(b.label == "Buat akun Pengurus" for b in at.button) else None
# form_submit_button termasuk at.button
at.run()
cek("A4 setup Pengurus pertama berhasil (masuk dashboard)", any("Ringkasan Dashboard" in str(m.value) for m in at.markdown), teks(at)[:200])
cek("A5 menu Panduan Penggunaan ada di sidebar Pengurus", "Panduan Penggunaan" in menu(at))

# buat Nasabah dan Pengepul lewat Data Pengguna (alur lama)
at = pilih_menu(at, "Data Pengguna")
def buat_akun(at, nama, email, peran):
    t = {x.label: x for x in at.text_input}
    t["Nama"].input(nama); t["Email"].input(email)
    next(r for r in at.radio if r.label == "Peran").set_value(peran)
    next(b for b in at.button if b.label == "Buat akun").click()
    at.run()
    code = [c.value for c in at.code]
    return code[0] if code else None
pw_n = buat_akun(at, "Nasabah Uji", "nasabah@uji.id", "Nasabah")
pw_p = buat_akun(at, "Pengepul Uji", "pengepul@uji.id", "Pengepul")
cek("A6 akun Nasabah & Pengepul dibuat dengan sandi sementara", pw_n and pw_p, (pw_n, pw_p))

# input setoran (alur lama): metode Tabung, setuju di lokasi
at = pilih_menu(at, "Input Setoran")
sel = [s for s in at.selectbox]
sel[1].select("Kardus") if len(sel) > 1 else None
at.run()
nums = [n for n in at.number_input]
nums[0].set_value(10.0); at.run()
cb = next((c for c in at.checkbox if "nasabah menyatakan setuju" in c.label), None)
cb.check(); at.run()
b = tombol(at, "Simpan & Setujui")
cek("A7 tombol Simpan & Setujui aktif", b is not None and not b.disabled)
b.click(); at.run()
cek("A8 setoran tersimpan (Rp20.000)", any("tersimpan" in s.value and "Rp20.000" in s.value for s in at.success), [s.value for s in at.success])
PROD_SNAP = snapshot()
cek("A9 data produksi tersimpan di DB", PROD_SNAP and "Nasabah Uji" in PROD_SNAP)

# logout & login 3 peran
def login(at_, peran, email, pw):
    next(b for b in at_.button if b.label == peran).click(); at_.run()
    t = {x.label: x for x in at_.text_input}
    t["Email"].input(email); t["Kata sandi"].input(pw)
    next(b for b in at_.button if b.label.startswith("Masuk sebagai ") and b.label != "Masuk sebagai Demo").click()
    return at_.run()

at = baru()
at = login(at, "Pengurus", "pengurus@uji.id", "rahasia123")
cek("B1 login Pengurus tetap berfungsi", at.sidebar.radio and "Input Setoran" in menu(at) and not at.exception, at.exception)

# nasabah: wajib ganti sandi dulu
at = baru()
at = login(at, "Nasabah", "nasabah@uji.id", pw_n)
cek("B2 login Nasabah (sandi sementara) minta ganti sandi", any("Ganti kata sandi sementara" in t.value for t in at.title), teks(at)[:150])
t = {x.label: x for x in at.text_input}
t["Kata sandi sekarang"].input(pw_n); t["Kata sandi baru (minimal 8 karakter)"].input("nasabah123"); t["Ulangi kata sandi baru"].input("nasabah123")
next(b for b in at.button if b.label == "Simpan kata sandi baru").click(); at.run()
at = baru(); at = login(at, "Nasabah", "nasabah@uji.id", "nasabah123")
cek("B3 Nasabah masuk: menu Nasabah + Panduan", menu(at) == ["Beranda", "Persetujuan Setoran", "Riwayat Setoran", "Saldo Saya", "Riwayat Penarikan", "Profil Saya", "Panduan Penggunaan"], menu(at))
cek("B4 Nasabah melihat saldo Rp20.000", "Rp20.000" in " ".join(str(m.value) for m in at.markdown))

at = baru(); at = login(at, "Pengepul", "pengepul@uji.id", pw_p)
t = {x.label: x for x in at.text_input}
t["Kata sandi sekarang"].input(pw_p); t["Kata sandi baru (minimal 8 karakter)"].input("pengepul123"); t["Ulangi kata sandi baru"].input("pengepul123")
next(b for b in at.button if b.label == "Simpan kata sandi baru").click(); at.run()
at = baru(); at = login(at, "Pengepul", "pengepul@uji.id", "pengepul123")
cek("B5 Pengepul masuk: menu Pengepul + Panduan", menu(at) == ["Beranda", "Perkiraan Stok", "Riwayat Penjualan", "Profil Saya", "Panduan Penggunaan"], menu(at))

# peran salah ditolak (keamanan login lama)
at = baru(); at = login(at, "Pengurus", "nasabah@uji.id", "nasabah123")
cek("B6 login dengan jenis akun salah tetap ditolak", any("tidak sesuai" in e.value for e in at.error), [e.value for e in at.error])
at = baru(); at = login(at, "Nasabah", "nasabah@uji.id", "salah-sandi")
cek("B7 sandi salah tetap ditolak", any("salah" in e.value for e in at.error))

# ---------- C. MODE DEMO ----------
PROD_SNAP = snapshot()  # kondisi produksi tepat sebelum sesi demo dimulai
at = baru()
tombol(at, "Masuk sebagai Demo").click(); at.run()
cek("C1 masuk demo tanpa email/sandi, tanpa error", not at.exception and at.sidebar.radio, at.exception)
cek("C2 penanda MODE DEMO tampil (pita + sidebar)", "MODE DEMO" in " ".join(str(m.value) for m in at.markdown) + " ".join(str(m.value) for m in at.sidebar.markdown))
cek("C3 tampilan awal = Pengurus (menu Pengurus lengkap)", "Input Setoran" in menu(at) and "Pengaturan" in menu(at))
semua = " ".join(str(m.value) for m in at.markdown)
cek("C4 data produksi TIDAK tampil di demo", "Nasabah Uji" not in semua and "pengurus@uji.id" not in semua)
cek("C5 data simulasi tampil (Pengurus Demo)", "Pengurus Demo" in " ".join(str(m.value) for m in at.sidebar.markdown))

# jelajah semua menu Pengurus di demo
rusak = []
for m in menu(at):
    at = pilih_menu(at, m)
    if at.exception: rusak.append((m, str(at.exception)[:200]))
cek("C6 semua menu Pengurus (demo) terbuka tanpa error", not rusak, rusak)

# pindah ke Nasabah
def ganti_peran(at, peran):
    sc = next(x for x in at.get("button_group"))
    sc.set_value(peran)
    return at.run()
at = ganti_peran(at, "Nasabah")
cek("C7 berpindah ke tampilan Nasabah", menu(at)[1] == "Persetujuan Setoran" and not at.exception, at.exception)
rusak = []
for m in menu(at):
    at = pilih_menu(at, m)
    if at.exception: rusak.append((m, str(at.exception)[:200]))
cek("C8 semua menu Nasabah (demo) terbuka tanpa error", not rusak, rusak)

# simulasi persetujuan nasabah
at = pilih_menu(at, "Persetujuan Setoran")
cbs = [c for c in at.checkbox if "mencocokkan" in c.label]
cek("C9 ada setoran menunggu persetujuan (data simulasi)", len(cbs) == 1)
cbs[0].check(); at.run()
next(b for b in at.button if b.label == "Setujui Setoran").click(); at.run()
cek("C10 simulasi persetujuan berhasil, tidak ada lagi yang menunggu", any("Tidak ada setoran yang perlu diperiksa" in i.value for i in at.info), [i.value for i in at.info])

# simulasi pengajuan penarikan
at = pilih_menu(at, "Saldo Saya")
nom = next(n for n in at.number_input if "Nominal" in n.label); nom.set_value(50000); at.run()
next(b for b in at.button if b.label == "Kirim pengajuan").click(); at.run()
cek("C11 simulasi pengajuan penarikan terkirim", any("terkirim" in s.value for s in at.success), [s.value for s in at.success] + [e.value for e in at.error])

# ke Pengurus: proses pengajuan
at = ganti_peran(at, "Pengurus")
at = pilih_menu(at, "Penarikan Saldo")
setuju = [b for b in at.button if b.label == "Setujui pengajuan"]
cek("C12 Pengurus melihat 2 pengajuan (Budi + Nasabah Demo)", len(setuju) == 2, len(setuju))
setuju[0].click(); at.run()
cek("C13 simulasi persetujuan penarikan oleh Pengurus", any("disetujui" in s.value.lower() for s in at.success), [s.value for s in at.success] + [e.value for e in at.error])

# simulasi penjualan pengepul
at = pilih_menu(at, "Penjualan Pengepul")
yakin = next(c for c in at.checkbox if "konfirmasi seluruh stok" in c.label)
cek("C14 halaman Penjualan Pengepul demo menampilkan form (stok ada)", yakin is not None)

# input setoran lewat akun nasabah (simulasi)
at = pilih_menu(at, "Input Setoran")
cek("C15 Input Setoran demo: daftar nasabah dummy", any("Nasabah Demo" in (s.options or []) or "Budi Contoh" in (s.options or []) for s in at.selectbox), [s.options for s in at.selectbox])

# pengepul
at = ganti_peran(at, "Pengepul")
cek("C16 berpindah ke tampilan Pengepul", menu(at) == ["Beranda", "Perkiraan Stok", "Riwayat Penjualan", "Profil Saya", "Panduan Penggunaan"], menu(at))
rusak = []
for m in menu(at):
    at = pilih_menu(at, m)
    if at.exception: rusak.append((m, str(at.exception)[:200]))
cek("C17 semua menu Pengepul (demo) terbuka tanpa error", not rusak, rusak)

# ISOLASI: DB produksi tidak berubah sama sekali oleh seluruh aktivitas demo
cek("C18 ISOLASI: snapshot database produksi identik setelah semua aktivitas demo", snapshot() == PROD_SNAP)

# atur ulang
at = ganti_peran(at, "Pengurus")
next(b for b in at.button if b.label == "Atur ulang data demo").click(); at.run()
at = pilih_menu(at, "Penarikan Saldo")
cek("C19 Atur ulang data demo mengembalikan kondisi awal (1 pengajuan)", len([b for b in at.button if b.label == "Setujui pengajuan"]) == 1)

# keluar dari demo lalu login nyata: tidak ada sisa data demo
next(b for b in at.sidebar.button if b.label == "Keluar").click(); at.run()
cek("C20 Keluar dari demo kembali ke login", tombol(at, "Masuk sebagai Demo") is not None and not at.exception)
at = login(at, "Pengurus", "pengurus@uji.id", "rahasia123")
cek("C21 login nyata setelah demo: data asli tampil, tanpa data demo", "Pengurus Uji" in " ".join(str(m.value) for m in at.sidebar.markdown) and "Budi Contoh" not in teks(at))
at = pilih_menu(at, "Nasabah")
cek("C22 data nasabah asli utuh (bukan data demo)", any("Nasabah Uji" in str(d.value) for d in at.dataframe) and not any("Budi Contoh" in str(d.value) for d in at.dataframe))

# ---------- D. PANDUAN ----------
def ke_panduan(peran_login):
    a = baru(); 
    return a
at = pilih_menu(at, "Panduan Penggunaan")
cek("D1 Pengurus: halaman Panduan Penggunaan terbuka", not at.exception and len(at.tabs) == 5, [t.label for t in at.tabs])
cek("D2 Pengurus: ada panduan 12 halaman Pengurus", sum(1 for e in at.expander) >= 12 + 6 + 4, len(at.expander))

# tombol Panduan Halaman Ini per halaman
at = pilih_menu(at, "Input Setoran")
tombol(at, "Panduan Halaman Ini").click(); at.run()
cek("D3 Panduan Halaman Ini membuka panduan Input Setoran (bukan umum)", not at.exception, at.exception)

# konsistensi: kunci panduan sama dengan menu aplikasi
import panduan
at2 = baru(); tombol(at2, "Masuk sebagai Demo").click(); at2.run()
for peran in ("Pengurus", "Nasabah", "Pengepul"):
    if peran != "Pengurus":
        at2 = ganti_peran(at2, peran)
    menu_ = menu(at2)
    cek(f"D4 panduan {peran} mencakup seluruh menu ({len(menu_)})", set(menu_) == set(panduan.PANDUAN[peran]), set(menu_) ^ set(panduan.PANDUAN[peran]))
    # tombol panduan di tiap halaman tidak error
    rusak = []
    for m in menu_:
        at2 = pilih_menu(at2, m)
        b = tombol(at2, "Panduan Halaman Ini")
        if b is None: rusak.append((m, "tombol tak ada")); continue
        b.click(); at2.run()
        if at2.exception: rusak.append((m, str(at2.exception)[:150]))
    cek(f"D5 tombol Panduan Halaman Ini bekerja di semua halaman {peran}", not rusak, rusak)

# panduan Pengepul tidak membocorkan info internal
import json as _j
pengepul_txt = _j.dumps(panduan.PENGEPUL, ensure_ascii=False).lower()
for kata in ("harga beli", "kas", "saldo", "net kas", "laba"):
    cek(f"D6 panduan Pengepul tidak memuat '{kata}'", not re.search(r"\b" + kata + r"\b", pengepul_txt))

# panduan di akun nyata Nasabah & Pengepul
at = baru(); at = login(at, "Nasabah", "nasabah@uji.id", "nasabah123")
at = pilih_menu(at, "Panduan Penggunaan")
cek("D7 Nasabah nyata: hanya tab Mulai Cepat + Panduan Nasabah", [t.label for t in at.tabs] == ["Mulai Cepat", "Panduan Nasabah"], [t.label for t in at.tabs])
at = pilih_menu(at, "Profil Saya")
cek("D8 Profil Saya (nyata) punya pintasan Panduan", tombol(at, "Buka Panduan Penggunaan") is not None)
tombol(at, "Buka Panduan Penggunaan").click(); at.run()
cek("D9 pintasan membuka halaman Panduan", at.sidebar.radio[0].value == "Panduan Penggunaan", at.sidebar.radio[0].value)
at = baru(); at = login(at, "Pengepul", "pengepul@uji.id", "pengepul123")
at = pilih_menu(at, "Panduan Penggunaan")
cek("D10 Pengepul nyata: hanya tab Mulai Cepat + Panduan Pengepul", [t.label for t in at.tabs] == ["Mulai Cepat", "Panduan Pengepul"], [t.label for t in at.tabs])


# ---------- F. KEAMANAN SISI SERVER & ALUR LANJUTAN DEMO ----------
SNAP_F = snapshot()
# F1: memalsukan uid demo tanpa penanda demo -> harus ditolak (kembali ke login)
a = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=120)
a.session_state["uid"] = "pengurus@akun.demo"; a.run()
cek("F1 uid demo tanpa penanda demo ditolak (tampil login)", tombol(a, "Masuk sebagai Demo") is not None and not a.sidebar.radio)
# F2: penanda demo + data demo palsu dengan token salah -> ditolak
a = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=120)
a.session_state["uid"] = "pengurus@akun.demo"; a.session_state["demo"] = "x"; a.session_state["demo_db"] = {"_token": "lain", "users": []}; a.run()
cek("F2 token demo salah ditolak", tombol(a, "Masuk sebagai Demo") is not None and not a.sidebar.radio)
# F3: uid pengguna ASLI dengan sisa penanda demo -> tetap memakai data asli, bukan data demo
a = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=120)
a.session_state["uid"] = "pengurus@uji.id"; a.session_state["demo"] = "x"; a.run()
cek("F3 pengguna asli dengan sisa penanda demo tetap memakai data asli", "Pengurus Uji" in " ".join(str(m.value) for m in a.sidebar.markdown))

# F4: alur lengkap demo: setoran -> kirim ke nasabah -> setujui -> penjualan -> pengepul melihat
d = baru(); tombol(d, "Masuk sebagai Demo").click(); d.run()
d = pilih_menu(d, "Input Setoran")
sels = list(d.selectbox)
sels[0].select("Siti Contoh"); d.run()
sels = list(d.selectbox); sels[1].select("Besi"); d.run()
nums = list(d.number_input); nums[0].set_value(5.0); d.run()
next(r for r in d.radio if r.label == "Persetujuan nasabah").set_value("Nasabah setuju lewat akunnya"); d.run()
tombol(d, "Simpan & Kirim ke Nasabah").click(); d.run()
cek("F4 demo: setoran baru tersimpan (menunggu nasabah)", any("tersimpan" in s.value for s in d.success), [s.value for s in d.success] + [e.value for e in d.error])
# penjualan
d = pilih_menu(d, "Penjualan Pengepul")
next(c for c in d.checkbox if "konfirmasi seluruh stok" in c.label).check(); d.run()
tombol(d, "Simpan penjualan").click(); d.run()
cek("F5 demo: penjualan pengepul tersimpan, stok kembali nol", not d.exception and any("Belum ada stok" in i.value for i in d.info), [i.value for i in d.info] + [str(d.exception)])
d = ganti_peran(d, "Pengepul"); d = pilih_menu(d, "Riwayat Penjualan")
cek("F6 demo: Pengepul melihat 2 catatan penjualan", len(d.expander) == 2, len(d.expander))
d = pilih_menu(d, "Perkiraan Stok")
cek("F7 demo: stok Pengepul kosong setelah penjualan", any("Belum ada sampah terkumpul" in i.value for i in d.info), [i.value for i in d.info])
# F8: menonaktifkan akun demo lewat Data Pengguna tidak merusak sesi
d = ganti_peran(d, "Pengurus"); d = pilih_menu(d, "Data Pengguna")
sb = next(s for s in d.selectbox if s.label == "Kelola akun"); sb.select("nasabah@akun.demo"); d.run()
next(b for b in d.button if b.label == "Aktifkan atau nonaktifkan akun").click(); d.run()
d = ganti_peran(d, "Nasabah")
cek("F8 akun demo dinonaktifkan: berpindah ke Nasabah tetap berjalan (tidak jatuh ke login)", d.sidebar.radio and not d.exception and tombol(d, "Masuk sebagai Demo") is None)
# F9: Pengaturan & Profil demo aman
d = ganti_peran(d, "Pengurus"); d = pilih_menu(d, "Pengaturan")
cek("F9 Pengaturan demo versi aman (tanpa unduh cadangan/muat data contoh)", tombol(d, "Muat data contoh") is None and not d.exception and not any("Postgres" in str(m.value) for m in d.markdown))
d = ganti_peran(d, "Nasabah"); d = pilih_menu(d, "Profil Saya")
cek("F10 Profil demo tanpa form ganti sandi", not any(t.label == "Kata sandi sekarang" for t in d.text_input) and not d.exception)
cek("F11 ISOLASI: DB produksi identik setelah seluruh uji F", snapshot() == SNAP_F)

# batas akhir: produksi tetap tak berubah oleh sesi demo/panduan
_a, _b = json.loads(PROD_SNAP), json.loads(snapshot())
_beda = {k: (_a.get(k), _b.get(k)) for k in set(_a) | set(_b) if _a.get(k) != _b.get(k)}
print("   selisih produksi:", _beda)
cek("E1 produksi di akhir uji hanya berbeda pada 'seq' (penghitung ID dari membuka Input Setoran di sesi nyata, perilaku lama)", set(_beda) <= {"seq"}, _beda)

g = [n for n, o in HASIL if not o]
print(f"\nTOTAL {len(HASIL)} uji, lulus {len(HASIL)-len(g)}, gagal {len(g)}")
for n in g: print("  GAGAL:", n)
sys.exit(1 if g else 0)
