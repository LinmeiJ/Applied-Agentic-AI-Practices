# AI-Powered LinkedIn Content Automation with n8n and - AutoGen Microservice

## Overview
This project challenges you to design and implement an AI-powered workflow
automation system that streamlines LinkedIn content creation and posting for a fintech
organization. The solution combines an AutoGen-inspired microservice with the n8n
workflow orchestrator. The workflow demonstrates intelligent orchestration across
multiple AI-driven components, including side ideation, drafting, and hashtag
generation, before applying guardrails for approval and publishing. The project highlights
how product leaders can deploy automation to achieve efficiency, brand consistency,
and scale in content strategy.

## Instructions
• Review the lessons and supporting materials on n8n workflows and AutoGen-
style multi-agent design
• Set up the required environment on the Ubuntu VM, including Node.js, n8n, and
the FastAPI microservice
• Follow step-by-step development to:
    - Build the AutoGen-style microservice (/linkedin endpoint)
    - Configure and connect the n8n workflow with Brand Config, AutoGen Microservice, Compose Final, and Approval Gate nodes
    - Implement Slack for dry-run testing and prepare LinkedIn integration for live posting
• Test and debug each component individually (microservice with curl, each n8n
node with Execute Node, and then the full workflow)
• Document the architecture, configuration steps, test runs, and error resolutions
• Submit:
    - Microservice code (main.py, .env.example)
    - Exported n8n workflow JSON
    - Screenshots of successful runs
    - A short reflection on design decisions, challenges, and trade-offs

## Situation
FinEdge Mumbai, a fintech company with over five hundred employees, is facing
significant challenges in its LinkedIn strategy:
• The content team spends 15+ hours per week manually drafting posts.
• Inconsistent posting has reduced engagement by 45%.
• Manual content creation is too slow, causing posts to miss trending topics.
• Executives lack a unified voice, weakening brand authority.
Despite having rich domain expertise, the company struggles to maintain an
authoritative LinkedIn presence. To overcome this, the product team decides to
implement an AutoGen-style multi-agent workflow that generates consistent, on-brand
LinkedIn posts with minimal human effort, while retaining oversight through approval
controls.

## Tasks
• Build a multi-agent microservice that returns multiple post ideas, a draft post with
confidence scoring, and relevant hashtags
• Deploy and test the microservice on your VM, ensuring it accepts brand and context
information via an API and returns structured JSON output
• Configure an n8n workflow with nodes for scheduling, brand configuration,
microservice invocation, composing the final post, approval gate, and routing to
Slack or LinkedIn
• Include mechanisms for logging and error handling to ensure transparency and
traceability

## Actions
To complete this project, you will have to:
• Design and implement the AutoGen-style microservice using FastAPI, exposing
an endpoint that accepts brand configuration and context, then returns JSON
containing ideas, draft, confidence score, and hashtags
• Run and test the microservice locally using curl or HTTP client tools to ensure it
produces the desired output format
• Create a new workflow in the n8n dashboard, with a schedule trigger set to a
suitable cadence for LinkedIn posting
• Add nodes for brand configuration and pass this data to the microservice using
an HTTP Request node with JSON parameters
• Parse the microservice response to assemble the final text and hashtags using a
Set node (no JavaScript required)
• Implement an approval gate that compares the confidence score against a
minimum threshold and checks a dry-run flag to route posts to Slack for review
or LinkedIn for direct publishing
• Configure Slack integration via incoming webhook or OAuth (optional) to send
draft posts for human review
• Add logging by appending run details (for example, timestamp, draft text,
confidence) to a database or spreadsheet to monitor performance and tune
thresholds
• Test the complete flow end-to-end and adjust parameters (for example,
confidence threshold) for optimal balance between automation and oversight


## Result
By the end of this project, you will deliver a working n8n workflow that automates
LinkedIn content generation, a functioning AutoGen-style microservice, a thorough
README detailing setup and run instructions, and documentation summarizing your
design decisions and testing outcomes.

# Technical Detals
## __init__.py
The empty __init__.py tells Python that app is a package.
## Create local python VM
```
python3 -m venv .venv

#activate it
source .venv/bin/activate

#select the environment in vs code using command+shift+p, and search:
Python: Select Interpreter
ensure the interpreter containing: .venv/bin/python

```

