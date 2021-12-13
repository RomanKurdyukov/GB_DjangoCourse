from locust import HttpUser, task, TaskSet
import re


def login(data):
    result = data.client.get("/auth/login/")
    token = re.search(r'[a-zA-Z0-9]{64}', result.text)
    data.client.post(
        "/auth/login/",
        {"username": "admin",
         "password": "admin",
         "csrf_token": token},
    )


def logout(data):
    result = data.client.get("/auth/logout/")
    token = re.search(r'[a-zA-Z0-9]{64}', result.text)
    data.client.post(
        "/auth/logout/",
        {"username": "admin",
         "password": "admin",
         "csrf_token": token,
         })


def index(data):
    data.client.get("/")


def profile(data):
    data.client.get("/products")


@task
class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
