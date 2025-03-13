import requests
from requests import Response


class QuestionProClient:
    def __init__(
        self,
        api_key: str,
        organization_id: str,
        env: str = "com",  # depends on data center
        language_id: int = 250,
    ):
        self.api_key = api_key
        self.env = env
        self.language_id = language_id
        self.organization_id = organization_id

    @property
    def organization_url(self):
        return f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}"

    @property
    def headers(self):
        return {"Content-Type": "application/json", "api-key": self.api_key}

    def get_organization(self) -> Response:
        return requests.get(self.organization_url, headers=self.headers)

    def update_organization(self, data: dict = {}) -> Response:
        return requests.put(self.organization_url, headers=self.headers, json=data)

    def get_departments(self, page: int = 1, per_page: int = 100) -> Response:
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments?page={page}&perPage={per_page}"

        return requests.get(url, headers=self.headers)

    def get_departments(self, department_id: str) -> Response:
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments/{department_id}"

        return requests.get(url, headers=self.headers)

    def create_department(self, data: dict = {}) -> Response:
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments"

        return requests.post(url, headers=self.headers, json=data)

    def update_department(self, department_id: str, data: dict = {}) -> Response:
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments/{department_id}"
        
        return requests.put(url, headers=self.headers, json=data)
    
    def delete_department(self, department_id: str):
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments/{department_id}"

        return requests.delete(url, headers=self.headers)

    def get_users_from_organization(self, page: int = 1, per_page: int = 100):
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/users?page={page}&perPage={per_page}"
        
        return requests.get(url, headers=self.headers)

    def get_users_from_department(self, department_id: str, page: int = 1, per_page: int = 100):
        url = f"https://api.questionpro.{self.env}/a/api/v2/organizations/{self.organization_id}/departments/{department_id}/users?page={page}&perPage={per_page}"

        return requests.get(url, headers=self.headers)
