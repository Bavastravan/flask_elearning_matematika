from datetime import datetime
from app.extensions import db


class Buku(db.Model):
    __tablename__ = "buku"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    kelas = db.Column(db.Integer, nullable=False)  # 1,2,3,... sesuai kelas siswa
    jumlah_halaman = db.Column(db.Integer, nullable=False)
    penerbit = db.Column(db.String(255))
    deskripsi = db.Column(db.Text)
    cover_path = db.Column(db.String(255))  # contoh: "covers/nama-file.jpg"
    file_path = db.Column(db.String(255))   # contoh: "files/nama-file.pdf"

    # opsional tapi disarankan, untuk mengurutkan buku paling baru
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Buku {self.judul}>"
