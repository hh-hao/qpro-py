# QuestionPro in Python

## Introduction
`qpropy` is a Python client for:
- Interacting with the QuestionPro API & Process data to usable format. It simplifies API calls for managing organizations, departments, users, surveys, questions, and responses.
- Process data to usable format.

## Installation
Ensure you have `requests` installed:
```sh
pip install -r requirements.txt
```

## Initialization
```python
from qpropy import QuestionProClient

# Initialize client with API Key
api_key = "your_api_key"
client = QuestionProClient(api_key)
```

### Setting Required IDs
Some methods require setting specific IDs before use:
```python
client.organization_id = 12345
client.department_id = 67890
client.user_id = 112233
client.folder_id = 445566
client.survey_id = 778899
```

### API Usage

See QuestionPro API documentations: https://www.questionpro.com/api/getting-started.html

| **Category**  | **Method** | **Description** | **Example Usage** |
|--------------|------------|----------------|-----------------|
| **Organization** | `get_organization()` | Retrieve organization details | `client.get_organization()` |
| | `update_organization(data)` | Update organization info | `client.update_organization({"name": "Updated Organization Name"})` |
| **Department** | `get_departments()` | List all departments | `client.get_departments()` |
| | `create_department(data)` | Create a new department | `client.create_department({"name": "Marketing"})` |
| **User** | `get_users_from_organization()` | Retrieve all users | `client.get_users_from_organization()` |
| | `get_user_by_email(email)` | Get user details by email | `client.get_user_by_email("user@example.com")` |
| | `create_user(data)` | Create a new user | `client.create_user({"departmentID": 1234,"firstName": "firstname"})` |
| **Survey** | `get_surveys_by_user()` | List surveys assigned to a user | `client.get_surveys_by_user()` |
| | `create_survey(data)` | Create a new survey | `client.create_survey({"name": "Customer Feedback"})` |
| | `get_survey()` | Get details of a specific survey | `client.get_survey()` |
| **Question** | `get_questions()` | Retrieve all questions in a survey | `client.get_questions()` |
| | `create_question(data)` | Add a new question to a survey | `client.create_question({"text": "How satisfied are you?"})` |
| **Response** | `get_responses()` | Retrieve all responses for a survey | `client.get_responses()` |
| | `create_response(data)` | Submit a response | `client.create_response({"question_id": 123, "answer": "Very Satisfied"})` |
| | `get_response(response_id)` | Retrieve a specific response | `client.get_response(456)` |

### Process data to usable format

```python
from qpropy import QuestionProHandler

handler = QuestionProHandler(client)
handler.get_responses()
```

## Error Handling
Each method raises an exception if there’s an error. Example:
```python
try:
    data = client.get_organization()
    print(data)
except ValueError as e:
    print(f"Error: {e}")
```

## License
This project is licensed under the MIT License.

