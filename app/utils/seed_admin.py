from app.extensions import db
from app.models import User
from app.utils.security import hash_password

def create_default_admin():
    admin_email = "admin@elearning-math.local"
    admin_name = "Admin E-Learning"
    admin_password = "admin123"  

    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print("[INFO] Admin sudah ada:", existing.email)
        return

    admin = User(
        nama=admin_name,
        email=admin_email,
        password_hash=hash_password(admin_password),
        role="admin",
           )
    db.session.add(admin)
    db.session.commit()
    print("[INFO] Admin default dibuat:", admin_email)
