import simpy
import random
from entity.customer import Customer
from framework.MessageBus import MessageBus


class Server:

    def __init__(self, env: simpy.Environment, capacity:int, rate_select = 1 / 240, time_checkout = 30):
        self.env = env
        self.update_lock = simpy.Resource(env, capacity=capacity)
        self.messageBus = MessageBus(self.env)

        self.rate_select = rate_select
        self.time_checkout = time_checkout

        self.env.process(self.listen())

    def listen(self):

        requestChannel = self.messageBus.getChannel("customerRequest")
        # 持续监听
        while True:
            customerRequest = yield requestChannel.get()
            customer = customerRequest['customer']
            completionEvent = customerRequest['completionEvent']
            self.env.process(self.serveCustomer(customer, completionEvent))

    def selectItem(self, customer : Customer):
        print(f"Customer {customer.id} is selecting item")

        # 服从特定的指数分布
        yield self.env.timeout(random.expovariate(self.rate_select))
    def checkout(self, customer : Customer):
        # 结账
        print(f"Customer {customer.id} is checking out")

        # 30s
        yield self.env.timeout(self.time_checkout)

    def serveCustomer(self, customer: Customer, completionEvent):
        # 服务
        # with self.update_lock.request() as req:
        #     # 1. 排队等待
        #     yield req

        # 1. 挑选商品
        yield self.env.process(self.selectItem(customer))

        with self.update_lock.request() as req:
            # 2. 排队等待
            yield req
            # 3. 结账
            yield self.env.process(self.checkout(customer))

        # 通知客户端处理完毕
        completionEvent.succeed()
