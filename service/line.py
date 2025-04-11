import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

LINE_API_URL = "https://api.line.me/v2/bot/profile/"

class LineService:
    
    def __init__(self, channel_access_token):
        self.headers = {
            "Authorization": f"Bearer {channel_access_token}"
        }

    def get_user_profile(self, user_id):
        url = f"{LINE_API_URL}{user_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            profile_data = response.json()
            logger.info(f"Profile data for user {user_id}: {profile_data}")
            return profile_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching profile for user {user_id}: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response text: {e.response.text}")
            return None
        
        
    def send_text_message(self, user_id, text):
        url = "https://api.line.me/v2/bot/message/push"
        payload = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
        try:
            response = requests.post(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to LINE user {user_id}: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response text: {e.response.text}")
            return None