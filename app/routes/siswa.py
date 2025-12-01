from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required, nocache

# Blueprint siswa (prefix biasanya /siswa)
siswa_bp = Blueprint("siswa", __name__)

# ============================================================
# ROOT → REDIRECT KE DASHBOARD
# ============================================================
@siswa_bp.route("/")
@login_required
@role_required("siswa")
def siswa_root():
    return redirect(url_for("siswa.dashboard"))

# ============================================================
# DASHBOARD (SATU SAJA)
# ============================================================
@siswa_bp.route("/dashboard")
@login_required
@role_required("siswa")
@nocache
def dashboard():
    """
    Dashboard utama siswa.
    Mengambil level & rata-rata nilai dari current_user
    dan daftar modul latihan.
    """
    level = getattr(current_user, "level", 1)
    rata_rata = getattr(current_user, "rata_rata", 0)

    modul_list = [
        {
            "nama": "Penjumlahan & Pengurangan",
            "deskripsi": "Bilangan 1–100 · 8 latihan",
        },
        {
            "nama": "Perkalian Dasar",
            "deskripsi": "Tabel 1–10 · 6 latihan",
        },
        {
            "nama": "Soal Cerita",
            "deskripsi": "Latihan pemahaman · 4 latihan",
        },
        {
            "nama": "Pecahan Sederhana",
            "deskripsi": "Perkenalan pecahan · 3 latihan",
        },
    ]

    return render_template(
        "siswa/dashboard.html",
        level=level,
        rata_rata=rata_rata,
        modul_list=modul_list,
    )

# ============================================================
# BUKU
# ============================================================
@siswa_bp.route("/buku")
@login_required
@role_required("siswa")
@nocache
def buku():
    return render_template("siswa/buku.html")

# ============================================================
# MISI → LIST LEVEL
# ============================================================
@siswa_bp.route("/misi")
@login_required
@role_required("siswa")
@nocache
def misi():
    """
    Menampilkan daftar level misi.
    """
    return render_template("siswa/misi.html")

# ============================================================
# HALAMAN PER LEVEL MISI
# ============================================================
@siswa_bp.route("/misi/level/<int:level>")
@login_required
@role_required("siswa")
@nocache
def misi_level(level):
    """
    Halaman soal untuk setiap level 1–10.
    """
    return render_template("siswa/level.html", level=level)

# ============================================================
# PROGRESS
# ============================================================
@siswa_bp.route("/progress")
@login_required
@role_required("siswa")
@nocache
def progress():
    # Ambil progres siswa (sementara dummy)
    level = getattr(current_user, "level", 1)
    rata_rata = getattr(current_user, "rata_rata", 0)

    return render_template(
        "siswa/progress.html",
        level=level,
        rata_rata=rata_rata,
    )

@siswa_bp.route('/profil')
def profil():
    return render_template('siswa/profil.html')

# ============================================================
# SUBMIT JAWABAN MISI
# ============================================================
@siswa_bp.route("/misi/level/<int:level>/submit", methods=["POST"])
@login_required
@role_required("siswa")
def submit_misi(level):
    """
    Menerima jawaban siswa (20 soal),
    nanti bisa disimpan ke database.
    """

    # Ambil 20 input jawaban dari form
    jawaban = {}
    for i in range(1, 21):
        jawaban[f"jawaban_{i}"] = request.form.get(f"jawaban_{i}", "").strip()

    # -------- DUMMY SAVE (sementara) ----------
    print("\n=== JAWABAN DITERIMA ===")
    print("User:", getattr(current_user, "id", None))
    print("Level:", level)
    for k, v in jawaban.items():
        print(f"{k}: {v}")
    print("==========================\n")

    flash("Jawaban kamu berhasil dikirim!", "success")

    return redirect(url_for("siswa.misi_level", level=level))
