# Time: 2019/9/8  14:27
# Author jzh
# File custom.py

import pika

import tasks

# 注册任务
task_register = {
    'message': tasks.send_message,
    'email': tasks.send_email
}


# 1. 获取连接对象
connection_host = '127.0.0.1'
connection_credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connection_host, credentials=connection_credentials))

# 2. 获取channel对象
channel = connection.channel()

# 3. 通过channel声明my_queue队列, 如果队列不存在则创建队列, 如果存在则忽略
channel.queue_declare(queue='my_queue')


# 4. 定义消息处理的函数
def callback(ch, method, properties, body):
    """
    回调函数
    :return:
    """
    # 判断任务是否注册
    task_name = body.decode()
    if task_name not in task_register:
        print('Error: task not register')
        return

    task_register[task_name]()


# 5. 关联消息队列
channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

# 6. 启动消费者
channel.start_consuming()

