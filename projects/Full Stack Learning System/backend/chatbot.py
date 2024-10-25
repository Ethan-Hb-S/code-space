from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests
import json
import uuid
import config

def get_access_token(service_account_key_path):
    credentials = Credentials.from_service_account_file(service_account_key_path, scopes=['https://www.googleapis.com/auth/dialogflow'])
    request = Request()

    # Refresh the access token before making the request
    credentials.refresh(request)

    return credentials.token

def detect_intent(project_id, session_id, text, service_account_key_path, language_code='en'):
    access_token = get_access_token(service_account_key_path)
    url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/agent/sessions/{session_id}:detectIntent"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "queryInput": {
            "text": {
                "text": text,
                "languageCode": language_code
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise

# Generate session id
def generateSessionID():
    session_id = str(uuid.uuid4())
    return session_id

def startConversion(session):
    return conversation("Hello", session)


# Converse with the chatbot in a session
def conversation(query, session):
    project_id = "yellowfrogs"
    language_code = "en"
    service_account_key_path = config.GOOGLE_APPLICATION_CREDENTIALS

    response = detect_intent(project_id, session, query, service_account_key_path, language_code)

    return response['queryResult']['fulfillmentText']
