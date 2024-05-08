from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://student:examen@db:5432/points')
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
    student = Student(name=name)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/assign/<int:student_id>', methods=['POST'])
def assign_grade(student_id):
    grade = int(request.form.get('grade'))
    student = db.session.get(Student, student_id)
    student.grade = grade
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Within the application context
    with app.app_context():
        # Create tables
        db.create_all()

    # Run the application
    app.run(debug=True, host='127.0.0.0', port=5000)






# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField, SubmitField
# from wtforms.validators import DataRequired, NumberRange
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://student:examen@db:5432/points')
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     grade = db.Column(db.Integer, default=0)

# class StudentForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     grade = IntegerField('Grade', validators=[NumberRange(min=0, max=100), DataRequired()])
#     submit = SubmitField('Submit')

# @app.route('/')
# def index():
#     students = Student.query.all()
#     return render_template('index.html', students=students)

# @app.route('/create', methods=['GET', 'POST'])
# def create_student():
#     form = StudentForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         student = Student(name=name)
#         db.session.add(student)
#         db.session.commit()
#         flash('Student added successfully!', 'success')
#         return redirect(url_for('index'))
#     return render_template('create_student.html', form=form)

# @app.route('/assign/<int:student_id>', methods=['GET', 'POST'])
# def assign_grade(student_id):
#     form = StudentForm()
#     student = Student.query.get_or_404(student_id)
#     if form.validate_on_submit():
#         student.grade = form.grade.data
#         db.session.commit()
#         flash('Grade assigned successfully!', 'success')
#         return redirect(url_for('index'))
#     form.grade.data = student.grade  # Set the form grade value to current grade
#     return render_template('assign_grade.html', form=form, student=student)

# if __name__ == '__main__':
#     with app.app_context():
#         # Create tables if they don't exist
#         db.create_all()
        
#     # Run the application
#     app.run(debug=True, host='0.0.0.0', port=5000)