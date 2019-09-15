## Exchange Topic
> Direct类型的Exchange可以根据具体的名字进行路由匹配, Topic类型的Exchange能够根据某个模式进行路由匹配
### 1. 路由模式
我们在发送消息到RabbitMQ队列时, 一般会为routing key指定具体的名字, 例如:
```python
channel.basic_publish(exchange='logs', routing_key='routing_name', body='message')
```
使用模式进行路由匹配, 可以不用指定具体的名字, 通过一定的模式进行匹配, RabbitMQ的模式格式如下:
1. 必须是由点分割的单词列表, 例如: `user.log.serious`, `sys.log`等
2. `*`代替不确定的1个单词, 例如: `user.log.*`, 那么`user.log.serious`, `user.log.info`能够匹配该模式, 但是`user.log.info.level`无法匹配
3. `#`代替0个或多个单词, 例如: `user.#.log`, 那么`user.log.serious`、`user.serious.my.log`、`user.log`都能匹配该模式