#!/usr/bin/python
import sqlite3
from flask import Flask,request,jsonify
from celery import Celery
import pandas as pd
import configparser

parser = configparser.RawConfigParser()   
configFilePath = 'appconfig.conf'
parser.read(configFilePath)

broker_url=parser.get('general','broker_url')
result_backend=parser.get('general','result_backend')
task_default_queue=parser.get('general','task_default_queue')
exchange=parser.get('general','exchange')
routing_key=parser.get('general','routing_key')
result_serializer='json'
accept_content=['application/json']
# Database
DATABASE= parser.get('general', 'DATABASE_FILE')

api = Flask(__name__)
app = Celery('task')
app.conf.update(
    result_backend = result_backend,
    broker_url = broker_url,
    accept_content = accept_content,
    result_serializer = result_serializer,
    task_default_queue = task_default_queue,
    imports=("consumer"),
    task_routes = {
        'updateDB': {
            'exchange': exchange,
            'routing_key': routing_key
        }
    }
)

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
         conn.execute("INSERT INTO Items (item) VALUES (?)",[payload['item']])
         r=app.send_task('consumer.updateDB',kwargs=payload)
      
      return '',202


# main driver function
if __name__ == '__main__':
    api.run()


