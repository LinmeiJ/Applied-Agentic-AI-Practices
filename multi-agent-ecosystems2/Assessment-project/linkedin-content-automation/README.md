# AI-Powered LinkedIn Content Automation with n8n and AutoGen Microservice

## Overview
This project implements an AI-powered workflow automation system that streamlines LinkedIn content creation for fintech organizations. The solution combines an AutoGen-inspired multi-agent microservice with n8n workflow orchestration.

**Key Features:**
- 🤖 5 specialized AI agents (Idea, Writer, Reviewer, Evaluator, Hashtag)
- 🔄 Revision workflow with human feedback
- 📊 Confidence scoring with 10-criteria weighted rubric
- 🚦 Bias/judgment gate for content safety
- ☁️ Support for both local (Ollama) and cloud (Azure OpenAI) models
- 📋 n8n workflow with approval gates and Slack integration
- 📝 Google Sheets logging for transparency



# Poject Structure 
## Folder Structure
linkedin-agent/
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py                    # FastAPI endpoints
│   ├── models.py                  # Request/Response models
│   ├── services.py                # Business orchestration
│   ├── model_client.py            # Creates Azure/OpenAI model clients
│   ├── enums.py                   # ModelType enum
│   │
│   └── agents/
│       ├── __init__.py
│       ├── idea_agent.py
│       ├── writer_agent.py
│       ├── reviewer_agent.py
│       ├── hashtag_agent.py
│       └── evaluator_agent.py   
│
├── requirements.txt
├── README.md
└── .env


## Setup Instructions

### 1. Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Microservice runtime |
| Ollama | Latest | Local LLM for development |
| n8n | Latest | Workflow orchestration |
| Docker | Latest | For n8n container (optional) |

### 2. Clone and Setup Python Environment
``` 
# Clone the repository
git clone <your-repo-url>
cd linkedin-content-automation

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On macOS/Linux
# or .venv\Scripts\activate  # On Windows

# Select the environment in VS Code using Cmd+Shift+P, search:
# Python: Select Interpreter
# Ensure the interpreter contains: .venv/bin/python

# Install dependencies
python -m pip install -r requirements.txt

# Verify packages
python -m pip list
```

# Environment Configuration
```
# Copy example env file
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
# If using Ollama locally, no additional config needed
```

# Install and Run Ollama
```
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

#Which model is running on
curl http://localhost:11434/api/tags

# Pull the model (choose one)
ollama pull deepseek-r1:14b  # Recommended for quality
# OR
ollama pull qwen3:8b         # Lighter, faster

# Start Ollama server
ollama serve

# Check if running
lsof -i :11434
```
## Useful Ollama Commands:
```
# Check running models
ollama ps

# Stop ollama by port
lsof -ti :11434 | xargs kill -9

# Kill all ollama processes
sudo killall -9 ollama

# Check service status (macOS)
launchctl list | grep ollama
```
# Run the Microservice
```
# From project root, with venv activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access the API
# Swagger UI: http://localhost:8000/docs
# Health check: http://localhost:8000/health
# Config test: http://localhost:8000/config
```
## If running with n8n in Docker:
```
# Use host.docker.internal in n8n HTTP requests
# URL: http://host.docker.internal:8000/linkedin

# Start app with host 0.0.0.0 to accept external connections
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## Kill port 8000 if in use:
```
lsof -ti :8000 | xargs kill -9
```

# Test the API
```
curl -X POST http://localhost:8000/linkedin \
  -H "Content-Type: application/json" \
  -d '{
    "brand": {
      "company_name": "FinEdge Mumbai",
      "industry": "Fintech",
      "brand_voice": "professional and informative",
      "target_audience": "Financial professionals and executives"
    },
    "context": {
      "topic": "AI in Financial Planning",
      "goal": "Educate and engage the audience",
      "key_points": [
        "AI improves financial planning accuracy",
        "Saves time and reduces human error",
        "Enables real-time decision making"
      ]
    },
    "automation": {
      "minimum_confidence": 0.85,
      "dry_run": true
    }
  }'
  ```
####  Using VS Code Debugger:
```
.vscode/launch.json is configured
# Press Cmd+Shift+D to open debug view
# Press F5 to start debugging
```
expected response:
 ```
 {
  "ideas": [
    "1. AI is transforming fintech...",
    "2. The future of financial planning...",
    "3. Why data-driven decisions win..."
  ],
  "draft": "Exciting developments in AI...",
  "confidence": 0.87,
  "confidence_reason": "grammar_readability (0.95): Clean writing...",
  "minimum_confidence": 0.85,
  "dry_run": true,
  "hashtags": ["#Fintech", "#AI", "#FinancialPlanning"],
  "status": "AI_GENERATED",
  "company": "FinEdge Mumbai",
  "goal": "Educate and engage the audience",
  "topic": "AI in Financial Planning",
  "audience": "Financial professionals and executives",
  "revision_number": 0,
  "decision": null,
  "reject_reason": null
}
 ```   

# Set Up n8n
##  Run n8n with Docker:
```
open -a Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
  ```
  Access n8n: http://localhost:5678

#  Import and Configure n8n Workflow
1. Open n8n dashboard
2. Click "Import from File"
3. Select linkedin-workflow.json
4. Configure the following nodes:
    Brand Config Node: Set your company details
    ```
    {
  "company_name": "FinEdge Mumbai",
  "industry": "Fintech",
  "brand_voice": "professional and informative",
  "target_audience": "Financial professionals and executives"
    }
    ```
    HTTP Request Node: Point to your microservice
    ```
    Method: POST
    URL: http://host.docker.internal:8000/linkedin (if using Docker)
    URL: http://localhost:8000/linkedin (if local)
     ```
    Slack Node: Configure webhook URL:
    - Channel: #linkedin-reviews
    - Credentials: Add Slack OAuth or webhook

    Google Sheets Node: Configure logging
    - Spreadsheet ID: Your sheet ID
    - Sheet Name: "LinkedIn Activity Log"

# Workflow Architecture
```
Schedule Trigger (Daily/Weekly)
        │
        ▼
    Brand Config
        │
        ▼
