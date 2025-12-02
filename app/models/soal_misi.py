from app.extensions import db

class SoalMisi(db.Model):
    __tablename__ = "soal_misi"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False, index=True)
    nomor = db.Column(db.Integer, nullable=False)  # 1–20 per level

    teks_soal = db.Column(db.Text, nullable=False)

    opsi_a = db.Column(db.Text)
    opsi_b = db.Column(db.Text)
    opsi_c = db.Column(db.Text)
    opsi_d = db.Column(db.Text)

    kunci_pg = db.Column(db.String(1))      # 'A' / 'B' / 'C' / 'D'
    kunci_isian = db.Column(db.Text)        # untuk soal cerita / isian

    __table_args__ = (
        db.UniqueConstraint("level", "nomor", name="uq_soal_misi_level_nomor"),
    )

    def __repr__(self):
        return f"<SoalMisi L{self.level} No{self.nomor}>"
