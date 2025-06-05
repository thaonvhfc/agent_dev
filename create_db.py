#!/usr/bin/env python3
"""
Script để tạo database và admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine, SessionLocal
from app.auth import get_password_hash
from app.database import User

def create_database():
    """Tạo tất cả tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_admin_user():
    """Tạo admin user"""
    db = SessionLocal()
    try:
        # Kiểm tra xem admin đã tồn tại chưa
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Tạo admin user
        hashed_password = get_password_hash("admin123")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=hashed_password,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        
        # Tạo user thường
        user_password = get_password_hash("user123")
        regular_user = User(
            username="user",
            email="user@example.com",
            password_hash=user_password,
            is_admin=False
        )
        
        db.add(regular_user)
        db.commit()
        print("Regular user created successfully!")
        print("Username: user")
        print("Password: user123")
        
    except Exception as e:
        print(f"Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_database()
    create_admin_user()