# Time: 2019/9/9  13:23
# Author jzh
# File custom.py

import sys
import pika

connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=connection_host,
    credentials=connection_credentials
))

channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)

queue_name = result.method.queue

for routing_key in sys.argv[1:]:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=routing_key)


def callback(ch, method, properties, body):
    print('消费者接收到消息: %s' % body.decode())


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
