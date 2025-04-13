import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple, Optional
import time
from datetime import datetime
import streamlit as st
from streamlit.components.v1 import html

class AuthUtils:
    def __init__(self):
        self.db_path = Path(__file__).parent / 'data' / 'user_db.json'
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Create empty DB if doesn't exist
        if not self.db_path.exists():
            with open(self.db_path, 'w') as f:
                json.dump({}, f)

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self) -> Dict:
        """Load users from database"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}

    def save_users(self, users: Dict) -> bool:
        """Save users to database"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(users, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False

    def verify_login(self, username: str, password: str) -> Tuple[bool, str]:
        """Verify login credentials"""
        if not username or not password:
            return False, "Username and password are required"

        users = self.load_users()
        
        if username not in users:
            return False, "User not found"
        
        hashed_password = self.hash_password(password)
        if users[username]["password"] != hashed_password:
            return False, "Invalid password"

        # Update last login time
        users[username]["last_login"] = str(datetime.now())
        self.save_users(users)
        
        return True, "Login successful!"

    def register_user(self, username: str, password: str, confirm_password: str, email: str) -> Tuple[bool, str]:
        """Register a new user with validation"""
        # Input validation
        if not username or not password or not email:
            return False, "All fields are required"
        
        if password != confirm_password:
            return False, "Passwords do not match"

        # Load existing users
        users = self.load_users()
        
        # Check if username exists
        if username in users:
            return False, "Username already exists"

        # Create new user with hashed password
        users[username] = {
            "password": self.hash_password(password),
            "email": email,
            "created_at": str(datetime.now()),
            "last_login": None
        }

        # Save to file
        if not self.save_users(users):
            return False, "Error saving user data"

        return True, "Registration successful! Please login."