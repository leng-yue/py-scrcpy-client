from socket import socket
from typing import Dict, List, Optional

from pydantic import BaseModel


class RunMode(BaseModel):
    Pvp: str
    Earning: str
    All: List[str]


runmode = RunMode(Pvp="pvp", Earning="earning", All=["pvp", "earning"])
