from pydantic import BaseModel

# response_model = response schema
class Blog(BaseModel):
    title:str
    body: str

class ShowBlog(Blog):
    class Config():
        orm_mode = True