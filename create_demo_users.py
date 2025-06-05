#!/usr/bin/env python3
"""
Script để tạo demo users cho hệ thống
"""

from app.database import SessionLocal, create_tables, User
from app.auth import get_password_hash

def create_demo_users():
    """Tạo demo users"""
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Kiểm tra và tạo admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            print("✅ Tạo admin user: admin/admin123")
        else:
            print("ℹ️  Admin user đã tồn tại")
        
        # Kiểm tra và tạo demo user
        user = db.query(User).filter(User.username == "user").first()
        if not user:
            demo_user = User(
                username="user",
                password_hash=get_password_hash("user123"),
                role="user"
            )
            db.add(demo_user)
            print("✅ Tạo demo user: user/user123")
        else:
            print("ℹ️  Demo user đã tồn tại")
        
        db.commit()
        print("\n🎉 Demo users đã sẵn sàng!")
        print("Admin: admin/admin123 (có thể upload PDF)")
        print("User: user/user123 (chỉ chat)")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_users()