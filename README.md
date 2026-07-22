# 🚀 SETUP_GUIDE.md

# Complete Student Setup Guide for AI Agentic Track Demos

---
# Why This Matters

This setup exercise is about much more than getting the demos to run. It teaches professional skills you'll use throughout your career as an AI engineer.

| Skill | Why It's Important |
|--------|--------------------|
| Using AI for infrastructure setup | Real-world AI engineers use AI to solve infrastructure and configuration problems. |
| Environment variables | The industry standard for securely managing credentials and secrets. |
| Azure Foundry | One of the most widely used enterprise AI platforms. |
| Refactoring code | Essential for writing secure, maintainable, and reusable software. |
| Troubleshooting with AI | Debugging efficiently with AI is a core engineering skill. |

---
## Why This Setup Guide Exists

### The Problem

Your demo notebooks contain **hardcoded Azure credentials** that were made to run from the Practice Lab Environment (VM) and won't work outside of it. These are placeholders from the course creators that look like this:

```python
os.environ["AZURE_OPENAI_API_KEY"] = "THE_KEY"
azure_endpoint = "https://openai-api-management-gw.azure-api.net"
```

These credentials are only valid in the Practice Lab environment. They will never work outside of the VM.

---

### The Solution

You will:

- Set up your own Azure Foundry resource with real deployments.
- Create a `.env` file with your personal credentials.
- Refactor the notebooks to use your `.env` file instead of hardcoded values.
- 💰 Set up Azure Budget Alerts (Recommended)
- Test everything to ensure it works.

---

## Why We're Doing It This Way

| Traditional Approach | Our Approach |
|----------------------|--------------|
| Static PDF instructions | AI-guided setup with prompts |
| Students get stuck and give up | Students learn to troubleshoot with AI |
| One-size-fits-all | Personalized to each student's environment |
| Outdated quickly | AI adapts to Azure's changing UI |
| Doesn't leverage AI | Uses AI to learn about AI infrastructure |

You're using AI to solve a real infrastructure problem. This is exactly how AI engineers work in the real world.

---

# ⚠️ SECURITY RULE: NEVER PASTE YOUR API KEY

Treat your API key like a password.

### ✅ Do

- Use placeholders like `YOUR_API_KEY_HERE` in prompts.
- Copy your actual API key directly into the `.env` file yourself.

### ❌ Don't

- NEVER paste your real API key into an LLM.
- NEVER share your API key with anyone.
- NEVER commit your `.env` file to GitHub.

---

# 💰 Azure Budget Alerts (Recommended)

## Why Set Up a Budget Alert?

Even though you have free Azure credits, it's a good practice to monitor your spending.

A budget alert will:

- Notify you when your spending approaches a specified amount.
- Give you peace of mind that you won't accidentally exceed your available credits.
- Teach you an important cloud cost-management practice used by professional engineers.

---

## How Much Should You Budget?

For this course, you'll realistically spend **less than $5** using the demo notebooks.

A **$5** or **$10** budget alert provides a safe threshold while giving you plenty of room to complete all course activities.

---

# What You Have

| Item | Location |
|------|----------|
| Demo notebooks | `Demos_updated/Lesson_*/Demo_*` |
| Hardcoded fake credentials | Inside each notebook |
| This setup guide | Root folder (`SETUP_GUIDE.md`) |

---

# What You'll Get

After completing this setup, you'll have:

- ✅ Azure account with credits (or use your existing account)
- ✅ Azure Foundry resource with two deployed models
- ✅ A `.env` file containing your credentials
- ✅ Azure Budget Alerts (email notifications)
- ✅ Refactored notebooks that actually run
- ✅ Confidence using AI to solve infrastructure problems

---

# Prerequisites

Before you start, make sure you have:

- VS Code installed
- Python 3.10 or newer
- A web browser (for Azure Portal)
- Access to an LLM (Claude, ChatGPT, DeepSeek, etc.)

---

# The 6 Prompts

Use these prompts with Claude, ChatGPT, DeepSeek, or any LLM. Follow the instructions in each prompt exactly.

---

# 📌 Prompt 1: Azure Account & Foundry Setup

Copy this into your LLM:

