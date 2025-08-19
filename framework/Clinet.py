import simpy

from entity.customer import Customer
from framework.MessageBus import MessageBus
from framework.Server import Server


class Client:

    def __init__(self, env: simpy.Environment, id : int, messageBus : MessageBus, callbackRecordTime : callable):
        self.env = env
        # 根据id构建用户
        self.customer = Customer(id)
        self.messageBus = messageBus
        self.startTime = None
        self.endTime = None
        self.callbackRecordTime = callbackRecordTime

    def run(self):
        # 模拟用户的购物流程
        self.startTime = self.env.now

        completionEvent = self.env.event()

        # 用messageBus
        requestChannel = self.messageBus.getChannel('customerRequest')

        yield requestChannel.put({  # 通过这个“bus”传递信息
            "customer": self.customer,
            "completionEvent": completionEvent
        })

        yield completionEvent  # 等待服务完成


        self.endTime = self.env.now

        self.callbackRecordTime(self.getCostTime())

    def getCostTime(self) -> float:
        print(f"customer {self.customer.id} cost time: {self.endTime - self.startTime}")
        return self.endTime - self.startTime