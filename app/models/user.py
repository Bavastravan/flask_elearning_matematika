from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="siswa")

    # tambahan profil
    nama_sekolah = db.Column(db.String(150), nullable=True)
    kelas = db.Column(db.Integer, nullable=True)  # 1–6
    poin = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
