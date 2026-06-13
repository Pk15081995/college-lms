import os

class Config:
    # ── DATABASE ──
    # Reads DATABASE_URL from environment (Render provides this automatically).
    # Falls back to your LOCAL PostgreSQL if not set.
    #
    # LOCAL format: postgresql://<user>:<password>@localhost:5432/<dbname>
    # Change 'postgres', 'password', and 'collegelms' below to match your local setup.
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/collegelms'
    )

    # Render gives URLs starting with postgres:// but SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}

    SECRET_KEY = os.environ.get('SECRET_KEY', 'college-lms-secret-key-change-in-production')

    # ── EMAIL (optional) ──
    # To enable real emails, set these as environment variables.
    # If not set, notifications are saved in-app + printed to console (still works for demo).
    MAIL_SERVER   = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT     = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_ENABLED  = bool(os.environ.get('MAIL_USERNAME'))
