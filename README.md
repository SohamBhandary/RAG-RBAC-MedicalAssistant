# 🏥 Secure RAG-Powered Medical Chatbot with Role-Based Access Control

A **production-style, full-stack Medical Chatbot** built using a **Retrieval-Augmented Generation (RAG)** pipeline with **role-based access control (RBAC)**.  
The system delivers **document-grounded medical answers** tailored to different user roles such as **Doctor, Nurse, Patient, and Others**, with a strong focus on **security, modular backend design, and GenAI workflows**.

---

## 🧠 What This Project Solves

- Prevents hallucinations by grounding responses in uploaded medical documents
- Enforces **role-based access** to sensitive medical knowledge
- Enables secure, scalable GenAI-powered QnA systems for real-world use cases

---

## 🧠 System Architecture

The application follows a **modular, AI-first backend architecture**:

- 🌐 **FastAPI backend** exposing secure APIs
- 🧠 **Groq LLM (LLaMA 3)** for natural language generation
- 📦 **Pinecone** for semantic vector search
- 📄 **Google AI Embeddings** for document vectorization
- 🗄️ **MongoDB Atlas** for user persistence & RBAC
- 🎛️ **Streamlit frontend** for interactive chat UI

> Queries are filtered by **user role** before retrieval and generation.

---

## 🚀 Core Features

### 🔐 Authentication & RBAC
- Secure signup & login
- Password hashing using **Bcrypt**
- Role-based access control:
  - **Admin** – document upload & management
  - **Doctor / Nurse / Patient / Others** – role-specific QnA access

---

### 🧠 RAG Pipeline
- Document ingestion & embedding
- Vector storage using **Pinecone**
- Semantic retrieval using **Google AI Embeddings**
- Context-aware answer generation with **LLaMA 3 (Groq)**

---

### 📄 Document Management
- Admin-only document upload
- Secure document indexing
- Role-aware query filtering

---

### 🎛️ Frontend
- Streamlit-based chat interface
- Role-aware user experience
- Real-time medical QnA interaction

---

## 🛠 Tech Stack

### Backend & AI
- FastAPI
- Groq LLM (LLaMA 3)
- Pinecone
- Google AI Embeddings
- LangChain-style RAG pipeline

### Database & Security
- MongoDB Atlas
- Bcrypt (Password hashing)
- Role-Based Access Control (RBAC)

### Frontend
- Streamlit

---

## 🧩 Backend Design Highlights

- Modular FastAPI routing
- Clean separation of concerns:
  - Auth
  - Document ingestion
  - Retrieval pipeline
  - Chat generation
- Role-based query filtering before inference
- Scalable GenAI-ready architecture
---

## 🎯 Project Focus

This project is intentionally **backend & AI-heavy**, emphasizing:
- Secure role-based access
- Reliable document-grounded GenAI responses
- Real-world RAG architecture
- Scalable and modular backend design

