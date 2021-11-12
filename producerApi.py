#!/usr/bin/python
import sqlite3
from flask import Flask,request,jsonify
from celery import Celery
import pandas as pd

api = Flask(__name__)

app = Celery('task')
default_config = 'celeryconfig'
app.config_from_object(default_config)

DATABASE="test.db"

@api.route('/create', methods=['POST'])
def create_main():
   if request.method=="POST":
       print(DATABASE)
       with sqlite3.connect(DATABASE) as conn:
           conn.execute('''CREATE TABLE Items
                  (id INTEGER PRIMARY KEY,
                  item           varchar(20)    NOT NULL,
                  status         varchar(20)    DEFAULT 'pending');''')
           return "Table created",202

@api.route('/getData', methods=['GET'])
def display_main():
   if request.method=="GET":
       with sqlite3.connect(DATABASE) as conn:
           df = pd.read_sql_query("SELECT id, item,status from Items", conn)
           df_list = df.values.tolist()
           JSONP_data = jsonify(df_list)
           return JSONP_data,200

         
@api.route('/', methods=['POST'])
def update_main():
   if request.method=="POST":
      payload=request.get_json()

      with sqlite3.connect(DATABASE) as conn:
         print("Opened database successfully")
         conn.execute("INSERT INTO Items (item) VALUES (?)",[payload['item']])
         print("Records created successfully")
         df = pd.read_sql_query("SELECT id, item,status from Items", conn)
         print(df)
         r=app.send_task('consumer.updateDB',kwargs=payload)
      
      return "Inserted the data and added in rabbitmq queue",204


# main driver function
if __name__ == '__main__':
    api.run()


