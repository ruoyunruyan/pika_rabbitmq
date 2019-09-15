# Time: 2019/9/9  10:41
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
    time.sleep(len(body))
    print('消息处理完成!')
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 设置公平调度
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
