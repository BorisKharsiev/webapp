from locust import HttpUser, task, between
import random

class TaskManagerUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        # Создаем пользователя и получаем токен
        self.client.post("/users/", json={
            "username": f"testuser{random.randint(1, 1000)}",
            "email": f"test{random.randint(1, 1000)}@example.com",
            "password": "testpass123"
        })
        
        response = self.client.post("/token", data={
            "username": "testuser",
            "password": "testpass123"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    @task(3)
    def create_task(self):
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/tasks/", json={
            "title": f"Test Task {random.randint(1, 1000)}",
            "description": f"Test Description {random.randint(1, 1000)}",
            "status": random.choice(["pending", "in_progress", "completed"]),
            "priority": random.randint(0, 5)
        }, headers=headers)

    @task(2)
    def get_tasks(self):
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/tasks/", headers=headers)

    @task(1)
    def get_top_tasks(self):
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/tasks/top/", headers=headers)

    @task(1)
    def search_tasks(self):
        if not self.token:
            return
            
        headers = {"Authorization": f"Bearer {self.token}"}
        search_terms = ["test", "task", "important", "urgent"]
        self.client.get(f"/tasks/?search={random.choice(search_terms)}", headers=headers) 