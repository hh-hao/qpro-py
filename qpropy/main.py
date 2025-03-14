import logging
from typing import List, Dict, Any

from qpropy.fetch import QuestionProClient
from qpropy.util.parse import _parse_response

# Setup logging instead of print statements
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestionProHandler:
    def __init__(self, client: QuestionProClient):
        self.client = client

    def get_responses(self, count_responses: int = 100):
        responses: List[Dict[str, Any]] = self.client.get_responses(per_page=count_responses)

        result = []

        for response in responses:
            try:
                response_obj = _parse_response(response)
                result.append(response_obj)
            except Exception as e:
                logger.error(f"Error parsing response {response.get('responseID', 'Unknown')}: {e}")

        return result
    
    