from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

class UserResponse(BaseModel):
    status:str
    user_id:int

app = FastAPI()
 
#path parameters
@app.get("/info/{username}/{rollno}")
def read_info(username:str = Path(...,min_length=3,max_length=10) , rollno:int):
    if usename == "Suhaib":
        raise HTTPException(status_code=404,detail=f"username {Suhaib} not permitted")
    return {"username":username, "rollno":rollno}


# @app.get("/info/{usename}/{userid}")
# def read_info(username:str, userid:int = Path(..., gt=0, lt=100000)):
#     return {"username":username,
#             "userid":userid}


@app.get("/info/{userid}")
def read_info(username:str = Query(...,min_length=1, max_length=7), userid:int = Path(..., gt=0, lt=100000)):
    return {"username":username,
            "userid":userid}

# @app.post("/create-user")
# def create_user(name:str, age:int):
#     return {"name":name, "age":age, "status":"ok"}

#query parameters
@app.get("/users/all")
def get_all_users(limit: int | None = Query(..., gt=0,lt=100) ):
    print(f"limit: {limit}")
    if limit:
        return {"users":["Ameen Alam"]}
    else:
        return {"users":["Ameen Alam","Shehzad"]}
    


#body
# @app.post("/create-user")
# def create_user(user:User):
#     return {"name":user.name, "age":user.age, "status":"ok"}


@app.get("/create-user")
def create_user():
    return {"name": "Suhaib", "age":"21", "status":"ok"}



@app.post("/create-user", response_model=UserResponse)
def create_user(user: User, user_id: int):
    print("\n[USER]", user)
    return {"status":"user created", "user_id":user_id}  #error code 500 internal server if the schema UserResponse is not returned

# PUT -> Update
# DELETE -> Delete
