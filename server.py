import pika
import queries as Q
import json
import logging
from logging.config import dictConfig

file = open('logging_config.ini', "r")
config = json.load(file)
dictConfig(config)


logger = logging.getLogger(__name__)
# logger.setLevel('ERROR')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):

    data = json.loads(str(body)[2:-1])
    print('Recieved -> {}'.format(data))

    logger.info('Recieved -> {}'.format(data))

    if data['method'] == 'GET':
        response = Q.display_data()
    elif data['method'] == 'POST':
        response = Q.insert_data(data['username'], data['comment'])

    elif data['method'] == 'PUT':
        response = Q.update_data(data['id'], data['username'], data['comment'])

    elif data['method'] == 'DELETE':
        response = Q.delete_data(data['id'])

    else:
        response = "wrong api"

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue='rpc_queue')
print(" [x] Awaiting RPC requests")
channel.start_consuming()
