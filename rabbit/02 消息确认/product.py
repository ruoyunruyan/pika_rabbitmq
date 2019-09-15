# Time: 2019/9/9  9:46
# Author jzh
# File product1.py


import pika

# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 通过channel声明my_queue队列, 如果队列不存在则创建队列, 如果存在则忽略
channel.queue_declare(queue='my_queue')

task_list = ['message', 'email']
# 4. 发送消息
for index in range(2):
    channel.basic_publish(exchange='', routing_key='my_queue', body=task_list[index])

# 5. 关闭链接对象
connection.close()

print('消息发送完毕!')