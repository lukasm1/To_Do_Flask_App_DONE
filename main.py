from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)


##To Do TABLE Configuration
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)


##To Do Form Configuration
class ToDoForm(FlaskForm):
    name = StringField('Name of the Task', validators=[DataRequired()], render_kw={"placeholder": "Type here e.g. buy bananas"})
    add = SubmitField('Add')


@app.route("/")
def home():
    return redirect(url_for('index'))


@app.route("/index.html")
def index():
    todos = db.session.query(ToDo).all()
    form = ToDoForm()

    return render_template("index.html", form=form, todos=todos)


@app.route('/add', methods=["POST"])
def add():
    new_todo = ToDo(
        name=request.form.get("name"),
        completed=False,
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(ToDo).get(todo_id)
    if ToDo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(ToDo).get(todo_id)
    if ToDo:
        print("yyyy")
        todo.completed=not todo.completed
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)