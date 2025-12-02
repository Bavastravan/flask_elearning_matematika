from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required, nocache
from app.models import Buku, MisiLevel, SoalMisi
from app.extensions import db

siswa_bp = Blueprint("siswa", __name__)

# ROOT
@siswa_bp.route("/")
@login_required
@role_required("siswa")
def siswa_root():
    return redirect(url_for("siswa.dashboard"))

# DASHBOARD
@siswa_bp.route("/dashboard")
@login_required
@role_required("siswa")
@nocache
def dashboard():
    level = getattr(current_user, "level", 1)
    poin = getattr(current_user, "poin", 0)
    kelas = getattr(current_user, "kelas", None)  # pastikan kolom ini ada di users

    # Ambil modul/buku sesuai kelas user, urut paling baru
    query = Buku.query
    if kelas is not None:
        query = query.filter_by(kelas=kelas)

    modul_list = (
    Buku.query
    .filter_by(kelas=kelas)
    .order_by(Buku.created_at.desc())
    .limit(8)
    .all()
)

    return render_template(
        "siswa/dashboard.html",
        level=level,
        poin=poin,
        modul_list=modul_list,
    )



# BUKU
@siswa_bp.route("/buku")
@login_required
@role_required("siswa")
@nocache
def buku():
    buku_list = Buku.query.order_by(Buku.kelas, Buku.judul).all()
    return render_template("siswa/buku.html", buku_list=buku_list)

# MISI LIST LEVEL
@siswa_bp.route("/misi")
@login_required
@role_required("siswa")
@nocache
def misi():
    misi_list = MisiLevel.query.order_by(MisiLevel.level).all()
    return render_template("siswa/misi.html", misi_list=misi_list)

# HALAMAN PER LEVEL
@siswa_bp.route("/misi/level/<int:level>")
@login_required
@role_required("siswa")
@nocache
def misi_level(level):
    misi = MisiLevel.query.filter_by(level=level).first()
    soal_list = (
        SoalMisi.query
        .filter_by(level=level)
        .order_by(SoalMisi.nomor.asc())
        .all()
    )
    return render_template(
        "siswa/level.html",
        level=level,
        misi=misi,
        soal_list=soal_list,
        feedback=None,   # awalnya belum ada feedback
    )

# SUBMIT JAWABAN MISI + FEEDBACK
@siswa_bp.route("/misi/level/<int:level>/submit", methods=["POST"])
@login_required
@role_required("siswa")
def submit_misi(level):
    soal_list = (
        SoalMisi.query
        .filter_by(level=level)
        .order_by(SoalMisi.nomor.asc())
        .all()
    )

    benar = 0
    total = len(soal_list)

    for soal in soal_list:
        jawaban = (request.form.get(f"jawaban_{soal.id}") or "").strip()

        if soal.kunci_pg:
            if jawaban.upper() == (soal.kunci_pg or "").upper():
                benar += 1
        elif soal.kunci_isian:
            if jawaban.lower() == soal.kunci_isian.lower():
                benar += 1

    nilai = int((benar / total) * 100) if total else 0

    # aturan poin
    if nilai == 100:
        tambahan_poin = 10
    elif nilai >= 80:
        tambahan_poin = 7
    elif nilai >= 60:
        tambahan_poin = 4
    else:
        tambahan_poin = 1

    # update poin user
    current_user.poin = (current_user.poin or 0) + tambahan_poin
    db.session.commit()

    feedback = (
        f"Wahhh! Selamat, jawaban kamu benar {benar}/{total}, "
        f"nilai kamu {nilai}. Kamu mendapat {tambahan_poin} poin!"
    )

    misi = MisiLevel.query.filter_by(level=level).first()

    return render_template(
        "siswa/level.html",
        level=level,
        misi=misi,
        soal_list=soal_list,
        feedback=feedback,
    )


# PROGRESS
from app.models import MisiLevel

@siswa_bp.route("/progress")
@login_required
@role_required("siswa")
@nocache
def progress():
    # data user asli
    level = getattr(current_user, "level", 1)
    poin_total = getattr(current_user, "poin", 0)

    # ambil semua level yang ada di tabel misi_level
    misi_list = MisiLevel.query.order_by(MisiLevel.level).all()

    # label: Level 1, Level 2, ...
    labels = [f"Level {m.level}" for m in misi_list]

    # nilai batang: misalnya target poin per level (100), atau 0 kalau mau kosong dulu
    # kalau kamu sudah punya logika poin per level, ganti bagian ini
    values = [100 for _ in misi_list]

    return render_template(
        "siswa/progress.html",
        level=level,
        poin=poin_total,
        labels=labels,
        values=values,
    )


# PROFIL
@siswa_bp.route("/profil")
@login_required
@role_required("siswa")
@nocache
def profil():
    return render_template("siswa/profil.html")
