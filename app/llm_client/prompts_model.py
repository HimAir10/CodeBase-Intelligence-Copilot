from pydantic import BaseModel, Field

class PromptMessage(BaseModel): 
    role  : str
    content : str


class PromptTemplate(BaseModel): 
    id : str
    version : str
    description : str 

    messages : list[PromptMessage]

