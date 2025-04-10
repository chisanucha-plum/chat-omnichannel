from typing import Optional
import pytz
import requests
from urllib.parse import urlencode
from datetime import datetime

from model.configuration import Configuration
from model.user import Visitor

class RocketChatClient:
    def __init__ (self):
        config = Configuration.get_config()
        self.host = config.rocket_chat.host
    
    def get(self, path, params: dict = None):
        """
        Get a request to the Rocket.Chat API.
        """
        url = f"{self.host}{path}"        
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            url += f"?{query_string}"
            
        response = requests.get(url)
        
        if not response.ok:
            raise requests.exceptions.HTTPError(f"Error: {response.status_code} - {response.text}")
    
        return response.json()
        
    def post(self,path, json : Optional[dict] = None, params=None):
        """
        Post a request to the Rocket.Chat API.
        """
        url = f"{self.host}{path}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(url, json=json, headers=headers, params=params)
        
        if not response.ok:
            raise requests.exceptions.HTTPError(f"Error: {response.status_code} - {response.text}")
        
        return response
    
    def _map_visitor_data(self,visitor: dict) -> Visitor:
        """Map the visitor data from Rocket.Chat to the Visitor model."""
        
        if visitor.get("_updatedAt") is not None:
            updated_at = visitor["_updatedAt"]
            updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            updated_at =  updated_at.astimezone(pytz.timezone('Asia/Bangkok'))
             
            visitor["_updatedAt"] = updated_at
            
        
        return Visitor(
            id=visitor.get('_id'),
            token=visitor.get('token'),
            name=visitor.get('name'),
            username=visitor.get('username'),
            status=visitor.get('status'),
            ts=visitor.get('ts'),
            department=visitor.get('department'),
            updated_at=visitor.get('_updatedAt'),
        )

    def create_livechat_visitor(self,visitor:Visitor):
        """
        Create a livechat visitor in Rocket.Chat.
        """
        try:
            
            visitor_data = {key: value for key, value in {
                "token": visitor.token,
                "name": visitor.name,
                "username": visitor.username,
                "status": visitor.status,
                "ts": visitor.ts,
                "department": visitor.department
            }.items() if value is not None}
            
            response = self.post(
                '/api/v1/livechat/visitor',
                json={
                    "visitor": visitor_data
                }
            )
            return response.json()
        except Exception as e:
            print(f"Error creating livechat visitor: {e}")
            return None
        
    def get_livechat_visitor(self,token : str) :
        
        try:
            
            response = self.get(
                '/api/v1/livechat/visitor/{token}'.format(token=token),
            )
            
            if response.get("visitor") is None:
                raise ValueError("Visitor not found")
            
            return self._map_visitor_data(response.get("visitor"))
        
        except Exception as e:
            print(f"Error get livechat visitor: {e}")
            return None
        
        
