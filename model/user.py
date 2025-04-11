from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Visitor:
    token : str
    id : Optional[str] = None
    username : Optional[str] = None
    status : Optional[str] = None
    ts : Optional[str] = None
    name : Optional[str] = None
    department : Optional[str] = None
    updated_at : Optional[datetime] = None