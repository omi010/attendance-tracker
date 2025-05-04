from pydantic import BaseModel

class Student(BaseModel):
    name: str
    roll_no: int
    class_name: str
    school: str
    contact: str
