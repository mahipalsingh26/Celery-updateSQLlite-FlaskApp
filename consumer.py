from celery import Celery
import sqlite3
import time
app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@localhost')
app.conf.task_default_queue = 'updateDBqueue'

@app.task
def updateDB(x):
    with sqlite3.connect("test.db") as conn:
        print("Opened database successfully",x)
        time.sleep(20)
        print("Opened database successfully")
        conn.execute('''UPDATE Items SET status = 'completed' WHERE item = ?''', [x['item']])
        print("Records updated successfully")
        cursor = conn.execute("SELECT id, item,status from Items")
        for row in cursor:
            print ("Id: ", row[0],"Item: ", row[1],"Status: ", row[2])
    return x