import os
import sys
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List, Dict
import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.schemas import RequestModel, AnswerModel, ErrorModel
from services.process import ProcessRequest
from config.config import config

app = FastAPI( title="Telegram Bot", 
    description="Telegram Bot to recevive and send messages")

# --- Definicion de Endpoints --- 
@app.get("/Health", summary="Health Check", description="Check if the server is running")
async def health():
    return {"status": "OK", "message": "Server is running"}

@app.post("/process", summary="Procceses the user request", description="Processes the user query and returns an answer")
async def process(req: RequestModel):
    try:

        if not req.message:
            return JSONResponse(status_code=400, content={"error": "Message is required"} )
        
        procces = ProcessRequest(req.message)
        response = procces.process_request()
        return AnswerModel(answer=response)
    
    except HTTPException as http:
        return JSONResponse(status_code=http.status_code, content={"error": http.detail})
    
    except TimeoutError as e:
        return JSONResponse(status_code=400,content={"error": f"Timeout error {e}"})
    
    except ValueError as e:
        return JSONResponse(status_code=402,content={"error": f"Value error {e}"})
    
    except Exception as e:
        return JSONResponse(status_code=500,content={"error": f"Internal server error {e}"})
    

uvicorn.run(app, host="127.0.0.1", port=8000) if __name__ == "__main__" else None   

