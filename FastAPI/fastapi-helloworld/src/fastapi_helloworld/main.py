from fastapi import FastAPI

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

@app.post("/chat/start")
def start_chat(messages:dict):
    print(messages)
    return {"messages": messages}
    

@app.post("/chat")
def chat(messages:dict):
    return {"message": "Hello World"}
   
def try_pytest():
    assert root() == {"message": "Hello World"}

try_pytest()