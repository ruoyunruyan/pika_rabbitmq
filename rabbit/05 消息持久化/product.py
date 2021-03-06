# Time: 2019/9/9  10:41
# Author jzh
# File product.py

import pika

# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 通过channel声明my_queue队列, 如果队列不存在则创建队列, 如果存在则忽略
# durable 设置消息队列的持久化
channel.queue_declare(queue='my_queue', durable=True)

task_list = ['aaaa', 'b', 'cccc', 'd']
# 4. 发送消息   默认的消息发送机制是循环发送消息
# properties 设置消息持久化
for index in range(4):
    channel.basic_publish(exchange='',
                          routing_key='my_queue',
                          body=task_list[index],
                          properties=pika.BasicProperties(delivery_mode=2))

# 5. 关闭链接对象
connection.close()

print('消息发送完毕!')
