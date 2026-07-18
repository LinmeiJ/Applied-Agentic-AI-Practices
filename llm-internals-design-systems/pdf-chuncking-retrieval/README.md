# RAG Pipeline Using PDF Chunking and Retrieval

## Project Overview

This project demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using LangChain, Azure OpenAI, and FAISS.

The application allows users to ask questions about multiple PDF documents. It retrieves the most relevant document content using semantic search and then uses Azure OpenAI to generate the final answer.

---

## Technologies Used

- Python
- Jupyter Notebook
- LangChain
- Azure OpenAI
- FAISS
- PyPDFLoader
- RecursiveCharacterTextSplitter

---

## Configuration

This project uses environment variables to securely store Azure OpenAI credentials.

Create a `.env` file in the project root with the following information:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

AZURE_OPENAI_CHAT_DEPLOYMENT=your-chat-model-deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-model-deployment
```

Replace the placeholder values with your own Azure OpenAI resource information.

> **Note:** Never share or upload your actual `.env` file because it contains your API credentials.

---

## Dataset

This project uses three AWS Glue reference documents:

- ETL Modernization with AWS Glue.pdf
- AWS Glue Best Practices – Build Efficient Data Pipeline.pdf
- Serverless ETL with AWS Glue.pdf

---

## Project Workflow

The RAG pipeline follows these steps:

1. Load the PDF documents.
2. Clean the extracted text.
3. Split the documents into smaller chunks.
4. Generate embeddings using Azure OpenAI.
5. Store the embeddings in an FAISS vector database.
6. Retrieve the most relevant document chunks based on the user's question.
7. Use Azure OpenAI GPT to generate the final answer.

---

## Project Structure

```text
RAG-PDF-Pipeline/
│
├── main.ipynb
├── README.md
├── analysis_report.md
├── requirements.txt
│
├── data/
│   ├── ETL Modernization with AWS Glue.pdf
│   ├── aws-glue-best-practices-build-efficient-data-pipeline.pdf
│   └── serverless-etl-aws-glue.pdf
│
└── outputs/
    ├── chunk_statistics.png
    ├── query_what_is_aws_glue.png
    ├── query_schedule_glue_jobs.png
    └── query_glue_pros_cons.png
```

---

## How to Run

1. Open `main.ipynb` in Visual Studio Code or Jupyter Notebook.
2. Make sure the `.env` file is configured with your Azure OpenAI credentials.
3. Run the notebook from the first cell to the last cell.
4. The first notebook cell will install the required Python packages if they are not already installed.
5. Run the sample queries or enter your own questions to retrieve information from the uploaded PDF documents.

---

## Sample Questions

Some example questions used for testing:

- What is AWS Glue?
- How do I schedule AWS Glue jobs?
- List the pros and cons of using AWS Glue in general.

Sample outputs are available in the **outputs** folder.

---

## Notes

This project was completed as part of the Agentic AI Bootcamp course-end project. The goal was to gain hands-on experience with building a complete RAG pipeline using LangChain, Azure OpenAI, and FAISS.