# src/main.py

from turtle import position
import streamlit as st
import sys
from pathlib import Path
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time
import json
from streamlit.components.v1 import html
import os
import hashlib
import base64
import pyperclip  # Add this import at the top of your file

# File to store user data
USER_DATA_FILE = "user_data.json"
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user data
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Function to save user data
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to register a new user
def register_user(username, password, email):
    user_data = load_user_data()
    
    if username in user_data:
        return False, "Username already exists"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    hashed_password = hash_password(password)
    
    user_data[username] = {
        "password": hashed_password,
        "email": email
    }
    
    save_user_data(user_data)
    return True, "Registration successful"

# Function to authenticate user
def authenticate_user(username, password):
    user_data = load_user_data()
    
    if username not in user_data:
        return False, "User not found. Please register first."
    
    hashed_password = hash_password(password)
    
    if user_data[username]["password"] != hashed_password:
        return False, "Incorrect password"
    
    return True, "Login successful"

def validate_credentials(username: str, password: str) -> bool:
    """
    Validate user login credentials
    
    Args:
        username (str): The username to validate
        password (str): The password to validate
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    # TODO: Replace with secure authentication logic
    # This is just a basic example - don't use in production!
    
    # You should:
    # 1. Never store passwords in plain text
    # 2. Use password hashing (e.g., bcrypt)
    # 3. Store credentials in a secure database
    # 4. Use environment variables or Streamlit secrets for sensitive data
    
    valid_credentials = {
        "admin": "secretpassword123"
    }
    
    return username in valid_credentials and valid_credentials[username] == password

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="VaultX | Secure Data Locker",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/VaultX',
        'Report a bug': "https://github.com/yourusername/VaultX/issues",
        'About': "### VaultX - Your Secure Data Locker\nBuilt with Streamlit and ❤️"
    }
)

@st.cache_data  # Cache the animation loading
def load_lottie_url(url: str):
    """Load Lottie animation from URL with error handling"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading animation: {str(e)}")
        return None

# Update with reliable Lottie animation URLs
lottie_loading = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_x62chJ.json")
lottie_success = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_error = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_kxsd2ytq.json")

