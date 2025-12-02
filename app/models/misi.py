from app.extensions import db

class MisiLevel(db.Model):
    __tablename__ = "misi_level"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, unique=True, nullable=False)  # 1–10
    judul = db.Column(db.String(255), nullable=False)
    jumlah_soal = db.Column(db.Integer, nullable=False, default=20)
    deskripsi = db.Column(db.Text)

    def __repr__(self):
        return f"<MisiLevel {self.level}>"
