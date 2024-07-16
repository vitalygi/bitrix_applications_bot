from typing import List, Optional
from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field



class Product(Document):
    category: str
    subcategory: str
    description: str
    name: str
    price: int
    photos: List[str]
    region: str

