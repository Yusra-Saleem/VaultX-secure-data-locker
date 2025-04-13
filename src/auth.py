import hashlib
import json
from pathlib import Path
import time

class Auth:
    """Authentication handler for VaultX"""
    
    def __init__(self):
        """Initialize authentication state"""
        self._authenticated = False
        self._users = {}
        self._current_user = None
        self._users_file = Path(__file__).parent / 'data' / 'users.json'
        
        # Create data directory if it doesn't exist
        self._users_file.parent.mkdir(exist_ok=True)
        
        # Load existing users
        self._load_users()

    def _load_users(self):
        """Load users from JSON file"""
        try:
            if self._users_file.exists():
                with open(self._users_file, 'r') as f:
                    self._users = json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            self._users = {}

    def _save_users(self):
        """Save users to JSON file"""
        try:
            with open(self._users_file, 'w') as f:
                json.dump(self._users, f, indent=4)
        except Exception as e:
            print(f"Error saving users: {e}")

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str, email: str = "") -> tuple[bool, str]:
        """Register a new user"""
        if not username or not password:
            return False, "Username and password are required"
        
        if username in self._users:
            return False, "Username already exists"
        
        # Hash password and store user
        hashed_password = self._hash_password(password)
        self._users[username] = {
            "password": hashed_password,
            "email": email,
            "created_at": time.time()
        }
        
        # Save updated users
        self._save_users()
        return True, "Registration successful! Please login."

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate a user"""
        if not username or not password:
            return False, "Username and password are required"
        
        if username not in self._users:
            return False, "User not found"
        
        hashed_password = self._hash_password(password)
        if self._users[username]["password"] != hashed_password:
            return False, "Invalid password"
        
        self._authenticated = True
        self._current_user = username
        return True, "Login successful!"

    def logout(self):
        """Log out current user"""
        self._authenticated = False
        self._current_user = None

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self._authenticated

    def get_current_user(self) -> str:
        """Get current user's username"""
        return self._current_user