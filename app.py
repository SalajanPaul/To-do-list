from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todo_list = todo.query.all()
    print(todo_list) #debugging
    return render_template('base.html', todo_list = todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo_item = todo.query.filter_by(id=todo_id).first()
    todo_item.complete = not todo_item.complete
    db.session.commit()
    return redirect(url_for("index"))
    
    
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_update = todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_update)
    db.session.commit()
    return redirect(url_for("index"))


    
with app.app_context():
    # Ensure the instance folder exists
    import os
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.create_all()
    

if __name__ == "__main__": 
    app.run(debug=True)