```text
I need to set up Azure for a class. I will NOT paste any API keys into this chat.

Scenario A: I don't have an Azure account yet. Guide me through signing up for a free Azure account with $200 credits.

Scenario B: I already have an Azure account. Guide me through creating an Azure Foundry resource.

Once I have access, guide me through:

1. Creating an Azure Foundry resource
2. Deploying a chat model with deployment name: vt-agi-chat
3. Deploying an embedding model with deployment name: vt-agi-embeddings
4. Finding my API key and endpoint URL

Tell me exactly what to click in the Azure Portal.
```

### What this does

Gets you an Azure account with the necessary resources.

---

# 📌 Prompt 2: Create a `.env` File

Copy this into your LLM:

```text
I need to create a .env file in VS Code for my Azure credentials.

I will NOT paste my actual API key into this chat. I'll use placeholders and fill in the values myself.

My deployment names are:

- Chat: vt-agi-chat
- Embedding: vt-agi-embeddings

Generate a .env file with these variable names (leave values as placeholders):

- AZURE_OPENAI_API_KEY=your-api-key-here
- AZURE_OPENAI_ENDPOINT=your-endpoint-here
- AZURE_OPENAI_CHAT_DEPLOYMENT=vt-agi-chat
- AZURE_OPENAI_EMBEDDING_DEPLOYMENT=vt-agi-embeddings
- AZURE_OPENAI_API_VERSION=2024-02-15-preview

If I have a Tavily key (optional), also include:

- TAVILY_API_KEY=your-tavily-key-here

Tell me:

1. Where to save the .env file (relative to my notebooks)
2. What to name it
3. How to fill in my actual values (I will do this manually)
4. How to verify it's in the right place

My project structure:

- Root folder: [replace with your actual path]
- Notebooks are in: Demos_updated/Lesson_*/Demo_*/
```

### What this does

Creates a template `.env` file that you'll fill with your actual credentials.

> **Important:** After your LLM gives you the `.env` template, open the file in VS Code and paste your actual API key and endpoint (not the placeholders).

---

# 📌 Prompt 3: Refactor Notebook

Copy this into your LLM and attach your notebook file:

```text
I have a Jupyter notebook with hardcoded credentials. I need to refactor specific cells to use my .env file.

I'm using VS Code. Here is my notebook:

[ATTACH YOUR .ipynb FILE]

The cells that need changes are:

- Cell 2 (imports): Add `from dotenv import load_dotenv` and `import os`
- Cell 3 (credentials): Replace hardcoded API key with `os.getenv("AZURE_OPENAI_API_KEY")`
- Cell 5 (embeddings): Replace hardcoded endpoint with `os.getenv("AZURE_OPENAI_ENDPOINT")`
- Cell 6 (LLM): Replace hardcoded endpoint with `os.getenv("AZURE_OPENAI_ENDPOINT")` and deployment name with `os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")`

My .env variables are:

- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_CHAT_DEPLOYMENT=vt-agi-chat
- AZURE_OPENAI_EMBEDDING_DEPLOYMENT=vt-agi-embeddings
- AZURE_OPENAI_API_VERSION

Show me the updated code for each cell. I will NOT paste my actual API key here—just use `os.getenv()` references.

Repeat this process for each demo notebook in the course.
```

### What this does

Refactors your notebook to use environment variables instead of hardcoded credentials.

### How to Attach a Notebook in VS Code

- Right-click the `.ipynb` file in VS Code.
- Select **Copy Path**.
- Or use the file upload feature in your LLM's interface.

---

# 📌 Prompt 4: Test Your Setup

Copy this into your LLM after refactoring:

```text
I've refactored my notebook to use .env variables. I need a test to verify everything works.

My deployment names are:

- Chat: vt-agi-chat
- Embedding: vt-agi-embeddings

Give me a test script I can run in a new VS Code cell that checks:

1. My .env file loads correctly
2. My API key and endpoint are valid (without exposing the key)
3. My deployments exist and are accessible

If the test passes, tell me what success looks like.

If it fails, I'll paste the error for troubleshooting.
```

### What this does

Provides a test script to verify your setup works.
---

---
# 📌 Prompt 5: Set Up an Azure Budget Alert

Copy this into your LLM:

```text
I've set up my Azure Foundry resource. Now I want to set up a budget alert to monitor my spending.

Guide me through:

1. Creating a budget in the Azure portal with a spending limit of $5 or $10
2. Setting up an email alert when I reach 50% and 80% of my budget
3. Verifying that the budget is active

I want to make sure I don't accidentally spend more than my free credits.

