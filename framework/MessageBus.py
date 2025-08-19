import simpy

class MessageBus:

    _instance = None

    def __new__(cls, env = None):
        # 单例模式
        if cls._instance is None:
            cls._instance = super(MessageBus, cls).__new__(cls)
            if env is not None:
                cls._instance.init(env)
        return cls._instance
    def init(self, env):
        self.env = env
        self.channels = {}

    def getChannel(self, channel_name):
        if channel_name not in self.channels:
            self.channels[channel_name] = simpy.Store(self.env)
        return self.channels[channel_name]