# Create a shared environment
```
python3 -m venv .venv
```
# Active it on MacOS:
```
source .venv/bin/activate
```
# Deactive "(.venv)(base)..." to just "(base)...", run:
```
deactivate
```

<!-- # disabling Anaconda’s automatic activation of the base environment. This is what many Python developers do
```
conda config --set auto_activate_base false
```
# Enable Anaconda's python environment
```
conda activate
``` -->

# What does faq.txt serve?
```
faq.txt is the answer sheet to the most likely technical and architectural questions someone might ask about this project.

faq = Frequently Asked Questions

3 TYPEs of FAQ:
 - Audience 1 — The Developer --> teach other how 
 - Audience 2 — The AI --> knowledge base
 - Audience 3 — Future me -> owner of the code: why choose or design this way
```

# Architecture Concept

```
Business Layer
-------------------------
Security Agent
Cost Agent
User Advocate
Tech Lead

Application Layer
-------------------------
run_agent()
RAG Pipeline
Prompt Logic
Workflow

Infrastructure Layer
-------------------------
LangChain
Azure OpenAI SDK
FAISS
tiktoken
Python

```


# %pip: The % means this is not normal Python;It is a Jupyter Notebook magic command.
# install: Download these libraries and make them available to Python.
# -U: U=upgrade; Upgrade to the latest version of the library if it is already installed.
# langchina-openai: This is the OpenAI integration for LangChain. without it, AzureChatOpenAI and ChatOpenAI will not work.
# langchain-community: This is the community integration for LangChain. It includes tools and utilities contributed by the community. such as FAISS, pdf loaders, Chroma, SQL DB, etc.
# langchain-classic: This is the classic version of LangChain. It includes the original features and functionalities of LangChain before the introduction of the new architecture.
# faiss-cpu: for GPU acceleration; This indicates that the FAISS library is being installed for CPU usage. FAISS is a library for efficient similarity search and clustering of dense vectors. The CPU version is suitable for machines without a GPU.
# tiktoken: It helps count tokens before sending them to the model; This is a library for tokenization, which is the process of converting text into tokens that can be processed by language models. It is used for efficient text processing and model input preparation.

```
%pip install -U langchain langchain-openai langchain-community langchain-classic faiss-cpu tiktoken
```