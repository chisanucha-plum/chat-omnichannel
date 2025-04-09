from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PlatformType(str,Enum):
    LINE = "LINE"
    FACEBOOK = "FACEBOOK"

class MessageType(str,Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    FILE = "FILE"
    STICKER = "STICKER"

@dataclass
class Message:
    type : MessageType
    text : setattr
    timestamp : datetime
    
@dataclass
class Messages:
    sender: str
    receiver: str
    platform: PlatformType
    messages: list[Message]