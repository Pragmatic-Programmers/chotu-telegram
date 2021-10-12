import os

class Config:
    TOKEN = os.environ.get("TOKEN")
    ID = int(os.environ.get("ID"))
    HASH = os.environ.get("HASH")
