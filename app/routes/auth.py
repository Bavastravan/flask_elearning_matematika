from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.utils.security import hash_password, verify_password


auth_bp = Blueprint("auth", __name__)


def nocache(view_func):
    def wrapper(*args, **kwargs):
        resp = make_response(view_func(*args, **kwargs))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    wrapper.__name__ = view_func.__name__
    return wrapper


@auth_bp.route("/register", methods=["GET", "POST"])
@nocache
def register():
    # Kalau sudah login, tidak perlu daftar lagi
    if current_user.is_authenticated:
        # Bisa diarahkan langsung ke dashboard sesuai role
        if current_user.role == "siswa":
            return redirect(url_for("siswa.dashboard"))
        elif current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))
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

        # 3. Hash password
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
@nocache
def login():
    # Kalau sudah login dan buka /auth/login atau klik "Mulai Belajar"
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

    return render_template("auth/login.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@nocache
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        new_password = request.form.get("new_password", "")
        new_password_confirm = request.form.get("new_password_confirm", "")

        # cek user
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email tidak terdaftar.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # validasi password baru
        if len(new_password) < 8 or new_password != new_password_confirm:
            flash("Password baru minimal 8 karakter dan harus sama di kedua kolom.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # update password
        user.password_hash = hash_password(new_password)
        db.session.commit()

        flash("Password berhasil diubah. Silakan login dengan password baru.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")

@auth_bp.route("/logout")
@login_required
@nocache
def logout():
    logout_user()
    session.clear()
    flash("Anda telah logout.", "info")
    
    # Buat response baru tanpa history parameter
    response = make_response(redirect(url_for("main.index")))
    response.headers["Clear-Site-Data"] = '"cache", "cookies", "storage"'
    return response

