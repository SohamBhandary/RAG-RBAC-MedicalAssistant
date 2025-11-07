from fastapi import APIRouter,Depends,Form
from Auth.routes import authenticate
from Chat.chat_query import answer_query


router=APIRouter()

@router.post("/chat")
async def chat(user=Depends(authenticate),message:str=Form(...)):
    return await answer_query(message,user["role"])