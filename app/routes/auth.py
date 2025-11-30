from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.utils.security import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Kalau sudah login, tidak perlu daftar lagi
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        nama_sekolah = request.form.get("nama_sekolah", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        role = "siswa"  # dikunci siswa SD

        cookie_consent = request.form.get("cookie_consent")
        parent_consent = request.form.get("parent_consent")

        # Debug cek value nama_sekolah
        print("DEBUG nama_sekolah:", repr(nama_sekolah))

        # 1. Validasi dasar
        if not nama or not email or not password or not password_confirm:
            flash("Semua kolom wajib diisi (kecuali nama sekolah).", "danger")
            return render_template("auth/register.html")

        if password != password_confirm:
            flash("Password dan konfirmasi password tidak sama.", "danger")
            return render_template("auth/register.html")

        if not cookie_consent or not parent_consent:
            flash("Harap menyetujui cookie dan pernyataan pendamping orang tua.", "danger")
            return render_template("auth/register.html")

        # 2. Cek email sudah terdaftar
        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar, silakan gunakan email lain atau masuk.", "warning")
            return render_template("auth/register.html")

        # 3. Hash password (pakai util milikmu)
        password_hash = hash_password(password)

        # 4. Buat user baru dan simpan ke database
        user = User(
            nama=nama,
            email=email,
            password_hash=password_hash,
            role=role,
            nama_sekolah=nama_sekolah or None,
        )
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Kalau sudah login, tidak perlu ke halaman login lagi
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(user.password_hash, password):
            flash("Email atau password salah.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Berhasil login.", "success")
        return redirect(url_for("main.index"))

    # GET: tampilkan form login
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return render_template("auth/forgot_password.html")
