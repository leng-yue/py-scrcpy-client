from socket import socket

from pydantic import BaseModel

# from typing import Dict, List, Optional


class ServerInfo(BaseModel):
    host: str
    port: int
    server: socket = None

    class Config:
        arbitrary_types_allowed = True
