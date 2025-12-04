"""
Student Information Portal - Flask Application
This application demonstrates:
- Object-Oriented Programming (Student class)
- Data handling and file management (JSON operations)
- Exception handling
- Flask routing and template rendering
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'student_portal_secret_key_2024'  # Required for flash messages

# Path to the JSON file storing student data
STUDENTS_FILE = 'students.json'


# ============================================================================
# PART A - Object-Oriented Design
# ============================================================================

class Student:
    """
    Student class to represent a student with attributes and methods.
    Demonstrates Object-Oriented Programming principles.
    """
    
    def __init__(self, name, roll_no, department, email):
        """
        Initialize a Student object with required attributes.
        
        Args:
            name (str): Student's full name
            roll_no (str): Student's roll number (unique identifier)
            department (str): Student's department
            email (str): Student's email address
        """
        self.name = name
        self.roll_no = roll_no
        self.department = department
        self.email = email
    
    def display_info(self):
        """
        Display student information in a formatted string.
        
        Returns:
            str: Formatted string containing all student information
        """
        return f"""
        Name: {self.name}
        Roll Number: {self.roll_no}
        Department: {self.department}
        Email: {self.email}
        """
    
    def update_email(self, new_email):
        """
        Update the student's email address.
        
        Args:
            new_email (str): New email address to set
        """
        self.email = new_email
        return f"Email updated successfully to: {self.email}"
    
    def to_dict(self):
        """
        Convert Student object to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the student
        """
        return {
            'name': self.name,
            'roll_no': self.roll_no,
            'department': self.department,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Student object from a dictionary.
        
        Args:
            data (dict): Dictionary containing student information
            
        Returns:
            Student: Student object created from dictionary
        """
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
    """
    Load all students from the JSON file.
    Implements exception handling for missing files or incorrect data format.
    
    Returns:
        list: List of student dictionaries, empty list if file doesn't exist or is invalid
    """
    try:
        # Check if file exists
        if not os.path.exists(STUDENTS_FILE):
            return []
        
        # Read and parse JSON file
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Validate data format
        if not isinstance(data, list):
            raise ValueError("Invalid data format: expected a list")
        
        return data
    
    except FileNotFoundError:
        # File doesn't exist, return empty list
        return []
    
    except json.JSONDecodeError as e:
        # Invalid JSON format
        print(f"Error: Invalid JSON format in {STUDENTS_FILE}: {e}")
        return []
    
    except ValueError as e:
        # Invalid data structure
        print(f"Error: {e}")
        return []
    
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error loading students: {e}")
        return []


def save_students(students_list):
    """
    Save list of students to JSON file.
    Implements exception handling for file write operations.
    
    Args:
        students_list (list): List of student dictionaries to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(students_list, file, indent=4, ensure_ascii=False)
        return True
    
    except IOError as e:
        print(f"Error writing to file {STUDENTS_FILE}: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error saving students: {e}")
        return False


def add_student(name, roll_no, department, email):
    """
    Add a new student record to the JSON file.
    
    Args:
        name (str): Student's name
        roll_no (str): Student's roll number
        department (str): Student's department
        email (str): Student's email
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Load existing students
        students = load_students()
        
        # Check if roll number already exists
        for student in students:
            if student['roll_no'] == roll_no:
                return False, f"Student with roll number {roll_no} already exists!"
        
        # Create new student dictionary
        new_student = {
            'name': name,
            'roll_no': roll_no,
            'department': department,
            'email': email
        }
        
        # Add to list
        students.append(new_student)
        
        # Save to file
        if save_students(students):
            return True, "Student added successfully!"
        else:
            return False, "Error saving student data."
    
    except Exception as e:
        return False, f"Error adding student: {str(e)}"


def get_all_students():
    """
    Display all student records.
    
    Returns:
        list: List of all student dictionaries
    """
    return load_students()


def search_student_by_roll(roll_no):
    """
    Search for a student by roll number.
    
    Args:
        roll_no (str): Roll number to search for
        
    Returns:
        dict or None: Student dictionary if found, None otherwise
    """
    try:
        students = load_students()
        
        for student in students:
            if student['roll_no'] == roll_no:
                return student
        
        return None
    
    except Exception as e:
        print(f"Error searching for student: {e}")
        return None


# ============================================================================
# PART B - Flask Web Application Routes
# ============================================================================

@app.route('/')
def index():
    """
    Home page route.
    Displays welcome message and navigation links.
    """
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_student_page():
    """
    Add Student page route.
    GET: Display the form
    POST: Process form submission and add student
    """
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        roll_no = request.form.get('roll_no', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate input
        if not all([name, roll_no, department, email]):
            flash('All fields are required!', 'error')
            return render_template('add.html')
        
        # Add student using our data handling function
        success, message = add_student(name, roll_no, department, email)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('students_page'))
        else:
            flash(message, 'error')
            return render_template('add.html')
    
    # GET request - show form
    return render_template('add.html')


@app.route('/students')
def students_page():
    """
    View Students page route.
    Displays all student records in a table using Jinja2 template.
    """
    students = get_all_students()
    return render_template('students.html', students=students)


@app.route('/search', methods=['GET', 'POST'])
def search_student():
    """
    Search Student page route (Bonus feature).
    GET: Display search form
    POST: Process search and display results
    """
    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        
        if not roll_no:
            flash('Please enter a roll number to search!', 'error')
            return render_template('search.html', student=None)
        
        # Search for student
        student = search_student_by_roll(roll_no)
        
        if student:
            flash(f'Student found!', 'success')
            return render_template('search.html', student=student)
        else:
            flash('Student not found!', 'error')
            return render_template('search.html', student=None)
    
    # GET request - show search form
    return render_template('search.html', student=None)


# ============================================================================
# Demonstration of OOP - Creating and using Student objects
# ============================================================================

def demonstrate_oop():
    """
    Demonstrate Object-Oriented Programming by creating Student objects
    and calling their methods. This function can be called to test the OOP features.
    """
    print("\n=== Demonstrating Object-Oriented Programming ===\n")
    
    # Create multiple Student objects
    student1 = Student("John Doe", "CS001", "Computer Science", "john.doe@university.edu")
    student2 = Student("Jane Smith", "EE002", "Electrical Engineering", "jane.smith@university.edu")
    student3 = Student("Bob Johnson", "ME003", "Mechanical Engineering", "bob.johnson@university.edu")
    
    # Display information using the display_info() method
    print("Student 1 Information:")
    print(student1.display_info())
    
    print("\nStudent 2 Information:")
    print(student2.display_info())
    
    # Update email using the update_email() method
    print("\nUpdating Student 1's email:")
    result = student1.update_email("john.doe.new@university.edu")
    print(result)
    print("\nUpdated Student 1 Information:")
    print(student1.display_info())
    
    print("\n=== OOP Demonstration Complete ===\n")


# Run the Flask application
if __name__ == '__main__':
    # Initialize students.json if it doesn't exist
    if not os.path.exists(STUDENTS_FILE):
        save_students([])
        print(f"Initialized {STUDENTS_FILE} with empty list.")
    
    # Uncomment the line below to run OOP demonstration
    # demonstrate_oop()
    
    # Run Flask app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)

