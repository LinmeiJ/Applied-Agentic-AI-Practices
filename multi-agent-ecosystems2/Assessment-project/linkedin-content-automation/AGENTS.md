# AI Coding Agent Instructions (AGENTS.md)

Purpose: provide concise, actionable guidance so AI coding agents can be productive in this repository.

What I am: a brief orientation for agents working on this project.

- **Project root**: this repo contains a FastAPI microservice that implements an AutoGen-style multi-agent LinkedIn content generator. See [README.md](README.md) for full project goals and setup.
- **Entry point**: the FastAPI app is at [app/main.py](app/main.py#L1-L200).
- **Config**: environment-driven settings are in [app/config.py](app/config.py#L1-L200). Load `.env` when running locally.
- **Model client & agents**: check [app/model_client.py](app/model_client.py) and [app/agents/](app/agents/) for agent implementations and client wiring.
- **Service & models**: business logic lives in [app/services.py](app/services.py#L1-L200) and Pydantic models in [app/models.py](app/models.py#L1-L200).
- **Tests**: quick tests and examples live in [test_agent.py](test_agent.py#L1-L200).

Quick commands (run from repository root):

```bash
# create and activate a venv (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
python -m pip install -r requirements.txt

# run the API locally (reload on change)
python -m uvicorn app.main:app --reload

# run tests
pytest -q
```

Agent behavior guidelines (concise):
- **Prefer linking** to existing docs: reference [README.md](README.md) rather than duplicating setup steps.
- **Be minimal**: only make changes that are necessary and small in scope for the user's request.
- **Respect environment variables**: do not embed secrets; use `.env` or CI secrets when running integrations.
- **Run tests**: run `pytest` when code changes are made; if tests fail, report failures and suggest focused fixes.
- **Follow repository style**: keep code changes small and consistent with existing patterns (FastAPI services, Pydantic models, single-responsibility services).

Where to look first for common tasks:
- Implement new API behavior: [app/main.py](app/main.py#L1-L200) -> [app/services.py](app/services.py#L1-L200) -> [app/models.py](app/models.py#L1-L200)
- Add or configure model clients: [app/model_client.py](app/model_client.py#L1-L200) and [app/config.py](app/config.py#L1-L200)
- End-to-end testing / workflow integration: [test_agent.py](test_agent.py#L1-L200) and the README instructions about n8n integration.

If you want me to create or update a different customization file (for example `.github/copilot-instructions.md` or a skill), tell me which file or scope to focus on and I will prepare it.
