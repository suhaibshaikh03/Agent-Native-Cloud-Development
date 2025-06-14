from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()
# def get_user_count_from_db(limit:int = 100):
#     print("Getting user count from db")
#     return 100

# @app.get("/count")
# def get_info(user_count: Annotated[int, Depends(get_user_count_from_db)]):
#     return {"count": user_count}

def depfunc1(num:int): 
    num = int(num)
    num += 1
    return num

def depfunc2(num): 
    num = int(num)
    num += 2
    return num

@app.get("/main/{num}")
def get_main(num: int, num1:  Annotated[int,Depends(depfunc1)], num2: Annotated[int,Depends(depfunc2)]):
    # Assuming you want to use num1 and num2 in some way
    #       1      2      3
    total = num + num1 + num2
    return {"Pakistan":total,
            "num":num,
            "num1":num1,
            "num2":num2}