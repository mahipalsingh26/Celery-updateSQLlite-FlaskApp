#!/usr/bin/python
import sqlite3
from flask import Flask,request
from celery import Celery
from consumer import updateDB
import pandas as pd
app = Flask(__name__)


# # conn.execute('''CREATE TABLE Items
# #          (id INTEGER PRIMARY KEY,
# #          item           varchar(20)    NOT NULL,
# #          status         varchar(20)    DEFAULT 'pending');''')
# print("Table created successfully",conn)

@app.route('/', methods=['POST'])
def update_main():
   if request.method=="POST":
      updatedata=request.get_json()
      #print(updatedata)
      
      with sqlite3.connect("test.db") as conn:
         print("Opened database successfully")
         conn.execute("INSERT INTO Items (item) VALUES (?)",[updatedata['item']])
         print("Records created successfully")
         df = pd.read_sql_query("SELECT id, item,status from Items", conn)
         print(df)
         primes = updateDB.delay(request.get_json())
      print("prime:",primes)
      return {"Task_id":str(primes)},202


#conn.commit()

# main driver function
if __name__ == '__main__':
    app.run()


