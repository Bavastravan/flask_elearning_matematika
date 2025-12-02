from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required, nocache
from app.extensions import db
from app.models import User, Buku, MisiLevel
from app.models import User, Buku, MisiLevel, SoalMisi
import os
from flask import current_app
from werkzeug.utils import secure_filename


admin_bp = Blueprint("admin", __name__)

# DASHBOARD
@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
@nocache
def dashboard():
    return render_template("admin/dashboard.html")

# DATA SISWA + SEARCH
@admin_bp.route("/siswa")
@login_required
@role_required("admin")
@nocache
def data_siswa():
    q = request.args.get("q", "").strip()

    query = User.query.filter(User.role == "siswa")

    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                User.nama.ilike(like),
                User.nama_sekolah.ilike(like),
            )
        )

    users = query.order_by(User.nama.asc()).all()

    return render_template("admin/data_siswa.html", users=users, q=q)

@admin_bp.route("/siswa/<int:user_id>/hapus", methods=["POST"])
@login_required
@role_required("admin")
def hapus_siswa(user_id):
    admin_pwd = request.form.get("admin_password", "")

    if not current_user.check_password(admin_pwd):
        flash("Password admin salah. Aksi blokir dibatalkan.", "error")
        return redirect(url_for("admin.data_siswa"))

    user = User.query.get_or_404(user_id)
    if user.role != "siswa":
        flash("Hanya akun siswa yang bisa dihapus dari menu ini.", "error")
        return redirect(url_for("admin.data_siswa"))

    db.session.delete(user)
    db.session.commit()
    flash("Akun siswa berhasil diblokir dan dihapus.", "success")
    return redirect(url_for("admin.data_siswa"))

# MODUL & MISI (GET)
@admin_bp.route("/modul")
@login_required
@role_required("admin")
@nocache
def modul_misi():
    buku_list = Buku.query.order_by(Buku.kelas, Buku.judul).all()
    misi_list = MisiLevel.query.order_by(MisiLevel.level).all()
    return render_template(
        "admin/modul_misi.html",
        buku_list=buku_list,
        misi_list=misi_list,
    )

# TAMBAH BUKU
@admin_bp.route("/modul/buku/tambah", methods=["POST"])
@login_required
@role_required("admin")
def tambah_buku():
    judul = request.form.get("judul", "").strip()
    kelas = request.form.get("kelas")
    jumlah_halaman = request.form.get("jumlah_halaman")
    penerbit = request.form.get("penerbit", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()

    cover_file = request.files.get("cover")
    file_buku = request.files.get("file_buku")

    cover_path = None
    file_path = None

    # path dasar static
    static_root = os.path.join(current_app.root_path, "static")

    # simpan cover
    if cover_file and cover_file.filename:
        covers_dir = os.path.join(static_root, "covers")
        os.makedirs(covers_dir, exist_ok=True)

        filename = secure_filename(cover_file.filename)
        cover_path = os.path.join("covers", filename)  # disimpan di DB
        cover_file.save(os.path.join(static_root, cover_path))

    # simpan file buku
    if file_buku and file_buku.filename:
        print("DEBUG file_buku:", file_buku.filename)
        files_dir = os.path.join(static_root, "files")
        os.makedirs(files_dir, exist_ok=True)

        filename = secure_filename(file_buku.filename)
        file_path = os.path.join("files", filename)
        file_buku.save(os.path.join(static_root, file_path))

    # normalisasi path (backslash → slash)
    if cover_path:
        cover_path = cover_path.replace("\\", "/")
    if file_path:
        file_path = file_path.replace("\\", "/")

    buku = Buku(
        judul=judul,
        kelas=int(kelas),
        jumlah_halaman=int(jumlah_halaman),
        penerbit=penerbit or None,
        deskripsi=deskripsi or None,
        cover_path=cover_path,
        file_path=file_path,
    )
    db.session.add(buku)
    db.session.commit()

    flash("Buku berhasil ditambahkan.", "success")
    return redirect(url_for("admin.modul_misi"))


# TAMBAH / UPDATE MISI LEVEL
@admin_bp.route("/modul/misi-level/tambah", methods=["POST"])
@login_required
@role_required("admin")
def tambah_misi_level():
    level = request.form.get("level", "").strip()
    judul_misi = request.form.get("judul_misi", "").strip()
    jumlah_soal = request.form.get("jumlah_soal", "").strip()
    deskripsi_misi = request.form.get("deskripsi_misi", "").strip()

    if not level or not judul_misi or not jumlah_soal:
        flash("Level, judul misi, dan jumlah soal wajib diisi.", "error")
        return redirect(url_for("admin.modul_misi"))

    level_int = int(level)

    misi = MisiLevel.query.filter_by(level=level_int).first()
    if not misi:
        misi = MisiLevel(level=level_int)

    misi.judul = judul_misi
    misi.jumlah_soal = int(jumlah_soal)
    misi.deskripsi = deskripsi_misi or None

    db.session.add(misi)
    db.session.commit()
    flash(f"Misi level {level_int} berhasil disimpan/diupdate.", "success")
    return redirect(url_for("admin.modul_misi"))


@admin_bp.route("/nilai/soal-level/simpan", methods=["POST"])
@login_required
@role_required("admin")
def simpan_soal_level():
    level = request.form.get("level", "").strip()
    catatan_level = request.form.get("catatan_level", "").strip()

    if not level:
        flash("Level misi wajib dipilih.", "error")
        return redirect(url_for("admin.nilai_laporan"))

    level_int = int(level)

    # Hapus semua soal lama di level ini
    SoalMisi.query.filter_by(level=level_int).delete()

    nomor = 1  # penomoran baru, berapa pun soal yang terisi

    # Loop 1–20 sesuai form, tapi skip yang kosong
    for i in range(1, 21):
        teks_soal = (request.form.get(f"soal_{i}") or "").strip()
        if not teks_soal:
            continue  # kalau teks kosong, soal ini di-skip

        opsi_a = (request.form.get(f"opsi_{i}_A") or "").strip() or None
        opsi_b = (request.form.get(f"opsi_{i}_B") or "").strip() or None
        opsi_c = (request.form.get(f"opsi_{i}_C") or "").strip() or None
        opsi_d = (request.form.get(f"opsi_{i}_D") or "").strip() or None
        kunci_pg = (request.form.get(f"kunci_pg_{i}") or "").strip() or None
        kunci_isian = (request.form.get(f"kunci_isian_{i}") or "").strip() or None

        soal = SoalMisi(
            level=level_int,
            nomor=nomor,              # urut tanpa bolong
            teks_soal=teks_soal,
            opsi_a=opsi_a,
            opsi_b=opsi_b,
            opsi_c=opsi_c,
            opsi_d=opsi_d,
            kunci_pg=kunci_pg,
            kunci_isian=kunci_isian,
        )
        db.session.add(soal)
        nomor += 1

    db.session.commit()
    flash(f"Soal untuk level {level_int} berhasil disimpan ({nomor-1} soal).", "success")
    return redirect(url_for("admin.nilai_laporan"))


# PENGATURAN
@admin_bp.route("/pengaturan")
@login_required
@role_required("admin")
@nocache
def pengaturan():
    return render_template("admin/pengaturan.html")

@admin_bp.route("/laporan")
@login_required
@role_required("admin")
@nocache
def nilai_laporan():
    return render_template("admin/nilai_laporan.html")


