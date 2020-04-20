from locust import HttpLocust, Locust, TaskSet, task, between
import json

class HealthCheckAPI(TaskSet):
    @task(1)
    def index(self):
        with self.client.get("/", catch_response=True) as response:
            print("HTTP Status" + str(response.status_code))
            if response.status_code > 400:
                response.success()
    @task(1)
    def healthCheck(self):
        with self.client.get("/health", catch_response=True) as response:
            jdata = json.loads(response.content)
            if response.status_code != 200 and jdata["message"] != "found a file":
                response.failure("Wrong Response")

class Start(HttpLocust):
    task_set = HealthCheckAPI
    wait_time = between(1,5)