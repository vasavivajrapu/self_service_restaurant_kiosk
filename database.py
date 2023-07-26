import sqlite3  
  
con = sqlite3.connect("restaurant.db")  
print("Database opened successfully")  
con.execute("create table IF NOT EXISTS bfitems(itemname TEXT PRIMARY KEY , price FLOAT NOT NULL)")  
con.execute("create table IF NOT EXISTS lunch(itemname TEXT PRIMARY KEY , price FLOAT NOT NULL)") 
con.execute("create table IF NOT EXISTS eveningitems(itemname TEXT PRIMARY KEY , price FLOAT NOT NULL)") 
con.execute("create table IF NOT EXISTS dinneritems(itemname TEXT PRIMARY KEY , price FLOAT NOT NULL)") 
con.execute("create table IF NOT EXISTS cart(itemname TEXT PRIMARY KEY , price FLOAT NOT NULL , nitems INT NOT NULL )")
con.execute("create table IF NOT EXISTS admin(username TEXT PRIMARY KEY ,password TEXT NOT NULL)")
con.execute("create table IF NOT EXISTS details(name TEXT PRIMARY KEY ,phonenumber TEXT NOT NULL)")
print("Tables created successfully")  
con.close() 