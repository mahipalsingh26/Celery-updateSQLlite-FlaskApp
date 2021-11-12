from celery import Celery
import sqlite3
import time

app = Celery('task')
default_config = 'celeryconfig'
app.config_from_object(default_config)


@app.task(serializer='json')
def updateDB(item):
    with sqlite3.connect("test.db") as conn:
        time.sleep(15)  ##Testing Perpose, It will update the status after 15 sec
        conn.execute('''UPDATE Items SET status = 'completed' WHERE item = ?''', [item])
        # app.log(f"{x['item']} status is updated as completed!")
    return item