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