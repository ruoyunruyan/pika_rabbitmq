# Time: 2019/9/9  11:03
# Author jzh
# File custom_log.py

import sys
import pika

# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 通过channel创建exchange, 类型为fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 4. 创建匿名队列 exclusive=True表示没有与队列的连接时, 队列删除
result = channel.queue_declare(queue='', exclusive=True)

# 队列的名称
queue_name = result.method.queue
print(queue_name)

# 5. 绑定队列到 exchange
channel.queue_bind(exchange='logs', queue=queue_name)


def print_log(ch, method, properties, body):
    print('打印日志: %s' % body.decode())


def write_log(ch, method, properties, body):
    with open('rabbitmq.log', 'wb') as f:
        f.write(body)
        print('已记录日志[%s]到文件rabbitmq.log' % body.decode())


# 通过命令行获取回调函数
callback = sys.argv[1] == 'print' and print_log or write_log

# 6. 消息处理
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()