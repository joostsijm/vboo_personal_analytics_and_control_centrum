
"""
Test application for api request. Change authorization if necessary
"""

import requests

URL = 'http://localhost:5000/api/request/listed/country'
HEADERS = {
    'Authorization': 'ZDoJMSKBKz0TNhfOcCRiraCxb0UHqnbVPIQkP6yJkTdSkvysxnyQgu0U5oQ0NBa9'
}

DATA = {
    'test': 'true',
}

PARAMS = {
    'alt': True
}

RESULT = requests.post(
    URL,
    headers=HEADERS,
    data=DATA,
    params=PARAMS
)
print(RESULT.text)
