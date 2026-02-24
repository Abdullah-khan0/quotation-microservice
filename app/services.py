import os
import json
import httpx
from typing import List
from .models import Item, LineItemResponse, QuoteResponse
from .utils import format_currency

# ----------------------------------------------------------------------
# Business logic – calculate totals
# ----------------------------------------------------------------------
def calculate_totals(items: List[Item], currency: str):
    line_items = []
    grand_total = 0.0

    for itm in items:
        line_total = itm.unit_cost * (1 + itm.margin_pct / 100) * itm.qty
        line_total = round(line_total, 2)

        line_items.append(
            LineItemResponse(
                sku=itm.sku,
                qty=itm.qty,
                unit_cost=itm.unit_cost,
                margin_pct=itm.margin_pct,
                line_total=line_total,
            )
        )
        grand_total += line_total

    grand_total = round(grand_total, 2)

    return line_items, grand_total

# ----------------------------------------------------------------------
# LLM wrapper – Groq (fallback to mock)
# ----------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def _call_groq(messages: List[dict], model: str = "mixtral-8x7b-32768"):
    """Direct HTTP call to Groq. Returns the generated text."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 500,
    }
    response = httpx.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()

def _mock_email_draft(request_data: dict) -> str:
    """Very small deterministic mock – used when no API key is present or during tests."""
    client = request_data["client"]
    lang = client["lang"]
    currency = request_data["currency"]
    total = request_data["grand_total"]
    delivery = request_data["delivery_terms"]
    notes = request_data.get("notes", "")

    if lang == "ar":
        tmpl = (
            f"عزيزي {client['name']},\n\n"
            f"نحن سعداء بتقديم عرض الأسعار بالعملة {currency}.\n"
            f"الإجمالي الكلي: {total} {currency}\n"
            f"شروط التسليم: {delivery}\n"
        )
        if notes:
            tmpl += f"ملاحظة: {notes}\n"
        tmpl += "\nمع أطيب التحيات,\nفريق المبيعات"
    else:  # English
        tmpl = (
            f"Dear {client['name']},\n\n"
            f"Please find below our quotation in {currency}.\n"
            f"Grand Total: {total} {currency}\n"
            f"Delivery Terms: {delivery}\n"
        )
        if notes:
            tmpl += f"Notes: {notes}\n"
        tmpl += "\nBest regards,\nSales Team"
    return tmpl

def generate_email_draft(request_json: dict) -> str:
    """
    Returns a short email draft in the language requested (en/ar).
    If GROQ_API_KEY is set, we call the real LLM, otherwise we use a deterministic mock.
    """
    if not GROQ_API_KEY:
        return _mock_email_draft(request_json)

    # Build a concise system+user prompt for the LLM
    system_msg = {
        "role": "system",
        "content": (
            "You are a professional sales engineer. Write a short email (max 200 words) "
            "summarising the quotation. Use the language indicated by the client (en or ar). "
            "Include total amount, delivery terms and any special notes."
        ),
    }

    user_msg = {"role": "user", "content": json.dumps(request_json, ensure_ascii=False)}

    return _call_groq([system_msg, user_msg])