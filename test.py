
"""
Test application for api request. Change authorization if necessary
"""

import requests

URL = 'http://localhost:5000/'
HEADERS = {
    'Authorization': 'cGwJNNbIhrKiMKjA4DuVhzL2YH8DxPDV37N5SAb6UbhYtFhYzgwhtmVS4iVloyEu'
}

DATA = {
    'test': 'true',
}

print(requests.get(URL, headers=HEADERS, data=DATA).text)
