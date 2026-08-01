# Phase 1: Build and test the AI microservice
First to build a standalone Python service that can generate LinkedIn content.

Use:
* use FastAPI
* expose a /linkedin API endpoint
* accept brand information and content context
* use an AutoGen-style multi-agent process
* return structured JSON containing:
    * several post ideas
    * one draft
    * a confidence score
    * hashtags
* be tested independently using curl or another HTTP client 

## Architecture
```
User or n8n sends JSON (Note:n8n is not yet involved in phase 1)
          ↓
FastAPI /linkedin endpoint
          ↓
Multi-agent content generation
          ↓
Ideas Agent
          ↓
Drafting Agent
          ↓
Hashtag/Review Agent
          ↓
Structured JSON response
```

Build this section:
```
Request
   ↓
FastAPI
   ↓
AutoGen-style agents
   ↓
JSON response
```

## Phase 1 project structure (draft)
```
linkedin-content-automation/
│
├── main.py
├── agents/
│   ├── idea_agent.py
│   ├── draft_agent.py
│   └── review_agent.py
├── models/
│   └── schemas.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Terminologies:
* FastAPI: astAPI turns your Python code into an HTTP service. This is important because later n8n will call that URL using an HTTP Request node. FastAPI receives this information and passes it to the agents.
   - Instead of calling a Python function like: result =create_linkedin_content(...)
   - Another app can call it through a URL:
   ``` POST http://localhost:8000/linkedin
  - You can think of FastAPI as the doorway between n8n and the - Python agent system:
    ```
    n8n
    ↓ HTTP request
    FastAPI
    ↓ Python function calls
    Agents
    ```
### Agents
#### Ideation Agent
**Responsibility**: Generate several LinkedIn post ideas from the topic and brand information. Example output:
```
[
  "How AI identifies suspicious transactions in real time",
  "Three ways AI improves financial fraud prevention",
  "Why responsible AI matters in fintech security"
]
```

#### Drafting Agent
**Responsibility**: Select or use the strongest idea and write the LinkedIn post. Example:
```
Financial fraud is becoming faster and more sophisticated.

AI-powered detection systems help financial institutions identify unusual patterns in real time...
```
#### Review or Hashtag Agent
**Responsibility**: Review whether the post matches the brand, assign a confidence score, and generate hashtags. Example:
```
{
  "confidence": 0.91,
  "hashtags": [
    "#Fintech",
    "#ArtificialIntelligence",
    "#FraudDetection"
  ]
}
```
### Final API response
The endpoint should combine the agents’ work into one structured response:
```
{
  "ideas": [
    "How AI identifies suspicious transactions in real time",
    "Three ways AI improves financial fraud prevention",
    "Why responsible AI matters in fintech security"
  ],
  "draft": "Financial fraud is becoming faster and more sophisticated...",
  "confidence": 0.91,
  "hashtags": [
    "#Fintech",
    "#ArtificialIntelligence",
    "#FraudDetection"
  ]
}
```
That exact structure is important because n8n will later read fields such as:
```
ideas
draft
confidence
hashtags
```