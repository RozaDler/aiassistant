from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.user_query import router as ask_router

#cors middleweare because backend and front end running on different port

app=FastAPI(title="Ai Assistant", description="API for AI Assistant Chatbot")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# middleweare exception handlers
app.middleware("http")(catch_exception_middleware)

# routers

# 1. upload pdf documents
app.include_router(upload_router)

# 2. asking query
app.include_router(ask_router)