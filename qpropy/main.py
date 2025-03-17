import logging
from typing import List, Dict, Any

from qpropy.fetch import QuestionProClient
from qpropy.util.parse import _parse_response

# Setup logging instead of print statements
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SurveyHandler:
    def __init__(self, client: QuestionProClient):
        self.client = client

    def get_responses(self, count_responses: int = 100):
        responses: List[Dict[str, Any]] = self.client.get_responses(
            per_page=count_responses
        )

        result = []

        for response in responses:
            try:
                response_obj = _parse_response(response)
                result.append(response_obj)
            except Exception as e:
                logger.error(
                    f"Error parsing response {response.get('responseID', 'Unknown')}: {e}"
                )

        return result


class SurveyCreator:
    def __init__(self, client: QuestionProClient):
        self.client = client
        self.survey_metadata = {}
        self.question_metadata = []
        self.survey_data = []

    def create_survey(self, name: str, folder_id: int):
        self.metadata = self.client.create_survey({"name": name, "folderID": folder_id})
        self.client.survey_id = self.metadata["surveyID"]
        
    def delete_survey(self):
        self.client.delete_survey()
        
    def create_survey_data(self, survey_data):
        self.survey_data = survey_data
        for question_data in self.survey_data:
            response = self.client.create_question(question_data)
            self.question_metadata.append(response)
        
    def refresh_metadata(self):
        self.metadata = self.client.get_survey()
        
    def refresh_question_metadata(self):
        self.question_metadata = self.client.get_questions()
        
    @property
    def question_code_to_id(self):
        return {question['code']: question['questionID'] for question in self.question_metadata} 
    
    def update_survey_data(self, data: dict = {}):
        return self.client.update_survey(data)
    
    # fail
    def update_question_data(self, question_code: str, data: dict = {}):
        question_id = self.question_code_to_id[question_code]
        return self.client.update_question(question_id, data)
        
            
