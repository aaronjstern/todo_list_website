from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)


@app.route('/')
def home():
    todo_list = db.session.query(ToDoList).filter_by(done=False)
    todo_list_done = db.session.query(ToDoList).filter_by(done=True)
    return render_template("index.html", todo_list=todo_list, todo_list_done=todo_list_done)


@app.route('/add', methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        new_todo = ToDoList(
            task=request.form["next_todo"],
            done=False
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/done', methods=["GET", "POST"])
def mark_done():
    if request.method == "POST":
        todo_id = request.args.get("todo_id")
        todo = db.session.query(ToDoList).get(todo_id)
        todo.done = True
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete', methods=["GET", "POST"])
def delete_todo():
    if request.method == "POST":
        todo_id = request.args.get("todo_id")
        todo = db.session.query(ToDoList).get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
