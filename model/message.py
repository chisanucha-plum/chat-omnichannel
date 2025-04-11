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
    text : str
    timestamp : datetime
    type : MessageType
    
@dataclass    
class Sender:
    id : str
    display_name : str
    Platform : PlatformType
    
@dataclass
class Receiver:
    id : str
    display_name : str
    Platform : PlatformType
    
       
@dataclass
class Messages:
    sender: Sender
    receiver: Receiver
    platform: PlatformType
    messages: list[Message]