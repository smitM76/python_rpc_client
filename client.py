import pika
import uuid
import json
import logging
from logging.config import dictConfig
import argparse

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#channel = connection.channel()
# channel.queue_declare(queue='rpc_queue')


class Rpc_client(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(data))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


parser = argparse.ArgumentParser()
parser.add_argument('method', help='Select The Method',
                    choices=["GET", "POST", "PUT", "DELETE"])
# parser.add_argument('id', help='id', type=int)
# parser.add_argument('username', help='username', type=str)
# parser.add_argument('comment', help='comment', type=str)

args, sub_args = parser.parse_known_args()
if args.method == 'GET':
    msg = {
        "method": "GET"
    }

elif args.method == 'POST':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='username', type=str)
    parser.add_argument('comment', help='comment', type=str)

    args = parser.parse_args(sub_args)
    u_name = args.username
    u_comment = args.comment
    msg = {
        "method": "POST",
        "username": u_name,
        "comment": u_comment
    }

elif args.method == 'PUT':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id', type=int)
    parser.add_argument('--username', help='username', type=str)
    parser.add_argument('--comment', help='comment', type=str)

    args = parser.parse_args(sub_args)
    u_id = args.id
    u_name = args.username
    u_comment = args.comment
    msg = {
        "method": "PUT",
        "id": u_id,
        "username": u_name,
        "comment": u_comment
    }

elif args.method == "DELETE":
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id', type=int)
    args = parser.parse_args(sub_args)
    u_id = args.id
    msg = {
        "method": "DELETE",
        "id": u_id
    }
else:
    print("Invalid option")

rpc = Rpc_client()
print(" [x] Requesting ")
response = rpc.call(json.dumps(msg))
print(" [.] Got %r" % response)
