# College Online Leave Management System

Flask + PostgreSQL leave management system with Student, Faculty, and HOD/Admin roles.

## Features
- Three-tier login: Student, Faculty, HOD/Admin
- Two-stage approval workflow: Student applies → Faculty approves → HOD final approval
- Apply / view / cancel leave (past-date applications are blocked)
- Email + in-app notifications on approval/rejection
- Reports: monthly, student-wise, by leave type, with PDF & Excel export
- PDF leave application download
- QR code verification for approved leaves
- Admin analytics dashboard
- Mobile responsive design
- Database tables: users, students, faculty, leave_requests, leave_types, notifications

## Tech Stack
- Backend: Python + Flask
- Database: PostgreSQL
- PDF: reportlab | Excel: openpyxl | QR: qrcode

## Demo Logins
| Role | Email | Password |
|------|-------|----------|
| HOD/Admin | hod@college.edu | hod123 |
| Faculty | anita@college.edu | faculty123 |
| Student | shivani@college.edu | student123 |

## Run Locally

1. Install PostgreSQL and create a database named `collegelms`.
2. Edit `config.py` if your PostgreSQL user/password differ from `postgres` / `password`.
3. Install dependencies and run:

```
pip install -r requirements.txt
python init_db.py        # creates tables + sample data
python app.py            # starts the server
```

4. Open http://localhost:5000

## Deploy on Render.com
This repo includes `render.yaml` which automatically provisions a free PostgreSQL
database and connects it via the `DATABASE_URL` environment variable. Just create a
new Blueprint on Render pointing to this repository.
