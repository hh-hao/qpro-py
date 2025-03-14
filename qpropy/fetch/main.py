import requests
from requests import Response
from typing import Optional, Dict, Any


class QuestionProClient:
    def __init__(self, api_key: str, env: str = "com", language_id: int = 250):
        self.api_key = api_key
        self.env = env
        self.language_id = language_id

        # Instance variables with None default
        self.organization_id: Optional[int] = None
        self.department_id: Optional[int] = None
        self.user_id: Optional[int] = None
        self.folder_id: Optional[int] = None
        self.survey_id: Optional[int] = None

    @property
    def base_url(self) -> str:
        return f"https://api.questionpro.{self.env}/a/api/v2"

    @property
    def headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "api-key": self.api_key}

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Helper method to send API requests and handle responses."""
        response: Response = requests.request(
            method, url, headers=self.headers, **kwargs
        )

        if response.status_code == 204:  # No content (DELETE requests)
            return {"message": "Success"}

        data: dict = response.json()

        if response.ok:
            return data.get("response", data)

        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
        raise ValueError(data)  # Fallback error

    def regenerate_api_key(self) -> Dict[str, Any]:
        return self._request("GET", f"{self.base_url}/apikey/regenerate")

    # -------------- Organization API --------------
    def get_organization(self) -> Dict[str, Any]:
        if not self.organization_id:
            raise ValueError("Organization ID is not set.")
        return self._request(
            "GET", f"{self.base_url}/organizations/{self.organization_id}"
        )

    def update_organization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.organization_id:
            raise ValueError("Organization ID is not set.")
        return self._request(
            "PUT", f"{self.base_url}/organizations/{self.organization_id}", json=data
        )

    # -------------- Department API --------------
    def get_departments(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"{self.base_url}/organizations/departments",
            params={"page": page, "perPage": per_page},
        )

    def get_department(self) -> Dict[str, Any]:
        if not self.department_id:
            raise ValueError("Department ID is not set.")
        return self._request(
            "GET", f"{self.base_url}/organizations/departments/{self.department_id}"
        )

    def create_department(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST", f"{self.base_url}/organizations/departments", json=data
        )

    def update_department(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.department_id:
            raise ValueError("Department ID is not set.")
        return self._request(
            "PUT",
            f"{self.base_url}/organizations/departments/{self.department_id}",
            json=data,
        )

    def delete_department(self) -> Dict[str, Any]:
        if not self.department_id:
            raise ValueError("Department ID is not set.")
        return self._request(
            "DELETE", f"{self.base_url}/organizations/departments/{self.department_id}"
        )

    # -------------- User API --------------
    def get_users_from_organization(
        self, page: int = 1, per_page: int = 100
    ) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"{self.base_url}/organizations/users",
            params={"page": page, "perPage": per_page},
        )

    def get_users_from_department(
        self, page: int = 1, per_page: int = 100
    ) -> Dict[str, Any]:
        if not self.department_id:
            raise ValueError("Department ID is not set.")
        return self._request(
            "GET",
            f"{self.base_url}/organizations/departments/{self.department_id}/users",
            params={"page": page, "perPage": per_page},
        )

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"{self.base_url}/organizations/users/search",
            params={"emailAddress": email},
        )

    def get_user(self) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")
        return self._request("GET", f"{self.base_url}/users/{self.user_id}")

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"{self.base_url}/users", json=data)

    def update_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")
        return self._request("PUT", f"{self.base_url}/users/{self.user_id}", json=data)

    def delete_user(self) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")
        return self._request("DELETE", f"{self.base_url}/users/{self.user_id}")

    # -------------- Folder API --------------
    def get_folders(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")
        return self._request(
            "GET",
            f"{self.base_url}/users/{self.user_id}/folders",
            params={"page": page, "perPage": per_page},
        )

    def get_folder(self) -> Dict[str, Any]:
        if not self.folder_id:
            raise ValueError("Folder ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")
        return self._request(
            "GET", f"{self.base_url}/users/{self.user_id}/folders/{self.folder_id}"
        )

    def create_folder(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.folder_id:
            raise ValueError("Folder ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "POST", f"{self.base_url}/users/{self.user_id}/folders", json=data
        )

    def update_folder(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.folder_id:
            raise ValueError("Folder ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "PUT",
            f"{self.base_url}/users/{self.user_id}/folders/{self.folder_id}",
            json=data,
        )

    def delete_user(self) -> Dict[str, Any]:
        if not self.folder_id:
            raise ValueError("Folder ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "DELETE", f"{self.base_url}/users/{self.user_id}/folders/{self.folder_id}"
        )

    # -------------- Survey API --------------
    def get_surveys_by_user(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/users/{self.user_id}/surveys?page={page}&perPage={per_page}",
        )

    def get_surveys_by_folder(
        self, page: int = 1, per_page: int = 100
    ) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")
        if not self.folder_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/users/{self.user_id}/folders/{self.folder_id}/surveys?page={page}&perPage={per_page}",
        )

    def get_survey(self):
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "GET", f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}"
        )

    def create_survey(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "POST", f"{self.base_url}/users/{self.user_id}/surveys", json=data
        )

    def update_survey(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "PUT",
            f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}",
            json=data,
        )

    def delete_survey(self) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "DELETE", f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}"
        )

    def get_survey_auth(self) -> Dict[str, any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "GET", f"{self.base_url}/surveys/{self.survey_id}/authentication"
        )

    def update_survey_auth(self, data: Dict[str, any]) -> Dict[str, any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")
        if not self.user_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "POST",
            f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}/authentication",
            json=data,
        )

    # -------------- Block API --------------

    #####

    # -------------- Question API --------------
    def get_questions(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/surveys/{self.survey_id}/questions?page={page}&perPage={per_page}",
        )

    def get_question(self, question_id: int):
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET", f"{self.base_url}/surveys/{self.survey_id}/questions/{question_id}"
        )

    def create_question(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("User ID is not set.")

        return self._request(
            "POST",
            f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}/questions",
            json=data,
        )

    def update_question(self, question_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "PUT",
            f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}/questions/{question_id}",
            json=data,
        )

    def delete_question(self, question_id: int) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "DELETE",
            f"{self.base_url}/users/{self.user_id}/surveys/{self.survey_id}/questions/{question_id}",
        )

    # -------------- Answer API --------------
    def get_answers(
        self, question_id, page: int = 1, per_page: int = 100
    ) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/surveys/{self.survey_id}/questions/{question_id}/answers?page={page}&perPage={per_page}",
        )

    def get_answer(self, question_id: int, answer_id: int) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/surveys/{self.survey_id}/questions/{question_id}/answers/{answer_id}",
        )

    def delete_answer(self, question_id: int, answer_id: int) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "DELETE",
            f"{self.base_url}/surveys/{self.survey_id}/questions/{question_id}/answers/{answer_id}",
        )

    # -------------- Reponses API --------------
    def get_responses(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/surveys/{self.survey_id}/responses?page={page}&perPage={per_page}"
        )
        
    def get_response(self, response_id: int):
        if not self.survey_id:
            raise ValueError("Survey ID is not set.")

        return self._request(
            "GET",
            f"{self.base_url}/surveys/{self.survey_id}/responses/{response_id}"
        )
        
        