from flask import Flask , url_for , redirect , render_template , request
import sqlite3
from datetime import datetime 
app = Flask(__name__)

# SQL Commands :
def get_db() :
    return sqlite3.connect("Project2.db" , timeout = 10)

def create_table() :
    conn = get_db() 
    cursor = conn.cursor() 
    cursor.execute(""" CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT , title TEXT NOT NULL , text TEXT NOT NULL , time TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def Add(title , data) :
    conn = get_db() 
    cursor = conn.cursor() 
    t = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute("INSERT INTO notes (title , text , time ) values (? , ? , ?) " , (title ,data , t))
    conn.commit()
    conn.close()

def Edit(id , title ,data) :
    conn = get_db() 
    cursor = conn.cursor()
    t = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute(
        "UPDATE notes SET title = ?, text = ? , time = ? WHERE id = ?",
        (title, data , t ,id)
    )
    conn.commit()
    conn.close()

def delete(id) :
    conn = get_db()
    cursor = conn.cursor() 
    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

def show(id) :
    conn = get_db() 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ? " , (id,))
    notes = cursor.fetchone()
    conn.close()
    return notes

def All() :
    conn = get_db() 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes 

def reset_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='notes'")
    conn.commit()
    conn.close()

def Delete() :
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DROP Table notes")
    conn.commit()
    conn.close()
#--------------------------X---------------------------------#

# For checking the error :

def id_exist(id) :
    notes = All()
    check = False
    for i in notes :
        if i[0] == id :
            check = True 
            break 
    return check

# Routings : 

@app.route("/")
def home() :
    return render_template("home.html")

@app.route("/add_notes" , methods = ["POST"])
def adding() :
    title = request.form.get("title")
    text = request.form.get("text")
    Add(title , text)
    return redirect(url_for('home'))

@app.route("/add" , methods = ["POST" , "GET"]) 
def addf() :
    return render_template("add_notes.html")

@app.route("/edit/<int:id>")
def edit(id) :
    if (id_exist(id)) == False :
        return render_template("error.html")
    
    notes = show(id)
    return render_template("edit_notes.html" , notes = notes)

@app.route("/Edit/<int:id>" , methods=["POST"])
def editf(id) :
    new_title = request.form.get("new_title")
    new_text = request.form.get("new_text")

    Edit(id , new_title , new_text)
    return redirect(url_for('home'))

@app.route("/view/<int:id>")
def view(id) :
    if (id_exist(id)) == False :
        return render_template("error.html")

    notes = show(id) 
    return render_template("view_all_notes.html" , notes = notes , all = False)

@app.route("/delete/<int:id>")
def deletef(id) :
    if (id_exist(id)) == False :
        return render_template("error.html")
    
    delete(id)
    return redirect(url_for('home'))

@app.route("/view_all")
def view_all() :
    notes = All()
    return render_template("view_all_notes.html" , notes = notes , all = True)


if(__name__ == "__main__") :
    create_table()
    # reset_table() # for reset when needed , Danger ☠️
    # Delete() # Danger ☠️
    app.run(debug = True , use_reloader = False)



