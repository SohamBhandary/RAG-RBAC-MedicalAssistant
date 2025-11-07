from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from .models import Signup
from .hash_utils import hash,verify
from Config.db import user_collections

router=APIRouter()
security=HTTPBasic()

def authenticate(crendtials:HTTPBasicCredentials=Depends(security)):
    user=user_collections.find_one({"username":crendtials.username})
    if not user or not verify(crendtials.password,user['password']):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return {"username":user["username"],"role":user["role"]}

    
@router.post("/signup")
def signup(req:Signup):
    if user_collections.find_one({"username":req.username}):
        raise HTTPException(status_code=400,detail="User already exsists")
    user_collections.insert_one({
        "username":req.username,
        "password": hash( req.password),
        "role":req.role
    })
    return {"message":"user created"}

@router.get("/login") 
def login(user=Depends(authenticate)):
    return {"message":f"welcome {user['username']}","role":user["role"]}
    

