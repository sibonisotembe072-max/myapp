from flask import Flask , redirect, render_template, request,flash,session
import sqlite3
import datetime
app = Flask(__name__)
db_name="save.db"
app.security_key="mysecurity123"

def init_db():
    Registered_on=datetime.date.today()
    conn= sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute(""" 
                   CREATE TABLE IF NOT EXISTS stu(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_name TEXT NOT NULL,
                       student_surname TEXT NOT NULL,
                       student_email TEXT NOT NULL,
                       student_contacts INTEGER NOT NULL,
                       student_address TEXT NOT NULL,
                       student_number UNIQUE,
                       Registered_on TEXT NOT NULL,
                       total_paid REAL
                       
                    
                       
                       
                   )
                   
                   
                   
                   
                   """);
    conn.commit()
    conn.close()





    
@app.route('/')
def this_is_home_page():
    return render_template('form.html')

@app.route('/kill')
def fresh():
    return render_template('form.html')

@app.route('/close')
def nav():
    return render_template('form.html')

@app.route("/profile/<int:student_id>",methods=['GET','POST'])
def profilee(student_id):
    conn=sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT* FROM stu WHERE id=?", (student_id,))
    student=cursor.fetchone()
    return render_template("profile.html" ,student=student)


@app.route('/enrol', methods=['POST'])
def take_input():
    name=request.form["student_name"]
    surname=request.form["student_surname"]
    email=request.form["student_email"]
    contacts=request.form["student_contacts"]
    address=request.form["student_address"]
    number=request.form["student_number"]
    datee= datetime.date.today()
    registration =request.form["registration"]
    conn= sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute("INSERT INTO stu(student_name,student_surname,student_email,student_contacts,student_address,student_number,Registered_on,total_paid) VALUES(?,?,?,?,?,?,?,?)",(name ,surname,email,contacts,address,number,datee,registration))
    conn.commit()
    conn.close()
    return render_template("response.html")

@app.route('/portal')
def students():
   conn=sqlite3.connect(db_name)
   cursor= conn.cursor()
   cursor.execute("SELECT * FROM stu")
   data =cursor.fetchall() 
   conn.close()
   total=len(data)
   return render_template('student.html',lengthh=total,  students=data)

@app.route('/query', methods=['POST'])
def search():
   name=request.form["student_query"]
   conn=sqlite3.connect(db_name)
   cursor= conn.cursor()
   cursor.execute("SELECT * FROM stu WHERE  student_number=?",(name,))
   data =cursor.fetchone() 
   
   conn.close()
   return render_template('searched.html', results=data)


@app.route('/proceed/<int:id>',methods=['POST'])
def up(id):
   name=request.form['name']
   surname=request.form['surname']
   email=request.form['email']
   cell=request.form['cell']
   student_number=request.form['number']
   total=request.form['total']
   conn=sqlite3.connect(db_name)
   cursor= conn.cursor()
   cursor.execute("UPDATE stu SET student_name=?,student_surname=?,student_email=?,student_contacts=?,student_number=?,total_paid=? WHERE id=?",(name,surname,email,cell,student_number,total,id,))
   conn.commit() 
   conn.close()
   return "student updated"

@app.route('/admit')
def back_to_home():
    return render_template("form.html")

@app.route("/amount",methods=["POST"])
def newamount():
    idee = request.form['student_id']
    student_name = request.form['student_name']
    student_surname = request.form['student_surname']
    student_number = request.form['student_number']
    amount = request.form['amount']
    table=student_name
    
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS  {table}(
        student_id INTEGER,
        student_name TEXT,
        student_surname TEXT,
        student_number INTEGER,
        amount INTEGER
        
        
    )""")
    cursor.execute(f"INSERT INTO {table} (student_id,student_name,student_surname,student_number,amount) VALUES(?,?,?,?,?)",(idee,student_name,student_surname,student_number,amount))
    conn.commit()
    conn.close()
    return "amount added"

@app.route("/viewer/<student>")
def show(student):
    try:
     conn=sqlite3.connect(db_name)
     cursor=conn.cursor()
     cursor.execute(f"SELECT * FROM {student}")
     all_tables=cursor.fetchall()
     conn.close()
     return render_template("viewer.html",all_tables=all_tables)
    except sqlite3.OperationalError:
        return f"{student} have no payment record yet"
        
    

if __name__=='__main__':
    init_db()
    app.run(debug=True)
