from datetime import datetime
from app.extensions import db

class RiwayatMisi(db.Model):
    __tablename__ = "riwayat_misi"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    level = db.Column(db.Integer, nullable=False)         # level misi yang dikerjakan
    nilai = db.Column(db.Integer, nullable=False)         # 0–100
    poin_didapat = db.Column(db.Integer, nullable=False)  # misal 10 kalau nilai 100
    selesai_pada = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RiwayatMisi user={self.user_id} level={self.level} nilai={self.nilai}>"
