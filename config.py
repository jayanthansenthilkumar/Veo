"""
Configuration settings for Gen AI Platform
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "genai_platform.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    OUTPUT_FOLDER = BASE_DIR / 'outputs'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav', 'mp3'}
    
    # Google AI API settings
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Generation settings
    IMAGE_MODEL = 'imagen-4.0-generate-001'
    VIDEO_MODEL = 'veo-3.1-generate-preview'
    MUSIC_MODEL = 'models/lyria-realtime-exp'
    
    # Generation limits
    MAX_IMAGES_PER_REQUEST = 4
    MAX_VIDEO_DURATION = 30  # seconds
    MAX_MUSIC_DURATION = 120  # seconds
    VIDEO_GENERATION_TIMEOUT = 600  # 10 minutes
    
    # Default generation parameters
    DEFAULT_IMAGE_COUNT = 1
    DEFAULT_VIDEO_RESOLUTION = '720p'
    DEFAULT_MUSIC_BPM = 120
    DEFAULT_MUSIC_TEMPERATURE = 1.0
    DEFAULT_MUSIC_DURATION = 30
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting (requests per minute)
    RATE_LIMIT_IMAGE = 10
    RATE_LIMIT_VIDEO = 5
    RATE_LIMIT_MUSIC = 5
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        # Create directories if they don't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER / 'images', exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER / 'videos', exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER / 'music', exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
