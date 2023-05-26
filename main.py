from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import or_, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

username = "postgres"
password = "priyajoice"
dbname = "postgres"

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    actual_marks = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)


# app.app_context().push()
# db.create_all()


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    form = SearchForm()
    student_list = Student.query

    tag = form.search.data

    if tag is not None:

        if tag.isnumeric():
            student_list = db.session.query(Student).filter(or_(Student.actual_marks == tag, Student.total_marks == tag))
        else:
            student_list = db.session.query(Student).filter(
                or_(func.lower(Student.name) == tag.lower(), func.lower(Student.email) == tag.lower(),
                    func.lower(Student.gender) == tag.lower()))

        return render_template("home.html", form=form,
                               student_list=student_list.paginate(page=page, per_page=per_page, error_out=False))

    return render_template("home.html", form=form,
                           student_list=student_list.paginate(page=page, per_page=per_page, error_out=False))


if __name__ == "__main__":
    app.run(debug=True)
