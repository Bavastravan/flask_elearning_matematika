from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import current_user
from app.extensions import db
from app.models.user import User
from app.blueprints.auth import auth_bp


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

        print("DEBUG nama_sekolah:", repr(nama_sekolah))
    


        # (opsional) validasi checkbox juga di server
        cookie_consent = request.form.get("cookie_consent")
        parent_consent = request.form.get("parent_consent")

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

        # 2. Cek email sudah dipakai atau belum
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email sudah terdaftar, silakan gunakan email lain atau masuk.", "warning")
            return render_template("auth/register.html")

        # 3. Hash password
        password_hash = generate_password_hash(password)

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

        flash("Pendaftaran berhasil! Silakan masuk dengan email dan password Anda.", "success")
        return redirect(url_for("auth.login"))

    # GET: tampilkan form
    return render_template("auth/register.html")
