# Quotation Microservice

A **FastAPI** microservice that generates quotations, calculates line totals & grand total, and returns a ready‑to‑send email draft. All calculations are performed locally; an optional external LLM (via GROQ) can be used to enrich the email text.

---

## Table of Contents

- [Features](#features)  
- [Project Structure](#project-structure)  
- [Prerequisites](#prerequisites)  
- [Installation & Local Run](#installation--local-run)  
- [Running with Docker](#running-with-docker)  
- [Environment Variables](#environment-variables)  
- [API Reference](#api-reference)  
- [Sample Requests](#sample-requests)  
- [Testing](#testing)  


---

## Features

- **POST** `/quote` – Accepts a JSON payload with client, items, currency, delivery terms & notes.  
- Calculates **line totals** (`unit_cost × qty × (1 + margin_pct/100)`).  
- Returns **grand total** and a **ready‑to‑send email draft**.  
- Fully typed with **Pydantic** models.  
- Interactive API docs via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`).  
- Optional integration with GROQ (or any LLM) for richer email content.

---

## Project Structure
quotation_service/
├── app/
│ ├── main.py # FastAPI app
│ ├── models.py # Pydantic models for request & response
│ └── services.py # Business logic for quotation calculation
├── .venv/ # Python virtual environment (not included in repo)
├── requirements.txt # Python dependencies
└── README.md



All source code lives under the `app/` package; tests are kept in `tests/`.

---

## Prerequisites

| Tool | Minimum Version | Why you need it |
|------|----------------|-----------------|
| Python | **3.10** | Language runtime |
| pip | latest | Dependency manager |
| Docker (optional) | 20.10+ | Containerisation |
| git | any | Source control |

> **Tip:** If you use VS Code, the **Python** extension will automatically detect the virtual‑env and give you IntelliSense for the FastAPI project.

---

## Installation & Local Run

```bash
# 1️⃣ Clone the repo
git clone https://github.com/<YOUR_USERNAME>/quotation-microservice.git
cd quotation-microservice

# 2️⃣ Create & activate a virtual environment
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3️⃣ Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4️⃣ Set required environment variables
# macOS / Linux
export GROQ_API_KEY="your_groq_api_key"

# Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key"

# 5️⃣ Run the API
uvicorn app.main:app --reload   # --reload enables hot‑reloading while developing


Open your browser at http://127.0.0.1:8000/docs to view the interactive Swagger UI.



## Running with Docker
Docker isolates the whole runtime (Python, dependencies, env‑vars) into a single, reproducible image.

1️⃣ Build the image
docker build -t quotation-service .

2️⃣ Run the container
docker run -d \
  -p 8000:8000 \
  -e GROQ_API_KEY="your_groq_api_key" \
  --name quotation-service \
  quotation-service
---
The API will now be reachable at http://localhost:8000/docs.
---
Common Docker commands
Command	Description
docker ps

List running containers
docker stop quotation-service

Stop the container
docker rm quotation-service

Remove the stopped container
docker logs quotation-service

View container logs
docker run -p 9000:8000 …

Map container port 8000 to host port 9000 if 8000 is busy




API Documentation

POST /quote - Generate quotation

Request Body Example:
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

Response Example:
{
  "line_items": [
    {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240, "margin_pct": 22, "line_total": 35136},
    {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18, "line_total": 4507.6}
  ],
  "grand_total": 39643.6,
  "email_draft": "Dear Gulf Eng.,\n\nPlease find below our quotation in SAR...\nBest regards,\nSales Team"
}

Sample Curl Request
curl -X POST "http://127.0.0.1:8000/quote" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
  "currency": "SAR",
  "items": [
    {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
    {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
  ],
  "delivery_terms": "DAP Dammam, 4 weeks",
  "notes": "Client asked for spec compliance with Tarsheed."
}'


Environment Variables

GROQ_API_KEY → API key used for any external service integration (if required)

Store in .env file or pass via Docker -e flag


## How the Microservice Works

Below is a simple flow of how the quotation microservice works:
      +-------------------+
      |   Client System   |
      | (sends POST JSON) |
      +---------+---------+
                |
                v
      +-------------------+
      |    FastAPI App    |
      |  (app/main.py)    |
      +---------+---------+
                |
     Validate & parse JSON
                |
                v
      +-------------------+
      | Business Logic    |
      | (services.py)     |
      | - Calculate line  |
      |   totals          |
      | - Calculate grand |
      |   total           |
      +---------+---------+
                |
                v
      +-------------------+
      | Generate Response |
      | (email draft +    |
      |  totals)          |
      +---------+---------+
                |
                v
      +-------------------+
      |  Response JSON    |
      |  Sent back to     |
      |  Client           |
      +-------------------+



##Testing

Local testing via Swagger UI: http://127.0.0.1:8000/docs

Automated tests (if you add tests/):

