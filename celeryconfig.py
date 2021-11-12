result_backend = 'rpc://'
broker_url = 'pyamqp://guest:guest@localhost:5672'

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
task_default_queue = 't1test1'

imports=("consumer")
task_protocol = 1
task_routes = {
    'task': {
        'exchange': 't1test1',
        'routing_key': 't1test1'
    }
}
