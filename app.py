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

app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db' 
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db2 = SQLAlchemy(app2)

    
class User(db2.Model):
    username = db2.Column(db2.String(200), nullable=False, primary_key=True)
    email = db2.Column(db2.String(200), nullable=False)
    password = db2.Column(db2.String(200), nullable = False)
    data_created = db2.Column(db2.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'{self.username} - {self.email}'
    
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['username']
        password = request.form['password']
        if username and email and password:
            register_user = User(username = username, password = password, email = email)
            db.session.add(register_user)
            db.session.commit()
            flash('User Registered Successfully')
        else:
            flash('Something went wrong')  
          
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
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
    return render_template('home.html', lists = lists)

@app.route('/delete/<int:sno>')
def delete(sno):
    all_todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(all_todo)
    db.session.commit()
    return redirect('/home')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
       title = request.form['title']
       desc = request.form['desc']
       todo = Todo.query.filter_by(sno = sno).first()
       todo.title = title
       todo.desc = desc
       db.session.add(todo)
       db.session.commit()
       return redirect('/home')
    todo = Todo.query.filter_by(sno=sno).first()       
    return render_template('update.html', todo = todo )
if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    app.debug = True
    app.run()
    