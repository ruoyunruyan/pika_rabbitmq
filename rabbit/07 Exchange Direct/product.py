# Time: 2019/9/9  11:42
# Author jzh
# File product.py

import pika

# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 获取用户输入信息
while True:
    message = input('请输入消息:')
    if message == 'exit':
        break
    routing_key_name = input('请输入发送信息的路由:')
    channel.basic_publish(exchange='direct_log', routing_key=routing_key_name, body=message)

# 4. 关闭链接对象
connection.close()

print('消息发送完毕!')