## Create project structure 
```
linkedin-content-automation/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

Run commands:
```
mkdir app
touch app/__init__.py
touch app/main.py
touch app/services.py
touch .env.example
touch .gitignore
touch README.md
touch requirements.txt
```

## Add dependencies to requirements.txt
After adding dependencies, then run "python -m pip install -r requirements.txt"
(use 'python -m pip')
verify packages and versions using: 'python -m pip list'

## Run main.py
'python -m uvicorn': Run the Uvicorn web server using the active Python environment.
'app/main.py': find 'app/main.py'
':app": using the object named: 'app = FastAPI(...)'
'--reload': Restart automatically whenever you save a code change.
```
python -m uvicorn app.main:app --reload
```
### kills ports that are in use
```
lsof -i :<port number>
kill -9 <ID>

```

## Open localhost
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs # the swagger page
Note: if n8n runs in a docker container, you need this endpoint in the HTTP request URL: http://host.docker.internal:8000/linkedin and start the app using "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
Run n8n: ```n8n source "<Path to project>/.venv/bin/activate"```
## Add service & model layer
service.py & model.py (test w/ hardcoded messages)

## LLM - Ollama
- run ```ollama serve```: listen tcp 127.0.0.1:11434
- check if it is running: curl http://localhost:11434
- check the llm container: ollama ps

## Configuraiton management (config.py)

### Install pydantic-settings
```
python -m pip install pydantic-settings
```
## Configuration Management (`config.py`)

### Install `pydantic-settings`

```bash
python -m pip install pydantic-settings
```

### Purpose

Centralize application configuration using environment variables.

### Features

- Load configuration from `.env`
- Strongly typed settings
- Cached singleton using `@lru_cache`
- Single source of truth for application configuration

---

## Create Azure OpenAI Client (`model_client.py`)

### Purpose

Create a reusable Azure OpenAI client for all AI agents.

### Design

- Read Azure settings from `config.py`
- Return a configured `AzureOpenAIChatCompletionClient`
- Avoid duplicating client configuration across agents

**Azure Configuration**

- `azure_deployment` = Azure deployment name (e.g. `vt-agi-chat`)
- `model` = underlying model name (e.g. `gpt-5-mini`)

---

## Create Agent Package

Project structure:

```text
app/
│
├── agents/
│   ├── __init__.py
│   ├── idea_agent.py
│   ├── writer_agent.py
│   ├── reviewer_agent.py
│   └── hashtag_agent.py
|.  |__ eva
```

### Design Decision

- One agent per file
- Single Responsibility Principle
- Easier maintenance and future expansion

---

## Implement the First AI Agent

File:

```text
app/agents/idea_agent.py
```

### Purpose

Create an AI agent responsible for generating LinkedIn content ideas.

### Components

- `AssistantAgent`
- `create_model_client()`
- Agent name
- System message (agent role)

### Key Concept

The **system message** defines the agent's permanent role.

Example:

```
You are an experienced LinkedIn content strategist.
```

The **task** changes for every request.

Example:

```
Generate three LinkedIn post ideas about Agentic AI.
```

---

## Test the Agent

Create a temporary test script:

```text
test_agent.py
```

Run:

```bash
python test_agent.py
```

### Purpose

Validate the AI agent independently before integrating it into the FastAPI service.

### Verification

- Azure OpenAI connection works
- Agent returns a response
- Configuration is correct
- Prompt behaves as expected

---

## Improve Test Output

Instead of printing the entire `TaskResult`:

```python
print(result)
```

Print only the AI response:

```python
print(result.messages[-1].content)
```

This produces a clean output containing only the generated LinkedIn ideas.

# Once all agents constructed, here is where we ended up having:
```
                POST /linkedin
                       │
                       ▼
               LinkedInService
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Idea Agent     Writer Agent   Reviewer Agent
        │              │              │
        └──────────────┼──────────────┘
                       ▼
               Hashtag Agent
                       ▼
              LinkedInResponse
```
1. Idea agent: Generates content ideas
2. Write agent: Writes the LinkedIn post
3. Reviewer agent: Improves grammar, tone, and professionalism
4. Hashtag: Generates relevant LinkedIn hashtags



## Debug
### prerequisite:
.vscode/launch.json
### how to enter debug mode
```cmd+shift+d```
### how to start app in debug mode
```press 'F5''```