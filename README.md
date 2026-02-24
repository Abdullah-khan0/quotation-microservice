# 📄 Quotation Microservice  
FastAPI-based Quotation Generator with Automated Calculations & Email Draft

---

##  Overview

This project is a **FastAPI microservice** that generates structured quotations from a JSON payload.

It calculates:

- Line totals  
- Grand total  
- Generates a ready-to-send email draft  

All calculations are performed locally.  
Optionally, an external LLM (via GROQ) can be used to enrich the email content.

---

## Architecture

```
Client (POST JSON)
        ↓
FastAPI Endpoint (/quote)
        ↓
Pydantic Validation
        ↓
Business Logic (Calculation Engine)
        ↓
Generate Email Draft
        ↓
Return JSON Response
```

---

##  Features

- ✅ `POST /quote` endpoint
- ✅ Automatic line total calculation
- ✅ Grand total calculation
- ✅ Structured JSON response
- ✅ Email draft generation
- ✅ Fully typed with Pydantic models
- ✅ Swagger UI (`/docs`)
- ✅ ReDoc (`/redoc`)
- ✅ Optional GROQ LLM integration
- ✅ Docker support

---

##  Project Structure

```
quotation-microservice/
│
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic request/response models
│   └── services.py      # Business logic & calculations
│
├── tests/               # (Optional) Unit tests
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── .gitignore
└── README.md
```

---

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- Optional: Groq API
- Docker

---

## Installation & Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/quotation-microservice.git
cd quotation-microservice
```

---

### 2️⃣ Create Virtual Environment

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

If using GROQ:

**Mac/Linux**
```bash
export GROQ_API_KEY="your_groq_api_key"
```

**Windows PowerShell**
```bash
$env:GROQ_API_KEY="your_groq_api_key"
```

You can also create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

---

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

##  API Reference

### 🔹 POST `/quote`

Generates a quotation with calculated totals.

---

### Request Example

```json
{
  "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
  "currency": "SAR",
  "items": [
    {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
    {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
  ],
  "delivery_terms": "DAP Dammam, 4 weeks",
  "notes": "Client asked for spec compliance with Tarsheed."
}
```

---

###  Response Example

```json
{
  "line_items": [
    {
      "sku": "ALR-SL-90W",
      "qty": 120,
      "unit_cost": 240,
      "margin_pct": 22,
      "line_total": 35136
    },
    {
      "sku": "ALR-OBL-12V",
      "qty": 40,
      "unit_cost": 95.5,
      "margin_pct": 18,
      "line_total": 4507.6
    }
  ],
  "grand_total": 39643.6,
  "email_draft": "Dear Gulf Eng.,\n\nPlease find below our quotation in SAR...\n\nBest regards,\nSales Team"
}
```

---

## Calculation Logic

Each line total is calculated as:

```
line_total = unit_cost × qty × (1 + margin_pct / 100)
```

Grand total:

```
grand_total = sum(all line_totals)
```

---

##  Testing via cURL

```bash
curl -X POST "http://127.0.0.1:8000/quote" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
  "currency": "SAR",
  "items": [
    {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22}
  ],
  "delivery_terms": "DAP Dammam, 4 weeks",
  "notes": "Urgent request"
}'
```

---

##  Running with Docker

### 1️⃣ Build Image

```bash
docker build -t quotation-service .
```

---

### 2️⃣ Run Container

```bash
docker run -d \
  -p 8000:8000 \
  -e GROQ_API_KEY="your_groq_api_key" \
  --name quotation-service \
  quotation-service
```

Access:

```
http://localhost:8000/docs
```

---

### Common Docker Commands

| Command | Description |
|----------|-------------|
| `docker ps` | List running containers |
| `docker stop quotation-service` | Stop container |
| `docker rm quotation-service` | Remove container |
| `docker logs quotation-service` | View logs |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | Optional API key for LLM email enhancement |

---

##  Future Improvements

- Add PDF quotation export
- Add authentication (JWT)
- Add database persistence
- Add currency conversion API
- Deploy to AWS / Azure
- Add CI/CD pipeline
- Add automated unit tests

---
