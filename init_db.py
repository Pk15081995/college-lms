from app import app, db
from models import User, Student, Faculty, LeaveType, LeaveRequest
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta
import secrets

def seed():
    with app.app_context():
        db.create_all()
        if User.query.first():
            print("Database already has data — skipping seed.")
            return

        # Leave types
        types = [
            LeaveType(name='Medical Leave', max_days=15),
            LeaveType(name='Casual Leave', max_days=12),
            LeaveType(name='Personal Leave', max_days=10),
            LeaveType(name='Emergency Leave', max_days=5),
            LeaveType(name='Event/Sports Leave', max_days=8),
        ]
        db.session.add_all(types)
        db.session.commit()

        # HOD
        hod = User(name='Dr. Deepak Chauhan', email='hod@college.edu',
                   password=generate_password_hash('hod123'), role='hod')
        db.session.add(hod); db.session.commit()

        # Faculty
        fu1 = User(name='Prof. Anita Sharma', email='anita@college.edu',
                   password=generate_password_hash('faculty123'), role='faculty')
        fu2 = User(name='Prof. Rajesh Kumar', email='rajesh@college.edu',
                   password=generate_password_hash('faculty123'), role='faculty')
        db.session.add_all([fu1, fu2]); db.session.commit()
        fac1 = Faculty(user_id=fu1.id, department='MCA', designation='Associate Professor')
        fac2 = Faculty(user_id=fu2.id, department='MCA', designation='Assistant Professor')
        db.session.add_all([fac1, fac2]); db.session.commit()

        # Students
        students_data = [
            ('Shivani Chaudhary', 'shivani@college.edu', 'VGU24ONS3MCA0081', 'MCA', 'Sem 3', fac1.id),
            ('Arjun Mehta',       'arjun@college.edu',   'VGU24ONS3MCA0082', 'MCA', 'Sem 3', fac1.id),
            ('Priya Singh',       'priya@college.edu',   'VGU24ONS3MCA0083', 'MCA', 'Sem 3', fac2.id),
            ('Rohan Verma',       'rohan@college.edu',   'VGU24ONS3MCA0084', 'MCA', 'Sem 3', fac2.id),
        ]
        student_objs = []
        for name, email, roll, course, sem, fid in students_data:
            su = User(name=name, email=email,
                      password=generate_password_hash('student123'), role='student')
            db.session.add(su); db.session.flush()
            s = Student(user_id=su.id, roll_no=roll, course=course, semester=sem,
                        faculty_id=fid, total_classes=100, attended=85)
            db.session.add(s)
            student_objs.append(s)
        db.session.commit()

        # Sample leave requests
        today = date.today()
        samples = [
            (student_objs[0].id, 1, today + timedelta(days=3), today + timedelta(days=4), 'Medical checkup', 'approved'),
            (student_objs[1].id, 2, today + timedelta(days=5), today + timedelta(days=5), 'Family function', 'pending_faculty'),
            (student_objs[2].id, 4, today + timedelta(days=2), today + timedelta(days=2), 'Emergency at home', 'faculty_approved'),
        ]
        for sid, lt, frm, to, reason, status in samples:
            lr = LeaveRequest(student_id=sid, leave_type_id=lt, from_date=frm, to_date=to,
                              days=(to-frm).days+1, reason=reason, status=status,
                              qr_token=secrets.token_hex(16))
            if status in ('faculty_approved', 'approved'):
                lr.faculty_comment = 'Approved by faculty.'
                lr.faculty_action_at = datetime.utcnow()
            if status == 'approved':
                lr.hod_comment = 'Final approval granted.'
                lr.hod_action_at = datetime.utcnow()
            db.session.add(lr)
        db.session.commit()

        print("✅ Database seeded successfully!")
        print("\n── LOGIN CREDENTIALS ──")
        print("HOD/Admin : hod@college.edu / hod123")
        print("Faculty   : anita@college.edu / faculty123")
        print("Student   : shivani@college.edu / student123")

if __name__ == '__main__':
    seed()