def setup_styling():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        /* Global Styles */
        * {
            font-family: 'Poppins', sans-serif;
            color: #E2E8F0;
        }

        /* Clean Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #020617 0%, #0F172A 50%, #1E3A8A 100%) !important;
        }

        /* Streamlit Element Cleanup */
        #MainMenu, footer, header {
            display: none !important;
        }

        /* Content Container with Enhanced Glass Effect */
        .block-container {
            background: none;
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
        }

        /* Card Container with Glowing Border */
        .card {
            background: rgba(15, 23, 42, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }

        /* Headers with Enhanced Glow */
        h1, h2, h3 {
            color: #E2E8F0 !important;
            text-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(to right, #60A5FA, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Clean Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.9);
            border-right: 1px solid rgba(59, 130, 246, 0.2);
        }

        /* Enhanced Button Styling with Glow */
        .stButton > button {
            background: linear-gradient(45deg, rgba(37, 99, 235, 0.9), rgba(59, 130, 246, 0.9));
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            letter-spacing: 0.025em;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
            background: linear-gradient(45deg, rgba(37, 99, 235, 1), rgba(59, 130, 246, 1));
        }

        /* Input Fields and Dropdowns */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stMultiselect > div > div > div {
            background: rgba(15, 23, 42, 0.95) !important; /* Dark background */
            color: #E2E8F0 !important; /* Light text color */
            border: 2px solid rgba(59, 130, 246, 0.5) !important; /* Border color */
            border-radius: 12px !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }

        /* Dropdown Specific Styles */
        .stSelectbox > div > div > div {
            background: rgba(15, 23, 42, 0.95) !important; /* Dark background for dropdown */
            color: #E2E8F0 !important; /* Light text color for dropdown */
            border: 2px solid rgba(59, 130, 246, 0.5) !important; /* Border color */
            border-radius: 12px !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }

        /* Dropdown Hover Effect */
        .stSelectbox > div > div > div:hover {
            border-color: #3B82F6 !important; /* Change border color on hover */
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important; /* Glow effect on hover */
        }

        /* Dropdown Focus Effect */
        .stSelectbox > div > div > div:focus {
            border-color: #3B82F6 !important; /* Focus border color */
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5) !important; /* Glow effect */
            outline: none !important;
        }

        /* Placeholder Text Styling */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(226, 232, 240, 0.5) !important; /* Placeholder color */
        }

        /* Message Styling */
        .stSuccess {
            background: rgba(15, 99, 77, 0.90);
            color: #A7F3D0;
            border: 1px solid rgba(167, 243, 208, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .stError {
            background: rgba(156, 12, 12, 0.90);
            color: #FECACA;
            border: 1px solid rgba(254, 202, 202, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.9);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.5);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(59, 130, 246, 0.7);
        }

        /* Responsive Design */
        @media screen and (max-width: 768px) {
            .block-container {
                padding: 1rem;
                margin: 0.5rem;
            }

            h1 { font-size: 1.75rem; }
            h2 { font-size: 1.5rem; }
            h3 { font-size: 1.25rem; }

            .stButton > button {
                width: 100%;
                padding: 0.5rem 1rem;
            }
        }

        /* Enhanced Glowing Submit Button Styling */
        .stFormSubmitButton > button {
            background: linear-gradient(45deg, #2563EB, #3B82F6) !important;
            color: white !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 600 !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3),
                       0 0 30px rgba(59, 130, 246, 0.2),
                       inset 0 0 10px rgba(255, 255, 255, 0.2) !important;
            animation: buttonPulse 2s infinite !important;
        }

        .stFormSubmitButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                120deg,
                transparent,
                rgba(255, 255, 255, 0.4),
                transparent
            );
            animation: shine 2s infinite;
        }

        .stFormSubmitButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.5),
                       0 0 50px rgba(59, 130, 246, 0.3),
                       inset 0 0 15px rgba(255, 255, 255, 0.3) !important;
            background: linear-gradient(45deg, #1D4ED8, #2563EB) !important;
        }

        .stFormSubmitButton > button:active {
            transform: translateY(-1px) !important;
        }

        @keyframes buttonPulse {
            0% {
                box-shadow: 0 0 15px rgba(59, 130, 246, 0.3),
                           0 0 30px rgba(59, 130, 246, 0.2);
            }
            50% {
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.5),
                           0 0 40px rgba(59, 130, 246, 0.3);
            }
            100% {
                box-shadow: 0 0 15px rgba(59, 130, 246, 0.3),
                           0 0 30px rgba(59, 130, 246, 0.2);
            }
        }

        @keyframes shine {
            0% {
                left: -100%;
            }
            20% {
                left: 100%;
            }
            100% {
                left: 100%;
            }
        }

        /* Neon Glowing Submit Button Styling */
        .stFormSubmitButton > button {
            background: rgba(15, 23, 42, 0.8) !important;
            color: #00ff88 !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            border: 2px solid #00ff88 !important;
            font-weight: 600 !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.3s ease !important;
            text-shadow: 0 0 10px #2985fd,
                        0 0 20px #0091ff,
                        0 0 40px #099dff !important;
            box-shadow: 0 0 20px rgba(0, 179, 255, 0.40),
                       inset 0 0 20px rgba(0, 34, 255, 0.20) !important;
            animation: neonPulse 1.5s infinite !important;
        }

        .stFormSubmitButton > button:hover {
            background: rgba(0, 255, 136, 0.1) !important;
            color: #00d0ff !important;
            border-color: #00ff88 !important;
            transform: translateY(-3px) !important;
            text-shadow: 0 0 20px #0073ff,
                        0 0 40px #00aaff,
                        0 0 80px #01aaff !important;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.6),
                       0 0 50px rgba(0, 255, 136, 0.4),
                       inset 0 0 30px rgba(0, 255, 136, 0.4) !important;
        }

        .stFormSubmitButton > button:active {
            transform: translateY(-1px) !important;
        }

        @keyframes neonPulse {
            0%, 100% {
                text-shadow: 0 0 10px #00eeff,
                            0 0 20px #00b7ff,
                            0 0 40px #00ff88;
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.4),
                           inset 0 0 20px rgba(0, 255, 136, 0.2);
            }
            50% {
                text-shadow: 0 0 15px #00ff88,
                            0 0 30px #02c4ff,
                            0 0 60px #00ff88;
                box-shadow: 0 0 30px rgba(0, 255, 136, 0.6),
                           inset 0 0 30px rgba(0, 255, 136, 0.3);
            }
        }

        /* Optional: Add glowing ripple effect on click */
        .stFormSubmitButton > button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(0, 255, 136, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .stFormSubmitButton > button:active::after {
            width: 200px;
            height: 200px;
            opacity: 0;
        }

        /* Themed Submit Button Styling */
        .stFormSubmitButton > button {
            background: rgba(37, 99, 235, 0.9) !important;
            color: #E2E8F0 !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            border: 2px solid rgba(59, 130, 246, 0.5) !important;
            font-weight: 600 !important;
            position: relative !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2) !important;
        }

        .stFormSubmitButton > button:hover {
            background: rgba(37, 99, 235, 1) !important;
            border-color: rgba(59, 130, 246, 0.8) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3) !important;
        }

        .stFormSubmitButton > button:active {
            transform: translateY(0) !important;
        }

        /* Remove previous button animations and effects */
        .stFormSubmitButton > button::before,
        .stFormSubmitButton > button::after {
            display: none !important;
        }

        /* ...rest of your existing styles... */

        /* Centered Headings with Enhanced Styling */
        h1, h2, h3 {
            text-align: center !important;
            color: #E2E8F0 !important;
            text-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            font-weight: 600;
            margin: 2rem auto !important;
            max-width: 800px;
        }

        h1 {
            font-size: 3rem;
            background: linear-gradient(to right, #60A5FA, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glowingText 2s ease-in-out infinite;
        }

        /* Amazing Button Styling */
        .stFormSubmitButton > button {
            background: rgba(15, 23, 42, 0.8) !important;
            color: #E2E8F0 !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            border: 2px solid #3B82F6 !important;
            font-weight: 600 !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.4s ease !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2),
                       inset 0 0 10px rgba(59, 130, 246, 0.1) !important;
            backdrop-filter: blur(5px) !important;
            letter-spacing: 0.5px !important;
            transform: scale(1) !important;
        }

        /* Button Hover Effects */
        .stFormSubmitButton > button:hover {
            background: rgba(59, 130, 246, 0.15) !important;
            border-color: #60A5FA !important;
            transform: scale(1.02) translateY(-2px) !important;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.4),
                       inset 0 0 20px rgba(59, 130, 246, 0.2) !important;
            letter-spacing: 1px !important;
        }

        /* Button Border Animation */
        .stFormSubmitButton > button::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(45deg, 
                #3B82F6, #60A5FA, #93C5FD, #60A5FA, #3B82F6) !important;
            background-size: 400% !important;
            opacity: 0 !important;
            transition: 0.5s !important;
            animation: borderGlow 8s linear infinite !important;
        }

        .stFormSubmitButton > button:hover::before {
            opacity: 0.4 !important;
        }

        /* Button Click Effect */
        .stFormSubmitButton > button:active {
            transform: scale(0.98) translateY(0) !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
        }

        /* Animations */
        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes glowingText {
            0%, 100% { text-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
            50% { text-shadow: 0 0 25px rgba(59, 130, 246, 0.8); }
        }

        /* Remove previous button effects */
        .stFormSubmitButton > button::after {
            display: none !important;
        }

        /* ...rest of your existing styles... */

        /* Enhanced Input Fields with Theme Colors */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stMultiselect > div > div > div {
            width: 100% !important;
            background: rgba(15, 23, 42, 0.95) !important;
            color: #E2E8F0 !important;
            border: 2px solid #3B82F6 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2),
                       inset 0 0 10px rgba(59, 130, 246, 0.1) !important;
            animation: inputBorderGlow 2s infinite !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 1rem !important;
        }

        /* Input Hover Effect */
        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover,
        .stSelectbox > div > div > div:hover,
        .stMultiselect > div > div > div:hover {
            border-color: #60A5FA !important;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4),
                       inset 0 0 15px rgba(59, 130, 246, 0.2) !important;
            transform: translateY(-2px) !important;
        }

        /* Input Focus Effect */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus,
        .stMultiselect > div > div > div:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.5),
                       inset 0 0 20px rgba(59, 130, 246, 0.3) !important;
            transform: translateY(-2px) !important;
            outline: none !important;
            background: rgba(15, 23, 42, 0.98) !important;
        }

        /* Remove white background from input wrapper */
        .stTextInput > div,
        .stTextArea > div {
            background: transparent !important;
        }

        .stTextInput > div > div,
        .stTextArea > div > div {
            background: transparent !important;
        }

        /* Pulsing border animation */
        @keyframes inputBorderGlow {
            0%, 100% {
                border-color: #3B82F6 !important;
                box-shadow: 0 0 15px rgba(59, 130, 246, 0.2),
                           inset 0 0 10px rgba(59, 130, 246, 0.1) !important;
            }
            50% {
                border-color: #60A5FA !important;
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.3),
                           inset 0 0 15px rgba(59, 130, 246, 0.2) !important;
            }
        }

        /* Enhanced Input Fields with Theme Colors */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stMultiselect > div > div > div {
            background: rgba(15, 23, 42, 0.95) !important;
            color: #E2E8F0 !important;
            border: 2px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.1) !important;
            backdrop-filter: blur(5px) !important;
        }

        /* Input Focus States with Theme Glow */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus,
        .stMultiselect > div > div > div:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.2),
                       inset 0 0 10px rgba(59, 130, 246, 0.1) !important;
            transform: translateY(-2px) !important;
            outline: none !important;
            background: rgba(15, 23, 42, 0.98) !important;
        }

        /* Input Hover Effect */
        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover,
        .stSelectbox > div > div > div:hover,
        .stMultiselect > div > div > div:hover {
            border-color: rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.15) !important;
        }

        /* Placeholder Text Styling */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(226, 232, 240, 0.5) !important;
        }

        /* Form Groups with Enhanced Spacing */
        .form-group {
            margin-bottom: 1.5rem !important;
            position: relative !important;
        }

        /* Label Styling */
        .stTextInput > label,
        .stTextArea > label,
        .stSelectbox > label {
            color: #E2E8F0 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.3) !important;
        }

        /* Error State */
        .stTextInput > div > div > input:invalid,
        .stTextArea > div > div > textarea:invalid {
            border-color: rgba(239, 68, 68, 0.5) !important;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.1) !important;
        }

        /* ... existing styles ... */

        /* Center and style the subtitle */
        .auth-header p {
            text-align: center !important;
            color: #E2E8F0 !important;
            font-size: 1.2rem !important;
            margin: 1rem auto !important;
            background: linear-gradient(45deg, #f6f6f6, #d0def5) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-shadow: 0 0 15px rgba(59, 130, 246, 0.5) !important;
            animation: subtitleGlow 2s ease-in-out infinite !important;
        }

        @keyframes subtitleGlow {
            0%, 100% { text-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
            50% { text-shadow: 0 0 25px rgba(59, 130, 246, 0.8); }
        }

        /* Enhanced Input Fields with Neon Blue Effect */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(15, 23, 42, 0.95) !important;
            color: #E2E8F0 !important;
            border: 2px solid #3B82F6 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.2),
                       inset 0 0 10px rgba(59, 130, 246, 0.1) !important;
            animation: inputPulse 2s infinite !important;
        }

        /* Input Hover Effect */
        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover {
            border-color: #60A5FA !important;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4),
                       inset 0 0 15px rgba(59, 130, 246, 0.2) !important;
            transform: translateY(-2px) !important;
        }

        /* Input Focus Effect */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.5),
                       inset 0 0 20px rgba(59, 130, 246, 0.3) !important;
            transform: translateY(-2px) !important;
            outline: none !important;
        }

        @keyframes inputPulse {
            0%, 100% {
                box-shadow: 0 0 10px rgba(59, 130, 246, 0.2),
                           inset 0 0 10px rgba(59, 130, 246, 0.1);
            }
            50% {
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.3),
                           inset 0 0 15px rgba(59, 130, 246, 0.2);
            }
        }

        /* ... existing styles ... */

        /* Animated Lock Icon */
        .lock-container {
            width: 60px;
            height: 60px;
                
            margin: 3rem auto 1rem;
            position: relative;
        }

        .lock-icon {
            width: 100%;
            height: 80%;
            position: relative;
            animation: lockFloat 3s ease-in-out infinite;
        }

        .lock-body {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 35px;
            height: 35px;
            background: #3B82F6;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
        }

        .lock-shackle {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 25px;
            height: 25px;
            border: 6px solid #3B82F6;
            border-bottom: none;
            border-radius: 25px 25px 0 0;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
        }

        .lock-keyhole {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 12px;
            height: 12px;
            background: rgba(15, 23, 42, 0.95);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }

        .lock-glow {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
            animation: glowPulse 2s ease-in-out infinite;
        }

        @keyframes lockFloat {
            0%, 100% {
                transform: translateY(0) rotate(0);
            }
            50% {
                transform: translateY(-10px) rotate(2deg);
            }
        }

        @keyframes glowPulse {
            0%, 100% {
                opacity: 0.5;
                transform: scale(1);
            }
            50% {
                opacity: 0.8;
                transform: scale(1.1);
            }
        }

        /* Update auth-header to accommodate lock icon */
        .auth-header {
            text-align: center;
            margin-bottom: 1rem;
            position: relative;
        }

        .auth-header h1 {
            margin-top: 10px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.95);
            border-right: 1px solid rgba(59, 130, 246, 0.2);
            padding: 1rem;
        }

        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        }

        .sidebar-logo {
            font-size: 1.5rem;
            font-weight: 600;
            color: #E2E8F0;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .sidebar-logo span {
            font-size: 2rem;
        }

        /* Navigation Button Styling */
        .stButton > button {
            background: rgba(15, 23, 42, 0.95) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            margin-bottom: 0.5rem !important;
            transition: all 0.3s ease !important;
            text-align: left !important;
            font-size: 1rem !important;
        }

        /* Active Navigation Button */
        .stButton > button[data-testid="stPrimary"] {
            background: rgba(59, 130, 246, 0.2) !important;
            border-color: #3B82F6 !important;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.2) !important;
            font-weight: 600 !important;
        }

        .stButton > button:hover {
            background: rgba(59, 130, 246, 0.1) !important;
            border-color: rgba(59, 130, 246, 0.4) !important;
            transform: translateX(5px) !important;
        }

        /* Section Header Styling */
        .section-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.95);
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .section-icon {
            font-size: 1.5rem;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #E2E8F0;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }

        /* ... rest of existing styles ... */

        /* Encrypted Data Form Styling */
        .encrypted-form {
            background: rgba(15, 23, 42, 0.95);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(59, 130, 246, 0.2);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
        }

        /* Enhanced Text Area Styling */
        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.98) !important;
            color: #E2E8F0 !important;
            border: 2px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            font-family: 'Poppins', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.1) !important;
            min-height: 150px !important;
        }

        .stTextArea textarea:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.2) !important;
            transform: translateY(-2px) !important;
        }

        /* Encrypted Output Container */
        .encrypted-output {
            background: rgba(15, 23, 42, 0.98);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(59, 130, 246, 0.3);
            margin-top: 2rem;
        }

        .encrypted-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .encrypted-badge {
            background: rgba(59, 130, 246, 0.2);
            color: #60A5FA;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .copy-button {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #60A5FA;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .copy-button:hover {
            background: rgba(59, 130, 246, 0.2);
            transform: translateY(-1px);
        }

        .ciphertext {
            font-family: 'Courier New', monospace;
            color: #E2E8F0;
            background: rgba(15, 23, 42, 0.95);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            margin-top: 1rem;
            white-space: pre-wrap;
            word-break: break-all;
        }

        /* Success Animation */
        @keyframes successPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }

        .success-feedback {
            animation: successPulse 0.5s ease-in-out;
        }

        /* Custom styles for input fields and dropdowns */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stMultiselect > div > div > div {
            border: 2px solid rgba(59, 130, 246, 0.5) !important; /* Match your theme color */
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus,
        .stMultiselect > div > div > div:focus {
            border-color: #3B82F6 !important; /* Focus color */
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5) !important; /* Glow effect */
        }
    """, unsafe_allow_html=True)

def create_section_header(title: str, icon: str):
    """Create a styled section header with icon"""
    return f"""
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <span class="section-title">{title}</span>
    </div>
    """

def create_button(label: str, tooltip: str, key: str = None):
    """Create a button with tooltip"""
    return st.markdown(f"""
        <button class="stButton" data-tooltip="{tooltip}">
            {label}
        </button>
    """, unsafe_allow_html=True)

def show_popup_message(message: str, type: str = "info"):
    """Show a modal-like popup message"""
    popup_html = f"""
    <div class="popup-overlay" id="popup">
        <div class="popup-content">
            <div class="status-message {type}">
                {message}
            </div>
            <button onclick="document.getElementById('popup').style.display='none'" 
                    class="stButton">Close</button>
        </div>
    </div>
    <script>
        document.getElementById('popup').style.display = 'block';
        setTimeout(() => {{
            document.getElementById('popup').style.display = 'none';
        }}, 3000);
    </script>
    """
    st.markdown(popup_html, unsafe_allow_html=True)

def show_progress():
    """Show a custom progress bar"""
    return st.markdown("""
        <div class="progress-bar">
            <div class="progress-bar-fill"></div>
        </div>
    """, unsafe_allow_html=True)

def show_loading(message: str = "Processing..."):
    """Display loading animation with progress bar"""
    with st.container():
        show_progress()
        col1, col2 = st.columns([1, 4])
        with col1:
            if lottie_loading:
                st_lottie(
                    lottie_loading,
                    height=80,
                    key="loading",
                    speed=1.5
                )
            else:
                st.spinner()
        with col2:
            st.markdown(
                f'<div class="status-message loading">{message}</div>',
                unsafe_allow_html=True
            )

def show_success(message: str):
    """Display success message with animation and fallback"""
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            if lottie_success:
                st_lottie(
                    lottie_success,
                    height=80,
                    key="success",
                    speed=1
                )
            else:
                st.success("✅")  # Fallback to emoji
        with col2:
            st.markdown(
                f'<div class="status-message success">✨ {message}</div>',
                unsafe_allow_html=True
            )

def show_error(message: str):
    """Display error message with animation and fallback"""
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            if lottie_error:
                st_lottie(
                    lottie_error,
                    height=80,
                    key="error",
                    speed=1
                )
            else:
                st.error("⚠️")  # Fallback to emoji
        with col2:
            st.markdown(
                f'<div class="status-message error">⚠️ {message}</div>',
                unsafe_allow_html=True
            )

def create_analytics_dashboard():
    """Create a styled analytics dashboard with dark theme and real-time updates."""
    analytics_placeholder = st.empty()  # Create a placeholder for the analytics content

    while True:
        # Fetch the latest analytics data
        user_data = get_user_encrypted_data(st.session_state.username)
        total_encryptions = len(user_data)
        recent_activity = user_data[-5:] if user_data else []
        
        # Calculate today's activity
        today_count = sum(1 for d in user_data if d['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d")))

        # Update the analytics display
        with analytics_placeholder.container():
            st.markdown(create_section_header("Analytics Dashboard", "📈"), unsafe_allow_html=True)

            # Define metrics and their values
            metrics = {
                "Total Encryptions": total_encryptions,
                "Storage Used": total_encryptions * 1.5,  # Assuming 1.5 KB per encryption
                "Today's Activity": today_count,
                "Security Score": 95  # Example static score
            }

            # Define colors for each metric
            colors = ['#60A5FA', '#34D399', '#F472B6', '#FBBF24']

            # Create Bar Chart for metrics
            bar_fig = go.Figure()

            for i, (metric, value) in enumerate(metrics.items()):
                bar_fig.add_trace(go.Bar(
                    x=[metric],
                    y=[value],
                    marker_color=colors[i % len(colors)],  # Cycle through colors
                    hovertemplate='%{y}<extra></extra>'
                ))

            bar_fig.update_layout(
                title="Analytics Metrics",
                xaxis_title="Metrics",
                yaxis_title="Values",
                yaxis=dict(tick0=0, dtick=5),  # Set y-axis ticks to have a difference of 5
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                font=dict(color='#E2E8F0'),
                barmode='group',  # Group bars together
            )
            st.plotly_chart(bar_fig, use_container_width=True, key=f"metrics_bar_chart_{int(time.time())}")  # Unique key for metrics bar chart

            # Create Pie Chart with unique colors for each field
            pie_fig = go.Figure(data=[
                go.Pie(
                    labels=list(metrics.keys()),  # Use metric names as labels
                    values=list(metrics.values()),  # Use metric values
                    hole=.3,
                    marker=dict(colors=colors),  # Assign unique colors for each field
                    hoverinfo='label+percent'
                )
            ])
            pie_fig.update_layout(
                title="Distribution of Metrics",
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                font=dict(color='#E2E8F0')
            )
            st.plotly_chart(pie_fig, use_container_width=True, key=f"pie_chart_{int(time.time())}")  # Unique key for pie chart

            # Activity Timeline
            st.markdown("### Recent Activity")
            if recent_activity:
                for activity in reversed(recent_activity):
                    st.markdown(f"""
                        <div class="activity-card">
                            <div class="activity-time">{activity['timestamp']}</div>
                            <div class="activity-label">Data Encrypted</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent activity")

        # Sleep for a while before refreshing the data
        time.sleep(5)  # Adjust the refresh rate as needed

