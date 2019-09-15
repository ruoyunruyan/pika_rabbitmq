# Time: 2019/9/9  13:18
# Author jzh
# File product.py

import pika


connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=connection_host,
    credentials=connection_credentials
))


channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange', exchange_type='topic')

while 1:
    routing_key = input('请输入路由模式:')
    if routing_key == 'exit':
        break
    message = input('请输入消息:')
    if message == 'exit':
        break
    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message)


connection.close()
