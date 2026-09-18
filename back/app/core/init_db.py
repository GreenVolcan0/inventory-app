from app.core.database import session_local, engine, Base
from app.models import *
from app.services.auth import get_password_hash
from app.config import settings

def init_database():
    Base.metadata.create_all(bind=engine)
    
    db = session_local()
    
    try:
        if db.query(User).count() > 0:
            return

        super_admin = User(
            login=settings.INITIAL_ADMIN_LOGIN,
            first_name = "Андрей",
            last_name = "Петров",
            password_hash = get_password_hash(settings.INITIAL_ADMIN_PASSWORD),
            role=UserRole.super_admin
        )
        db.add(super_admin)
        db.commit()
    except Exception as e: db.rollback(); raise
    finally: db.close()