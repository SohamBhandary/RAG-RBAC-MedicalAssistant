from fastapi import FastAPI
from Auth.routes import router as auth_router
from Docs.routes import router as  docs_router
from Chat.routes import router as chat_router




app=FastAPI()
app.include_router(auth_router)
app.include_router(docs_router)
app.include_router(chat_router)




@app.get("/health")
def health_check():
    return {"message":"ok"}

