"""
Configuration Settings for Accident Detection System
Centralized configuration management
"""

import os
from pathlib import Path


class Config:
    """Base configuration"""
    
    # ==========================================
    # APPLICATION SETTINGS
    # ==========================================
    APP_NAME = "AI Accident Detection System"
    VERSION = "1.0.0"
    DEBUG = True
    
    # ==========================================
    # SERVER SETTINGS
    # ==========================================
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True  # Auto-reload on code changes (disable in production)
    
    # ==========================================
    # PATHS
    # ==========================================
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    MODEL_DIR = BASE_DIR / "models"
    DB_PATH = BASE_DIR / "accident_detection.db"
    
    # Create directories if they don't exist
    UPLOAD_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)
    
    # ==========================================
    # MODEL SETTINGS
    # ==========================================
    MODEL_INPUT_SIZE = (224, 224)  # Width, Height
    CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for accident detection
    FRAME_SKIP = 5  # Process every Nth frame
    
    # Severity thresholds
    HIGH_SEVERITY_THRESHOLD = 0.85
    MEDIUM_SEVERITY_THRESHOLD = 0.65
    
    # ==========================================
    # DATABASE SETTINGS
    # ==========================================
    DB_FILE = "accident_detection.db"
    
    # ==========================================
    # ALERT SETTINGS
    # ==========================================
    
    # Email Configuration
    EMAIL_ENABLED = False  # Set to True when configured
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # SMS Configuration (Twilio)
    SMS_ENABLED = False  # Set to True when configured
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
    
    # Emergency Contacts
    EMERGENCY_CONTACTS = {
        "ambulance": os.getenv("AMBULANCE_NUMBER", "+911234567890"),
        "police": os.getenv("POLICE_NUMBER", "+911234567891"),
        "family": os.getenv("FAMILY_NUMBER", "+911234567892"),
        "email": os.getenv("EMERGENCY_EMAIL", "emergency@example.com")
    }
    
    # ==========================================
    # LOCATION SETTINGS
    # ==========================================
    LOCATION_API = "https://ipapi.co/json/"
    LOCATION_TIMEOUT = 5  # seconds
    
    # Fallback location (if API fails)
    FALLBACK_LOCATION = {
        "city": "New Delhi",
        "region": "Delhi",
        "country": "India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    # ==========================================
    # CORS SETTINGS
    # ==========================================
    CORS_ORIGINS = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "*"  # Allow all (restrict in production)
    ]
    
    # ==========================================
    # FILE UPLOAD SETTINGS
    # ==========================================
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]
    
    # ==========================================
    # LOGGING SETTINGS
    # ==========================================
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE = BASE_DIR / "accident_detection.log"
    
    # ==========================================
    # API RATE LIMITING
    # ==========================================
    RATE_LIMIT_ENABLED = False
    RATE_LIMIT_REQUESTS = 100  # requests per minute
    
    # ==========================================
    # SECURITY SETTINGS
    # ==========================================
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # ==========================================
    # EXTERNAL APIs
    # ==========================================
    
    # OpenStreetMap for reverse geocoding
    OSM_API = "https://nominatim.openstreetmap.org/reverse"
    OSM_USER_AGENT = f"{APP_NAME}/{VERSION}"
    
    # Hospital finder
    OVERPASS_API = "http://overpass-api.de/api/interpreter"
    HOSPITAL_SEARCH_RADIUS_KM = 5


class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    RELOAD = True


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    RELOAD = False
    
    # Restrict CORS
    CORS_ORIGINS = [
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]
    
    # Enable rate limiting
    RATE_LIMIT_ENABLED = True


class TestingConfig(Config):
    """Testing-specific configuration"""
    TESTING = True
    DB_FILE = "test_accident_detection.db"


# ==========================================
# CONFIGURATION SELECTOR
# ==========================================

def get_config():
    """
    Get configuration based on environment
    
    Usage:
        config = get_config()
        print(config.APP_NAME)
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Default configuration instance
config = get_config()


# ==========================================
# USAGE EXAMPLES
# ==========================================

if __name__ == "__main__":
    print("Configuration Settings")
    print("=" * 50)
    print(f"App Name: {config.APP_NAME}")
    print(f"Version: {config.VERSION}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Server: {config.HOST}:{config.PORT}")
    print(f"Upload Directory: {config.UPLOAD_DIR}")
    print(f"Database: {config.DB_PATH}")
    print(f"Email Enabled: {config.EMAIL_ENABLED}")
    print(f"SMS Enabled: {config.SMS_ENABLED}")
    print("=" * 50)