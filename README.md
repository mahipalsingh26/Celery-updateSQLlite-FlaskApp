# Celery-updateSQLlite-FlaskApp
This repository demonstrating task that how we can use celery and flask application to update sqlite database.

## Getting Started

Below steps will get you a copy of this reposistory up and running on your local machine testing purposes.

### Clone the Repository
```
git clone 
```

### Installation
1. Install RabbitMQ server and start the server:
```
rabbitmq-server
```
2. Create python virtual environment and install the packages.
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Configure
Open `appconfig.conf` file and Make the necessary changes.
```
[general]

result_backend = rpc://
broker_url = pyamqp://guest:guest@localhost:5672


task_default_queue = updateDBqueue
exchange=''
routing_key=updateDBqueue

DATABASE_FILE=StoreItems.db

# log file
receiver_LOG_FILE=cmdmq_receiver.log
sender_LOG_FILE=cmdmq_sender.log
```
In broker_url guest and guest is default username and password.

### Run Program
1. Open terminal:
```
celery -A consumer worker --pool=solo -l info
```
2. In Another terminal:
```
python producerApi.py
```
After Running the api,
1. Open `RedditMQ-Flask.postman_collection.json` file in postmen and make Create Table Request from Postmen.
2. Make a `create-table` request. (Response Code: 200)
3. Make a `get-Data` request (First time response will be empty)
4. Make a `SEND-DATA-TO-QUEUE` request (Response Should be empty, Code: 202).
   - It will insert the data in table. Then send data to RabbitMQ-server for process.
   - Just after `SEND-DATA-TO-QUEUE` request, Make get-data request to view data is inserted and status="pending".
   - After 15 sec status="completed"
