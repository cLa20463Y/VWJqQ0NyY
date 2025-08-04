# 代码生成时间: 2025-08-05 00:00:57
import os
import requests
from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser

# 性能测试脚本
class PyramidPerformanceTestUser(FastHttpUser):
    # 等待请求之间的时间
    wait_time = between(1, 3)

    # 用户的性能测试函数
    @task
    def index(self):
        # 模拟GET请求到首页
        self.client.get("/")

    @task(3)  # 这个任务会执行3次
    def item_page(self):
        # 模拟GET请求到一个特定的页面
        self.client.get("/item/123")

    # 可以添加更多的测试任务...

# 性能测试入口点
if __name__ == "__main__":
    # 使用Locust运行性能测试
    os.system("locust -f performance_test_script.py")  # 启动Locust性能测试
