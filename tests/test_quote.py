import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

sample_payload = {
    "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
    "currency": "SAR",
    "items": [
        {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
        {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18},
    ],
    "delivery_terms": "DAP Dammam, 4 weeks",
    "notes": "Client asked for spec compliance with Tarsheed.",
}


def expected_line_totals():
    # manual calculation
    line1 = round(240.0 * (1 + 22 / 100) * 120, 2)
    line2 = round(95.5 * (1 + 18 / 100) * 40, 2)
    return line1, line2, round(line1 + line2, 2)


def test_quote_success_mocked_llm():
    """Runs the endpoint with the real code path but patches the LLM call so no external request is made."""
    with patch("app.services.GROQ_API_KEY", None):
        response = client.post("/quote", json=sample_payload)
        assert response.status_code == 200
        data = response.json()

        # --- line items ---
        line1_total, line2_total, grand = expected_line_totals()
        assert data["line_items"][0]["sku"] == "ALR-SL-90W"
        assert data["line_items"][0]["line_total"] == line1_total
        assert data["line_items"][1]["sku"] == "ALR-OBL-12V"
        assert data["line_items"][1]["line_total"] == line2_total

        # --- grand total ---
        assert data["grand_total"] == grand

        # --- email draft ---
        # because we patched the key to None the mock implementation is used
        assert "Dear Gulf Eng." in data["email_draft"]
        assert f"Grand Total: {grand} SAR" in data["email_draft"]
        assert "Delivery Terms: DAP Dammam, 4 weeks" in data["email_draft"]
        assert "spec compliance with Tarsheed" in data["email_draft"]


def test_quote_arabic_email():
    """Same test but client language = ar, ensuring Arabic mock works."""
    payload = sample_payload.copy()
    payload["client"] = payload["client"].copy()
    payload["client"]["lang"] = "ar"

    with patch("app.services.GROQ_API_KEY", None):
        response = client.post("/quote", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "عزيزي Gulf Eng." in data["email_draft"]
        assert "الإجمالي الكلي" in data["email_draft"]