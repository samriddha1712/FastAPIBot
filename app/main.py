from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(title="RAG Chatbot with Complaint System")

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router at the root level since we've already specified the /api prefix in the route paths
app.include_router(router)

# Add a root endpoint for health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}
