from typing import List, Optional
from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field


class User(Document):
    id: int
    name: Optional[str] = None
    nickname: Optional[str] = None
    username: Optional[str] = None
    is_registered: bool = False
    register_date: Optional[str] = None


class Application(Document):
    id: int
    responsible: Optional[str] = ''
    direction: Optional[str] = ''
    pay_form: Optional[str] = ''
    payer: Optional[str] = ''
    article: Optional[str] = ''
    comments: Optional[str] = ''
    amount: Optional[int] = 0
    payment_date: Optional[str] = ''
    add_info: Optional[str] = ''
    file: Optional[str] = ''
    file_type: Optional[str] = ''
    is_checked: Optional[bool] = False
    user_id: int