Tell me exactly what to click in the Azure portal.
```

### What this does

Creates an Azure Budget with email notifications so you can monitor your cloud spending while completing the course. This is a recommended cloud engineering best practice, even when using free Azure credits.

---

# 📌 Prompt 6: Troubleshooting

Copy this into your LLM when you get an error (**REMOVE any API keys from the error**):

```text
I'm getting this error when running my notebook (I have removed any API keys from this message):

[paste the full error message here, with any API keys removed]

My setup:

- .env file is in the same folder as my notebook
- Deployment names: vt-agi-chat and vt-agi-embeddings
- I'm using VS Code

What does this error mean and how do I fix it?
```

### What this does

Helps you troubleshoot errors without exposing your credentials.

---

# Student Workflow Summary

```text
Step 1
Open VS Code with your project folder
        ↓
Step 2
Copy Prompt 1
Paste into your LLM
Set up Azure & Foundry
        ↓
Step 3
Copy Prompt 2
Paste into your LLM
Create your .env file
        ↓
Step 4
Open the .env file
PASTE YOUR ACTUAL API KEY AND ENDPOINT (manually)
        ↓
Step 5
Copy Prompt 3
Paste into your LLM
ATTACH your notebook
Get the refactored code
        ↓
Step 6
Copy Prompt 4
Paste into your LLM
Test the refactored notebook
        ↓
Step 7
If an error occurs:
Copy Prompt 5
Paste the error (NO API KEY)
Get the fix
        ↓
Step 8
✅ Success!
Repeat Steps 5–7 for each demo notebook
```

---

# What Success Looks Like

After completing this process, you should have:

- ✅ An Azure account with credits (or be using an existing account)
- ✅ A deployed `vt-agi-chat` model
- ✅ A deployed `vt-agi-embeddings` model
- ✅ A `.env` file containing your credentials
- ✅ A notebook that runs without errors
- ✅ Ability to receive LLM usage cost notifications
- ✅ The ability to run **all demos** in the course

---

# Common Errors & Quick Fixes

| Error | Likely Cause | What to Ask Your LLM |
|--------|--------------|----------------------|
| `ModuleNotFoundError: No module named 'dotenv'` | `python-dotenv` is not installed | "How do I install `python-dotenv` in VS Code?" |
| `404 Resource not found` | Wrong endpoint or deployment name | "My Azure endpoint is giving a 404. What's the correct format?" |
| `403 Permission denied` | Invalid API key | "My API key isn't working. How do I generate a new one?" |
| `NameError: name 'AZURE_OPENAI_API_KEY' is not defined` | `.env` file isn't loading | "My `.env` file isn't loading. How do I fix this in VS Code?" |
| `Connection error` | Network or firewall issue | "Why can't my code connect to Azure?" |
| `RuntimeError: Agent execution was invoked synchronously from within a running event loop` | Jupyter async issue | "How do I fix the CrewAI event loop error in Jupyter?" |
| `APIConnectionError` | Wrong endpoint or network issue | "My Azure connection is failing. What should I check?" |
| `NotFoundError: Error code: 404 - Resource not found` | Deployment doesn't exist or deployment name is incorrect | "My deployment `vt-agi-chat` isn't found. How do I verify my deployments?" |

---

# Your `.env` File Template

Your `.env` file should look like this (using placeholders):

```env
# Azure Foundry Credentials

AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=your-endpoint-here
AZURE_OPENAI_CHAT_DEPLOYMENT=vt-agi-chat
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=vt-agi-embeddings
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Tavily (Optional)

TAVILY_API_KEY=your-tavily-key-here
```

> **Remember:** Replace the placeholder values with your actual credentials. Never share this file or commit it to GitHub.

---

# 🔑 Remember

- **NEVER** paste your API key into an LLM.
- Use placeholders in prompts.
- Paste your real API key **only** into your local `.env` file.

---

# Questions?

If you get stuck:

1. **First:** Use **Prompt 5** with your preferred LLM.
2. **Second:** Check the **Common Errors & Quick Fixes** table above.
3. **Third:** Post in the class discussion forum (without including your API key).

---
# 🔑 Key Takeaway for Students

## The magic formula for Azure Foundry:

# 1. Correct endpoint (no /openai/v1)
AZURE_ENDPOINT = "https://optimops.services.ai.azure.com"

# 2. Correct API version
api_version="2025-03-01-preview"

# 3. Custom class to handle Responses API
# (Share the ResponsesAPIChat class from above)

# 4. .env file for credentials
AZURE_OPENAI_API_KEY=your-actual-key
---
