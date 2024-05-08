# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://student:examen@db:5432/points')
# db = SQLAlchemy(app)

# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     grade = db.Column(db.Integer, default=0)

# @app.route('/')
# def index():
#     students = Student.query.all()
#     return render_template('index.html', students=students)

# @app.route('/create', methods=['POST'])
# def create_student():
#     name = request.form.get('name')
#     student = Student(name=name)
#     db.session.add(student)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/assign/<int:student_id>', methods=['POST'])
# def assign_grade(student_id):
#     grade = int(request.form.get('grade'))
#     student = db.session.get(Student, student_id)
#     student.grade = grade
#     db.session.commit()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     # Within the application context
#     with app.app_context():
#         # Create tables
#         db.create_all()

#     # Run the application
#     app.run(debug=True, host='127.0.0.0', port=5000)



###

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
os.environ.get('VAR_NAME', 'default val')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://student:examen@db:5432/points')
app.config['SECRET_KEY'] = os.urandom(24)  # For flashing messages, it's good to set a secret key
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/create', methods=['POST'])
def create_student():
    name = request.form.get('name')
    if not name:
        flash('Name cannot be empty.', 'error')
        return redirect(url_for('index'))
    
    student = Student(name=name)
    db.session.add(student)
    db.session.commit()
    flash('Student created successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/assign/<int:student_id>', methods=['POST'])
def assign_grade(student_id):
    try:
        grade = int(request.form.get('grade'))
        if grade < 0 or grade > 100:
            flash('Grade must be between 0 and 100.', 'error')
            return redirect(url_for('index'))
    except ValueError:
        flash('Invalid grade input.', 'error')
        return redirect(url_for('index'))

    student = db.session.get(Student, student_id)
    if student is None:
        flash('Student not found.', 'error')
        return redirect(url_for('index'))

    student.grade = grade
    db.session.commit()
    flash('Grade assigned successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='127.0.0.1', port=5000)


