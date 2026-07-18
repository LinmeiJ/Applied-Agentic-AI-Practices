# Analysis Report

## Introduction

This project demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using LangChain, Azure OpenAI, and FAISS. The application retrieves relevant information from multiple PDF documents and generates answers based on the retrieved content.

The goal of this project is to understand how document chunking, embeddings, vector search, and large language models work together to improve question-answering over custom documents.

---

## Implementation Overview

This project uses three AWS Glue PDF documents as the knowledge base.

The implementation follows these steps:

1. Load the PDF documents using PyPDFLoader.
2. Clean the extracted text by removing empty or very short pages.
3. Split the documents into smaller chunks using RecursiveCharacterTextSplitter.
4. Generate vector embeddings for each chunk using Azure OpenAI Embeddings.
5. Store the embeddings in an FAISS vector database.
6. Retrieve the top three most relevant document chunks (`k=3`) based on the user's question.
7. Use Azure OpenAI GPT to generate the final answer from the retrieved document content.

This workflow allows the application to answer questions using information from the uploaded documents instead of relying only on the language model's general knowledge.

---

## Metrics

The final document processing results are:

- Pages before cleaning: **83**
- Pages after cleaning: **81**
- Total chunks: **157**
- Average chunk size: **724.93 characters**
- Retrieved chunks per query: **3 (k=3)**

The application was tested with several sample questions, including:

- What is AWS Glue?
- How do I schedule AWS Glue jobs?
- List the pros and cons of using AWS Glue in general.

The results showed that the retriever successfully identified relevant document chunks and the language model generated accurate answers based on the retrieved content.

---

## Conclusion

This project helped me understand how a complete RAG pipeline works from end to end. I learned how document chunking improves retrieval, how embedding models convert document chunks into vector representations, and how FAISS performs semantic search to retrieve relevant information. I also learned how a large language model uses the retrieved document content to generate accurate answers.

In the future, I would like to improve this project by experimenting with different chunk sizes, adding more documents, and building a simple web interface so users can interact with the RAG application more easily.