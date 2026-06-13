from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ── USERS (base auth table for all roles) ──
class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(20), nullable=False)   # student / faculty / hod
    created_at = db.Column(db.DateTime, default=datetime.now)

    student    = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    faculty    = db.relationship('Faculty', backref='user', uselist=False, cascade='all, delete-orphan')


# ── STUDENTS ──
class Student(db.Model):
    __tablename__ = 'students'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roll_no      = db.Column(db.String(40), unique=True, nullable=False)
    course       = db.Column(db.String(80))      # e.g. MCA, BCA
    semester     = db.Column(db.String(20))
    faculty_id   = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)  # class advisor
    total_classes= db.Column(db.Integer, default=100)
    attended     = db.Column(db.Integer, default=85)

    leaves       = db.relationship('LeaveRequest', backref='student', cascade='all, delete-orphan')


# ── FACULTY ──
class Faculty(db.Model):
    __tablename__ = 'faculty'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department  = db.Column(db.String(80))
    designation = db.Column(db.String(80), default='Assistant Professor')

    advisees    = db.relationship('Student', backref='advisor', foreign_keys='Student.faculty_id')


# ── LEAVE TYPES ──
class LeaveType(db.Model):
    __tablename__ = 'leave_types'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80), nullable=False)
    max_days   = db.Column(db.Integer, default=15)


# ── LEAVE REQUESTS (two-stage approval: faculty -> hod) ──
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id            = db.Column(db.Integer, primary_key=True)
    student_id    = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    from_date     = db.Column(db.Date, nullable=False)
    to_date       = db.Column(db.Date, nullable=False)
    days          = db.Column(db.Integer, nullable=False)
    reason        = db.Column(db.Text, nullable=False)

    # Workflow status:
    # pending_faculty -> faculty_approved -> approved (by HOD)
    #                 -> rejected (by faculty or HOD)
    #                 -> cancelled (by student)
    status        = db.Column(db.String(30), default='pending_faculty')

    faculty_comment = db.Column(db.Text, default='')
    hod_comment     = db.Column(db.Text, default='')
    faculty_action_at = db.Column(db.DateTime, nullable=True)
    hod_action_at     = db.Column(db.DateTime, nullable=True)

    applied_on    = db.Column(db.DateTime, default=datetime.now)
    qr_token      = db.Column(db.String(64), unique=True)

    leave_type    = db.relationship('LeaveType')


# ── NOTIFICATIONS ──
class Notification(db.Model):
    __tablename__ = 'notifications'
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title     = db.Column(db.String(160), nullable=False)
    message   = db.Column(db.Text, nullable=False)
    is_read   = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.now)
