from fastapi import FastAPI
from pydantic import BaseModel

class MessageInput(BaseModel):
    role: str
    content: str


class ClassInput(BaseModel):
    message : list[MessageInput]


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/status")
# def status():
#     return {"status": "ok"}

# @app.post("/chat/start")
# def start_chat(messages:dict):
#     print(messages)
#     return {"messages": messages}
    

@app.post("/chat")
def chat(messages:ClassInput):
    print("[+] Chat Input model dump:", messages.model_dump())
    print("[+] Chat Input model dump:", messages.model_dump()["message"])
    print("[+] Chat Input model dump type :", type(messages.model_dump()))
    print("[+] Chat Input Type:", type(messages))
    print("[+] Chat Message: ",messages.message)
    print("[+] Chat Input:", type(messages.message))
    return {"message": "Hello World"}
