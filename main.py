import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from app.routes.brief_routes import router as brief_router

app = FastAPI(
    title="AI Application API",
    description="Backend for AI Application",
    version="1.0.0"
)

app.include_router(brief_router)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
