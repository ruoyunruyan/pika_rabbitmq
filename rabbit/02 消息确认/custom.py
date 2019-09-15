# Time: 2019/9/9  9:40
# Author jzh
# File custom.py

import time

import pika

connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=connection_host,
    credentials=connection_credentials
))

channel = connection.channel()

channel.queue_declare(queue='my_queue')


def callback(ch, method, properties, body):

    print('消费者接收到消息: %s\n开始处理...' % body.decode())
    time.sleep(5)
    print('消息处理完成!')
    # 消息处理完成后, 确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

channel.start_consuming()