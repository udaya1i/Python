from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
    
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable =False)
    desc = db.Column(db.String(500), nullable = False)
    date_created =  db.Column(db.DateTime, default = datetime.utcnow)
       
    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            new_todo = Todo(title=title, desc = desc)
            db.session.add(new_todo)
            db.session.commit()
            flash('Task added successfully','success')
        else:
            flash('Please fill the form','error')
    lists = Todo.query.all()
    return render_template('index.html', lists = lists)


@app.route('/delete/<int:sno>')
def delete(sno):
    all_todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(all_todo)
    db.session.commit()
    return redirect('/')

# @app.route('update/<int:sno>')
# def udpate(sno):
#     all_todo = Todo.query.filter_by(sno= sno).first()
#     all_todo['title'] = request.form['title']
#     all_todo['desc'] = request.form['desc']
#     if all_todo['title'] and all_todo['desc']:
#         update_todo = Todo[all_todo['title']=all_todo['title'], all_todo['desc']=all_todo['desc']]
        



if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    app.debug = True
    app.run()
    


        
        
    
