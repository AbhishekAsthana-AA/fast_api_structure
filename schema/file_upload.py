from pydantic import BaseModel
from typing import Optional


class DownloadFileSchema(BaseModel):
    file_id: int
