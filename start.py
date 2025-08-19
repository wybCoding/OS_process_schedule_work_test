import simpy

from framework.Server import Server

if __name__ == '__main__':
    from framework.workloadGenerator import WorkLoad
    env = simpy.Environment()
    # 模拟服务器（正式部署时可能使用分布式，通过ip访问等，这里仅模拟）
    server = Server(env, 3, 1/240, 30)
    # 模拟前台工作流
    workLoad = WorkLoad(500, env, 1 / 60)
    print("启动工作")
    env.run()
