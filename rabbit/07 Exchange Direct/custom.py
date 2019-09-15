# Time: 2019/9/9  11:42
# Author jzh
# File custom.py

import sys
import pika

# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 创建exchange交换器
channel.exchange_declare(exchange='direct_log', exchange_type='direct')

# 4. 创建临时队列
result = channel.queue_declare(queue='', exclusive=True)

# 5. 获取临时队列的名字
queue_name = result.method.queue

# 6. 队列queue与交换器exchange绑定
for routing_key_name in sys.argv[1:]:
    channel.queue_bind(exchange='direct_log', queue=queue_name, routing_key=routing_key_name)


def callback(ch, method, properties, body):
    print('消费者接收到消息: %s' % body.decode())


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()