def show_auth_page():
    """Display styled login/register form with custom theme"""
    # Initialize AuthUtils if not exists
    if 'auth_utils' not in st.session_state:
        class AuthUtils:
            def verify_login(self, username, password):
                success, message = authenticate_user(username, password)
                if success:
                    st.session_state.username = username  # Set the username in session state
                return success, message

            def register_user(self, username, password, confirm_password, email):
                if password != confirm_password:
                    return False, "Passwords do not match"
                return register_user(username, password, email)

        st.session_state.auth_utils = AuthUtils()
        
    # Create centered container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Card container for auth form
            st.markdown("""
                <div class="auth-card">
                    <div class="auth-header">
                        <div class="lock-container">
                            <div class="lock-icon">
                                <div class="lock-shackle"></div>
                                <div class="lock-body">
                                    <div class="lock-keyhole"></div>
                                </div>
                                <div class="lock-glow"></div>
                            </div>
                        </div>
                        <h1>Welcome to VaultX</h1>
                        <p>Secure Data Locker</p>
                    </div>
            """, unsafe_allow_html=True)
            
            # Initialize form mode
            if 'form_mode' not in st.session_state:
                st.session_state.form_mode = "login"
            
            # Form mode toggle buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Login", key="login_btn", use_container_width=True):
                    st.session_state.form_mode = "login"
            with col_b:
                if st.button("Register", key="register_btn", use_container_width=True):
                    st.session_state.form_mode = "register"
            
            st.markdown("---")
            
            # Login Form
            if st.session_state.form_mode == "login":
                with st.form("login_form"):
                    username = st.text_input("Username", key="login_username")
                    password = st.text_input("Password", type="password", key="login_password")
                    
                    if st.form_submit_button("Login", use_container_width=True):
                        if username and password:
                            success, message = st.session_state.auth_utils.verify_login(
                                username=username,
                                password=password
                            )
                            if success:
                                st.success(message)
                                st.session_state.authenticated = True
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.warning("Please fill in all fields")
            
            # Register Form
            else:
                with st.form("register_form"):
                    username = st.text_input("Username", key="reg_username")
                    email = st.text_input("Email", key="reg_email")
                    password = st.text_input("Password", type="password", key="reg_password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if username and email and password and confirm_password:
                            if password != confirm_password:
                                st.error("Passwords do not match")
                            else:
                                success, message = st.session_state.auth_utils.register_user(
                                    username=username,
                                    password=password,
                                    confirm_password=confirm_password,
                                    email=email
                                )
                                if success:
                                    st.success(message)
                                    st.session_state.form_mode = "login"
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(message)
                        else:
                            st.warning("Please fill in all fields")
            
            # Close card container
            st.markdown("</div>", unsafe_allow_html=True)

def show_encrypt_page():
    if 'username' not in st.session_state:
        st.error("User not logged in. Please log in first.")
        return  # Exit the function if the user is not logged in

    try:
        # Add sidebar navigation
        with st.sidebar:
            st.markdown("""
                <div class="sidebar-header">
                    <div class="sidebar-logo">
                        <span>🔒</span> VaultX
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Navigation items
            nav_items = {
                "Dashboard": "📊", 
                "Store Data": "📂",
                "Retrieve Data": "🔐",
                "Analytics": "📈",
                "Settings": "⚙️"
            }
            
            # Get current page from session state 
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "Dashboard"
            
            # Create navigation buttons
            for page, icon in nav_items.items():
                is_active = st.session_state.current_page == page
                if st.button(f"{icon} {page}", 
                           key=f"nav_{page}",  # Add unique keys
                           use_container_width=True,
                           type="primary" if is_active else "secondary"):
                    st.session_state.current_page = page
                    st.rerun()  # Force refresh when page changes

            # Add spacing before logout
            st.markdown("<br>" * 5, unsafe_allow_html=True)
            
            # Logout button at bottom of sidebar
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # Main content area
        with st.container():
            if st.session_state.current_page == "Dashboard":
                st.markdown(create_section_header("Dashboard", "📊"), unsafe_allow_html=True)
                
                # Get user statistics
                user_data = get_user_encrypted_data(st.session_state.username)
                total_encryptions = len(user_data)
                recent_activity = user_data[-5:] if user_data else []
                
                # Calculate today's activity
                today_count = sum(1 for d in user_data if d['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d")))
                storage_used = total_encryptions * 1.5  # Assuming 1.5 KB per encryption
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Encryptions", total_encryptions)
                with col2:
                    st.metric("Storage Used", f"{storage_used:.1f} KB")
                with col3:
                    st.metric("Today's Activity", today_count, f"+{today_count}")
                with col4:
                    st.metric("Security Score", "A+", "↗")
                
                # Add Session Duration Metric
                session_duration = time.time() - st.session_state.session_start_time
                st.metric("Session Duration", f"{int(session_duration // 60)} minutes {int(session_duration % 60)} seconds")

                # Create Bar Chart for specified metrics
                metrics = {
                    "Total Encryptions": total_encryptions,
                    "Storage Used": storage_used,
                    "Today's Activity": today_count
                }

                # Create Bar Chart
                bar_fig = go.Figure(data=[
                    go.Bar(
                        x=list(metrics.keys()),
                        y=list(metrics.values()),
                        marker_color=['#60A5FA', '#34D399', '#F472B6'],  # Different colors for each bar
                    )
                ])
                bar_fig.update_layout(
                    title="Dashboard Metrics",
                    xaxis_title="Metrics",
                    yaxis_title="Values",
                    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                    font=dict(color='#E2E8F0')
                )
                st.plotly_chart(bar_fig, use_container_width=True)

                # Activity Timeline
                st.markdown("### Recent Activity")
                if recent_activity:
                    for activity in reversed(recent_activity):
                        st.markdown(f"""
                            <div class="activity-card">
                                <div class="activity-time">{activity['timestamp']}</div>
                                <div class="activity-label">Data Encrypted</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No recent activity")
                
                # Add some CSS for the activity cards
                st.markdown("""
                    <style>
                    .activity-card {
                        background: rgba(15, 23, 42, 0.95);
                        border-radius: 8px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        border: 1px solid rgba(59, 130, 246, 0.2);
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    
                    .activity-time {
                        color: #94A3B8;
                        font-size: 0.875rem;
                    }
                    
                    .activity-label {
                        color: #60A5FA;
                        font-weight: 500;
                    }
                    </style>
                """, unsafe_allow_html=True)
            
            elif st.session_state.current_page == "Store Data":
                st.markdown(create_section_header("Store Data", "📂"), unsafe_allow_html=True)
                
                # Create the form
                with st.form("encrypt_form", clear_on_submit=True):
                    st.text_area("Enter sensitive data", 
                        placeholder="Type or paste your sensitive data here...",
                        height=150,
                        key="sensitive_data")
                    
                    passkey = st.text_input("Enter passkey", 
                        type="password",
                        placeholder="Enter your encryption passkey",
                        key="passkey")
                    
                    submitted = st.form_submit_button("🔒 Encrypt")

                if submitted:
                    # Check if both fields are filled
                    if st.session_state.sensitive_data and st.session_state.passkey:
                        try:
                            # Use Fernet encryption instead of base64
                            from cryptography.fernet import Fernet
                            from cryptography.hazmat.primitives import hashes
                            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                            import base64
                            
                            # Generate a key from the passkey
                            kdf = PBKDF2HMAC(
                                algorithm=hashes.SHA256(),
                                length=32,
                                salt=b'vaultx_salt',  # In production, use a random salt
                                iterations=100000,
                            )
                            key = base64.urlsafe_b64encode(kdf.derive(st.session_state.passkey.encode()))
                            f = Fernet(key)
                            
                            # Encrypt the data
                            encrypted_text = f.encrypt(st.session_state.sensitive_data.encode()).decode()
                            
                            # Save encrypted data
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if save_encrypted_data(st.session_state.username, encrypted_text, timestamp):
                                st.success("Data encrypted and saved successfully!")

                                # Copy to clipboard functionality
                                pyperclip.copy(encrypted_text)  # Copy the encrypted text to clipboard
                                st.success("Encrypted data copied to clipboard!")  # Notify the user

                                # Show encrypted output
                                st.markdown(f"""
                                    <div class="encrypted-output">
                                        <div class="encrypted-header">
                                            <span class="encrypted-badge">🔒 Encrypted</span>
                                        </div>
                                        <div class="ciphertext">{encrypted_text}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                        except Exception as e:
                            st.error(f"Encryption failed: {str(e)}")
                    else:
                        st.warning("Please enter both data and passkey")  # This message will show if either field is empty
            
            elif st.session_state.current_page == "Retrieve Data":
                st.markdown(create_section_header("Retrieve Data", "🔐"), unsafe_allow_html=True)
                
                # Create the form for manual decryption
                with st.form("decrypt_form", clear_on_submit=True):
                    st.text_area("Enter encrypted data", 
                        placeholder="Paste your encrypted data here...",
                        height=150,
                        key="encrypted_data")
                    
                    passkey = st.text_input("Enter passkey", 
                        type="password",
                        placeholder="Enter your decryption passkey",
                        key="decrypt_passkey")
                    
                    submitted = st.form_submit_button("🔓 Decrypt")

                if submitted and st.session_state.encrypted_data and st.session_state.decrypt_passkey:
                    try:
                        # Use Fernet decryption
                        from cryptography.fernet import Fernet
                        from cryptography.hazmat.primitives import hashes
                        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                        import base64
                        
                        # Generate a key from the passkey
                        kdf = PBKDF2HMAC(
                            algorithm=hashes.SHA256(),
                            length=32,
                            salt=b'vaultx_salt',  # In production, use a random salt
                            iterations=100000,
                        )
                        key = base64.urlsafe_b64encode(kdf.derive(st.session_state.decrypt_passkey.encode()))
                        f = Fernet(key)
                        
                        # Decrypt the data
                        decrypted_text = f.decrypt(st.session_state.encrypted_data.encode()).decode()
                        
                        # Show decrypted output
                        st.markdown(f"""
                            <div class="encrypted-output">
                                <div class="encrypted-header">
                                    <span class="encrypted-badge">🔓 Decrypted</span>
                                </div>
                                <div class="ciphertext">{decrypted_text}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Decryption failed: {str(e)}")
                else:
                    st.warning("Please enter both encrypted data and passkey")
            
            elif st.session_state.current_page == "Analytics":
                st.markdown(create_section_header("Analytics", "📈"), unsafe_allow_html=True)
                create_analytics_dashboard()
            
            elif st.session_state.current_page == "Settings":
                st.markdown(create_section_header("Settings", "⚙️"), unsafe_allow_html=True)
                
                # Settings form
                with st.form("settings_form"):
                    st.text_input("Change Username", key="new_username")
                    st.text_input("Change Email", key="new_email")
                    st.text_input("Change Password", type="password", key="new_password")
                    st.text_input("Confirm Password", type="password", key="confirm_new_password")
                    
                    submitted = st.form_submit_button("Save Changes")

                if submitted:
                    new_username = st.session_state.new_username
                    new_email = st.session_state.new_email
                    new_password = st.session_state.new_password
                    confirm_new_password = st.session_state.confirm_new_password
                    
                    if new_password != confirm_new_password:
                        st.error("Passwords do not match")
                    else:
                        # Update user data
                        user_data = load_user_data()
                        if st.session_state.username in user_data:
                            if new_username:
                                user_data[st.session_state.username]["username"] = new_username
                            if new_email:
                                user_data[st.session_state.username]["email"] = new_email
                            if new_password:
                                user_data[st.session_state.username]["password"] = hash_password(new_password)
                            
                            save_user_data(user_data)
                            st.success("Settings updated successfully")
                        else:
                            st.error("User not found")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def get_user_encrypted_data(username: str):
    """Retrieve encrypted data for the specified user."""
    user_data = load_user_data()  # Assuming this function loads user data from a JSON file
    if username in user_data:
        return user_data[username].get('encrypted_data', [])
    return []

def save_encrypted_data(username: str, encrypted_text: str, timestamp: str):
    """Save encrypted data for the user."""
    user_data = load_user_data()
    if username in user_data:
        if 'encrypted_data' not in user_data[username]:
            user_data[username]['encrypted_data'] = []
        user_data[username]['encrypted_data'].append({
            'text': encrypted_text,
            'timestamp': timestamp
        })
        save_user_data(user_data)  # Save the updated user data
        return True
    return False

def main():
    """Main function to run the Streamlit app"""
    setup_styling()
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = time.time()  # Record the session start time
    
    if st.session_state.authenticated:
        show_encrypt_page()
    else:
        show_auth_page()

if __name__ == "__main__":
    main()