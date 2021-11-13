from celery import Celery
import configparser
import sqlite3
import time
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

@app.task()
def updateDB(item):
    try:
        with sqlite3.connect(DATABASE) as conn:
            time.sleep(15)  ##Added for Testing purpose, It will update the status after 15 sec
            #Update the latest row with item =item
            conn.execute('''UPDATE Items SET status = 'completed' WHERE item = ? and id= (SELECT MAX(id) FROM Items WHERE item = ?)''', [item,item])
    except:
        #we can log error
        pass