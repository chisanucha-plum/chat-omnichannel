from functools import lru_cache
from typing import List
from typing import Any
from dataclasses import dataclass
import json
import os

@dataclass
class Channel:
    platform: str
    name: str
    channel_id: str
    channel_secret: str
    user_id: str 
    access_token: str 

    @staticmethod
    def from_dict(obj: Any) -> 'Channel':
        _platform = str(obj.get("platform"))
        _name = str(obj.get("name"))
        _channel_id = str(obj.get("channel_id"))
        _channel_secret = str(obj.get("channel_secret"))
        _user_id = str(obj.get("user_id"))
        _access_token = str(obj.get("access_token"))
        return Channel(_platform, _name, _channel_id, _channel_secret, _user_id, _access_token)

@dataclass
class RokcetChat:
    host: str
    @staticmethod
    def from_dict(obj: Any) -> 'RokcetChat':
        _host = str(obj.get("host"))
       
        return RokcetChat(_host)

@dataclass
class Configuration:
    channels: List[Channel]
    rocket_chat: RokcetChat

    @staticmethod
    def from_dict(obj: Any) -> 'Configuration':
        _channels = [Channel.from_dict(y) for y in obj.get("channels")]
        _rocket_chat = RokcetChat.from_dict(obj.get("rocket_chat"))
        return Configuration(_channels,_rocket_chat)
    
    @staticmethod
    @lru_cache()
    def get_config():

        site = os.getenv("SERVICE_SITE","development")
        config_file =f"config.{site}.json" 

        with open(config_file, "r", encoding="utf-8") as config_str:
            content = config_str.read()
            json_data = json.loads(content)
        
            return Configuration.from_dict(json_data)
        