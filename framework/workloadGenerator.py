import random
import simpy
from simpy.events import AllOf
from entity.customer import Customer
from framework.Clinet import Client
from framework.MessageBus import MessageBus
from framework.Server import Server


class WorkLoad:
    # 生成一组Client，模拟对Server的访问
    def __init__(self, numClient, env : simpy.Environment, arrivalRate):
        self.numClient = numClient
        self.env = env
        self.clientId = 0
        self.timeCostList = []
        self.arrivalRate = arrivalRate

        self.messageBus = MessageBus(self.env)

        # 使env注册执行时自动执行下面的run函数
        self.env.process(self.run())

    def run(self):
        client_events = []

        # 设计回调记录时间的函数
        def callbackRecodTime(time: float):
            # 记录时间
            self.timeCostList.append(time)

        while self.numClient != 0:
            currentId = self.clientId
            # Client端使用户进行工作
            currentClient = Client(self.env, currentId, self.messageBus, callbackRecodTime)


            # 启动Client端
            print(f"start Client {self.clientId} at {self.env.now}")
            # 记录Client端事件
            client_events.append(self.env.process(currentClient.run()))
            # 泊松分布等待一段时间(模拟下次用户到来,内部间隔实际服从指数分布)
            # yield self.env.timeout(stats.poisson.rvs( self.arrivalRate ))
            yield self.env.timeout(random.expovariate(self.arrivalRate))
            self.clientId += 1
            self.numClient -= 1

        yield AllOf(self.env, client_events)

        print(f"Average time cost: {self.getAveCostTime()}  s  (单位是秒)")


    def getAveCostTime(self) -> float:
        return sum(self.timeCostList) / len(self.timeCostList)
