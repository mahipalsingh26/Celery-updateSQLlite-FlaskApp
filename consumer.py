from celery import Celery
import configparser
import sqlite3
import time

app = Celery('task')
default_config = 'celeryconfig'
app.config_from_object(default_config)

parser = configparser.RawConfigParser()   
configFilePath = 'appconfig.conf'
parser.read(configFilePath)

# Database
DATABASE= parser.get('general', 'DATABASE_FILE')

@app.task(serializer='json')
def updateDB(item):
    with sqlite3.connect(DATABASE) as conn:
        time.sleep(15)  ##Testing Perpose, It will update the status after 15 sec
        #Update the latest row with item =item
        conn.execute('''UPDATE Items SET status = 'completed' WHERE item = ? and id= (SELECT MAX(id) FROM Items WHERE item = ?)''', [item,item])
    return item