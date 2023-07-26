from flask import Flask, render_template,request
from fileinput import filename
import sqlite3
import pandas as pd
from pathlib import Path
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('./')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('first.html')


@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/frame')
def frame():
    return render_template('main.html')


@app.route('/option')
def option():
    return render_template('option.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/adlogin')
def adlogin():
    return render_template('adlogin.html')


@app.route('/details')
def details():
    return render_template('details.html')


@app.route('/place')
def place():
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            cur.execute('select * from cart')
            items=cur.fetchall()   
            cur1=con.cursor()
            cur1.execute('select nitems*price from cart')
            s=cur1.fetchall()
            sum=0
            for i in s:
                 sum+=i[0]
            print(sum)
            cur3=con.cursor()
            cur3.execute('select * from details')
            det=cur3.fetchall()
            con.commit()
    return render_template('place.html',items=items,sum=sum,det=det)

@app.route('/payment')
def payment():
    with sqlite3.connect("restaurant.db") as con:     
            cur1=con.cursor()
            cur1.execute('select nitems*price from cart')
            s=cur1.fetchall()
            sum=0
            for i in s:
                 sum+=i[0]
            cur2= con.cursor()  
            cur2.execute('select * from details')  
            c=cur2.fetchall()
            x=c[0][0]+c[0][1][len(c[0][1])-4:]  
            cur3=con.cursor()
            cur3.execute('select * from details')
            det=cur3.fetchall()
            cur= con.cursor()
            cur.execute('delete from cart') 
            con.commit()
    return render_template('payment.html',sum=sum,x=x,det=det)

@app.route('/bf')
def bf():
    df = pd.read_csv('bf.csv')
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            df.to_sql('bfitems', con, if_exists='replace', index = False)
            cur.execute('select * from bfitems')
            rows=cur.fetchall()   
            con.commit() 
    return render_template('bf.html',rows=rows)


@app.route('/lunch')
def lunch():
    df = pd.read_csv('lunch.csv')
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            df.to_sql('lunch', con, if_exists='replace', index = False)
            cur.execute('select * from lunch')
            rows=cur.fetchall()   
            con.commit() 
    return render_template('lunch.html',rows=rows)


@app.route('/evening')
def evening():
    df = pd.read_csv('evening.csv')
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            df.to_sql('evening', con, if_exists='replace', index = False)
            cur.execute('select * from evening')
            rows=cur.fetchall()   
            con.commit() 
    return render_template('evening.html',rows=rows)


@app.route('/dinner')
def dinner():
    df = pd.read_csv('dinner.csv')
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            df.to_sql('dinner', con, if_exists='replace', index = False)
            cur.execute('select * from dinner')
            rows=cur.fetchall()   
            con.commit() 
    return render_template('dinner.html',rows=rows)


@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        u=request.form.get('uname')
        print(u)
        p=request.form.get('psw')
        print(p)
        with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()
            cur.execute("select * from admin where username='{a}'".format(a=u))
            c=cur.fetchall()
            print(c)
            if c[0][1]==p:
                return render_template('admin.html')
            done="provide correct login credentials"
    return render_template('adlogin.html',done=done)


@app.route('/main',methods=['POST','GET'])
def main():
    if request.method=='POST':
        n=request.form.get('name')
        print(n)
        p=request.form.get('ph')
        print(p)
        val=(n,p)
        with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            cur1= con.cursor()
            cur1.execute('delete from details')
            cur.execute('insert into details(name,phonenumber) values(?,?)',val)
            c=con.cursor()
            c.execute("select * from details")
            c1=c.fetchall()
            print(c1)
            if c1:
                 print('hi')
                 con.commit()
                 return render_template('main.html')
            print("hello")
            con.commit()
    return render_template('details.html')


@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method=='POST':
        l=[request.files.get('file0').filename,request.files.get('file1').filename,request.files.get('file2').filename,request.files.get('file3').filename]
        d={'0':'bf.csv','1':'lunch.csv','2':'evening.csv','3':'dinner.csv'}
        for i in l:
            if i!='':
                a=l.index(i)
        x=d[f'{a}']
        f=request.files.get(f'file{a}')
        data_filename = secure_filename(f.filename)
        if d[f'{a}']==f.filename:
             fp=os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
             f.save(fp)
             done=f"{ f.filename} sucessfully uploaded"
        else:
             done=f"upload {x} to insert data"
    return render_template('admin.html',done=done)


@app.route('/addcart',methods=['POST','GET'])
def addcart():
    if request.method=='POST':
        v=request.form.get('bfitem')
        v1=list(map(str,v[1:-3].split(',')))
        print(v1)
        with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            cur1=con.cursor()
            cur1.execute("select count(*) from cart where itemname='{a}'".format(a=v1[0]))
            c=cur1.fetchall()
            c1=c[0][0]
            if c1:
                cur.execute("update cart set nitems={a} where itemname='{b}'".format(a=c1+1,b=v1[0]))
            else:
                val=(v1[0],float(v1[1]),1)
                cur.execute('insert into cart(itemname,price,nitems) values(?,?,?)',val)
            con.commit()
    return render_template('menu.html')


@app.route('/cart')
def cart():
    with sqlite3.connect("restaurant.db") as con:  
            cur = con.cursor()  
            cur.execute('select * from cart')
            items=cur.fetchall()   
            cur1=con.cursor()
            cur1.execute('select nitems*price from cart')
            s=cur1.fetchall()
            sum=0
            for i in s:
                 sum+=i[0]
            con.commit()
    return render_template('cart.html',items=items,sum=sum)


if __name__ == '__main__':
   app.run(debug = True)