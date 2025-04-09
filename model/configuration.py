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

    @staticmethod
    def from_dict(obj: Any) -> 'Channel':
        _platform = str(obj.get("platform"))
        _name = str(obj.get("name"))
        _channel_id = str(obj.get("channel_id"))
        _channel_secret = str(obj.get("channel_secret"))
        return Channel(_platform, _name, _channel_id, _channel_secret)

@dataclass
class Configuration:
    channels: List[Channel]

    @staticmethod
    def from_dict(obj: Any) -> 'Configuration':
        _channels = [Channel.from_dict(y) for y in obj.get("channels")]
        return Configuration(_channels)
    
    @staticmethod
    @lru_cache()
    def get_config():
        
        site = os.environ.get("SERVICE_SITE","development")
        with open(f"config.{site}.json", "r") as f:
                        
            json_data =  json.loads(f.read())
            
            return Configuration.from_dict(json_data)
        