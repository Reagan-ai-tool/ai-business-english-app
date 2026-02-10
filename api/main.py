from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.validation import validate_user_input
from app.prompting import build_business_prompt
from app.client import call_openai_api

app = FastAPI(title="AI Business English API")

class RewriteRequest(BaseModel):
    text: str
    mode: str = "Correct + 3 paragraphs"

@app.post("/rewrite")
def rewrite(req: RewriteRequest):
    ok, cleaned_or_msg = validate_user_input(req.text)
    if not ok:
        raise HTTPException(status_code=400, detail=cleaned_or_msg)

    prompt = build_business_prompt(cleaned_or_msg, req.mode)
    result = call_openai_api(prompt)
    return {"result": result}