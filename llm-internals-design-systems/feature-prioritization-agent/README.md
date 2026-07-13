#architecture
```
Product Manager prompt
        │
        ▼
GPT-5 Mini with bound tools
        │
        ▼
Custom run_agent() orchestration loop
        │
        ├── UserAdvocate(feature)
        ├── TechLead(feature)
        └── BusinessAnalyst(feature)
        │
        ▼
ToolMessage results returned to GPT-5 Mini
        │
        ▼
GPT-5 Mini aggregates totals/averages
        │
        ▼
Prioritized feature list

Note: the assignment calls the 3 specilist components "agents", but technically speaking they are just simple deterministic python tools in this assigment. GPT-5-mini is the only LLM in this version.

```
# Start to build
## Install Dependencies from requirements.txt
```
python -m pip install -r requirements.txt
```


# Define the three scoring functions

