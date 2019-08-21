
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

print(requests.get(URL, headers=HEADERS, data=DATA).text)
