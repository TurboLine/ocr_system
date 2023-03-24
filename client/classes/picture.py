from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Picture:
    nickname: str
    time_application: datetime
    file_name: str
    file_url: str
    text_list: list

