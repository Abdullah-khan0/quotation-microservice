from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .models import QuoteRequest, QuoteResponse
from .services import calculate_totals, generate_email_draft
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
app = FastAPI(
    title="Quotation Microservice",
    description="Calculate line totals, grand total and generate an email draft (EN/AR).",
    version="1.0.0",
)


@app.post("/quote", response_model=QuoteResponse, summary="Create a quotation")
def create_quote(payload: QuoteRequest):
    # 1️⃣ Calculate totals
    line_items, grand_total = calculate_totals(payload.items, payload.currency)

    # 2️⃣ Prepare data for the LLM (everything the model might need)
    llm_payload = payload.dict()
    llm_payload.update(
        {
            "line_items": [li.dict() for li in line_items],
            "grand_total": grand_total,
        }
    )

    # 3️⃣ Generate email draft (real LLM if key present, else mock)
    try:
        email = generate_email_draft(llm_payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to generate email draft: {exc}",
        ) from exc

    # 4️⃣ Return the response
    resp = QuoteResponse(
        line_items=line_items,
        grand_total=grand_total,
        email_draft=email,
    )
    return JSONResponse(content=resp.dict())