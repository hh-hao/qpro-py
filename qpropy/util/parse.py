import logging
from typing import Dict, Any, List

from qpropy.schemas.response_schemas import (
    Response,
    ResponseItem,
    AnswerItem,
    AnswerValue,
    Location,
    CustomVariables,
)

# Setup logging instead of print statements
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _parse_response_item(response_item: Dict[str, Any]) -> ResponseItem:
    """Parse individual response items (questions and answers)."""
    answer_values: List[Dict[str, Any]] = response_item.get("answerValues", [])
    answer_items = []

    for answer_value in answer_values:
        try:
            value_obj = AnswerValue(**answer_value.pop("value"))
            answer_item = AnswerItem(**answer_value, value=value_obj)
            answer_items.append(answer_item)
        except Exception as e:
            logger.error(f"Error parsing answer value: {e}")

    return ResponseItem(
        **{key: value for key, value in response_item.items() if key != "answerValues"},
        answerValues=answer_items,
    )


def _parse_response(response: Dict[str, Any]) -> Response:
    """Convert raw API response into a structured Response object."""
    response_set = response.get("responseSet", [])
    response_set_objs = [_parse_response_item(item) for item in response_set]

    location = Location(**response.get("location", {}))
    custom_variables = CustomVariables(**response.get("customVariables", {}))

    return Response(
        **{
            key: value
            for key, value in response.items()
            if key not in ["location", "customVariables", "responseSet"]
        },
        location=location,
        customVariables=custom_variables,
        responseSet=response_set_objs,
    )