Generate LinkedIn Content (HTTP POST to /linkedin)
        │
        ▼
   Compose Final (Assemble post + hashtags)
        │
        ▼
   Approval Gate (Compare confidence vs threshold)
        │
        ├─── If confidence >= threshold ────► LinkedIn Post (Auto-publish)
        │
        └─── If confidence < threshold ─────► Slack Human Review
                                                 │
                                                 ├─── Approve ──► LinkedIn Post
                                                 ├─── Revise ───► Create Revision Payload
                                                 │                    │
                                                 │                    ▼
                                                 │              Revise LinkedIn Content
                                                 │                    │
                                                 │                    ▼
                                                 │              Revision Log (Sheet)
                                                 │
                                                 └─── Reject ────► Rejection Log (Sheet)
```

# Agent Architecture
Agent	           Model	               Purpose
Idea Agent	       Ollama (Local)	     Generates 3-5 creative post ideas
Writer Agent	    Ollama (Local)	     Writes the draft post
Reviewer Agent	    Ollama (Local)	     Polishes and improves content
Evaluator Agent	Azure    OpenAI	          Scores quality with 10-criteria rubric
Hashtag Agent	         Ollama (Local)	    Generates 4-6 relevant hashtags

## Evaluator Rubric (10 Criteria):
1. grammar_readability (6%)
2. clarity (8%)
3. brand_voice_alignment (12%)
4. audience_alignment (11%)
5. key_point_coverage (14%)
6. engagement_potential (10%)
7. accessibility_and_relatability (10%)
8. visual_scannability (8%)
9. topic_relevance (7%)
10. leadership_tone_appropriateness (14%)

Bias Gate: Hard override - if bias detected → confidence = 0.0

# Logging
## Google Sheets logs:
- LinkedIn Post Activity Log: All generated posts
- Revision Log: Revision history with feedback
- Rejection Log: Rejected posts with reasons

## Log Entries Include:
- Timestamp
- Draft text
- Confidence score
- Decision (approve/reject/revise)
- Company name
- Topic
- Revision number

# Error Handling
Component	                   Error Handling Strategy
FastAPI Service	           Try/except wrappers, fallback responses, retry logic
Agents	               Retry up to 3 times, graceful degradation
n8n HTTP	           120s timeout, validation node
n8n Workflow	       Error handler node, Slack alerts

# Troubleshooting
"Agent not responding" / "Model not found"
```
# Check Ollama is running
ollama ps
ollama serve

# Pull the model if missing
ollama pull deepseek-r1:14b
```

"Connection refused" when calling API from n8n"
```
# Check FastAPI is running with host 0.0.0.0
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# In n8n, use host.docker.internal if n8n is in Docker
http://host.docker.internal:8000/linkedin
```
"API Key missing" error
```
# Check .env file exists and has all required keys
cat .env
```
"Port 8000 already in use"
```
lsof -ti :8000 | xargs kill -9
```
"Evaluator returns 0.0 confidence"
```
# Check Azure OpenAI credentials in .env
# Verify the model deployment exists
# Check the evaluator is using ModelType.CLOUD (Azure)
```

# Development Commands Reference
```
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Run FastAPI with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run n8n (from venv)
n8n

# Kill port 8000
lsof -ti :8000 | xargs kill -9

# Check Python packages
python -m pip list

# VS Code Debug: Press F5
```





