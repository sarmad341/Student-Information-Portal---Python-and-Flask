"""
Student Information Portal - Flask Application
Vercel-Ready Version
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'student_portal_secret_key_2024'

# Get absolute path for students.json (required for Vercel)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, "students.json")


# ============================================================================
# PART A - Object-Oriented Design
# ============================================================================

class Student:
    def __init__(self, name, roll_no, department, email):
        self.name = name
        self.roll_no = roll_no
        self.department = department
        self.email = email

    def display_info(self):
        return f"""
        Name: {self.name}
        Roll Number: {self.roll_no}
        Department: {self.department}
        Email: {self.email}
        """

    def update_email(self, new_email):
        self.email = new_email
        return f"Email updated successfully to: {self.email}"

    def to_dict(self):
        return {
            'name': self.name,
            'roll_no': self.roll_no,
            'department': self.department,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            roll_no=data['roll_no'],
            department=data['department'],
            email=data['email']
        )


# ============================================================================
# PART A - Data Handling and File Management
# ============================================================================

def load_students():
    try:
        if not os.path.exists(STUDENTS_FILE):
            return []

        with open(STUDENTS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except Exception:
        return []


def save_students(students_list):
    try:
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(students_list, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print("Error saving:", e)
        return False


def add_student(name, roll_no, department, email):
    try:
        students = load_students()

        # Duplicate roll number check
        for student in students:
            if student['roll_no'] == roll_no:
                return False, f"Student with roll number {roll_no} already exists!"

        new_student = {
            'name': name,
            'roll_no': roll_no,
            'department': department,
            'email': email
        }

        students.append(new_student)

        if save_students(students):
            return True, "Student added successfully!"
        return False, "Error writing data."

    except Exception as e:
        return False, str(e)


def get_all_students():
    return load_students()


def search_student_by_roll(roll_no):
    try:
        students = load_students()
        for student in students:
            if student['roll_no'] == roll_no:
                return student
        return None
    except:
        return None


# ============================================================================
# PART B - Flask Routes
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_student_page():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll_no = request.form.get('roll_no', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()

        if not all([name, roll_no, department, email]):
            flash("All fields are required!", "error")
            return render_template('add.html')

        success, message = add_student(name, roll_no, department, email)

        flash(message, 'success' if success else 'error')

        if success:
            return redirect(url_for('students_page'))
        return render_template('add.html')

    return render_template('add.html')


@app.route('/students')
def students_page():
    students = get_all_students()
    return render_template('students.html', students=students)


@app.route('/search', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()

        if not roll_no:
            flash("Please enter a roll number!", "error")
            return render_template('search.html', student=None)

        student = search_student_by_roll(roll_no)

        if student:
            flash("Student found!", "success")
        else:
            flash("Student not found!", "error")

        return render_template('search.html', student=student)

    return render_template('search.html', student=None)


# NO app.run() here – Vercel handles this automatically
# END OF FILE
