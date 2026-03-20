# 🎓 AI Study Assistant Pro

## Project Goals

This project is an intelligent learning assistant system for students. It aims to improve learning efficiency by using text analysis technology to automatically understand learning materials (PDFs), including summaries, Q&A, and exercise generation.

## Team Members

- Jiajie Yan

## Key Features

### 📄 Document Parsing
Supports uploading PDF files and automatically extracts text content for subsequent analysis.

### Intelligent Summary
Automatically generates:

- Core Overview

- Key Points

- Conclusion

### Intelligent Q&A
Extracts the most relevant answers from the document using keyword matching and sentence scoring mechanisms, achieving AI-like Q&A functionality.

### Automatic Exercise Generation
Automatically generates multiple-choice questions based on document content to help users consolidate their knowledge.

### History
Automatically saves user summaries and Q&A records for later viewing and review.

### Multilingual Support
The system supports switching between Chinese and English interfaces and has international expansion capabilities.

### Login System
Provides basic user authentication functions to enhance system integrity.

## Technology Stack

- Frontend / UI: Streamlit

- Backend Logic: Python

- Document Processing: PyPDF2

- Text Analysis: Regular Expressions (Regex) + Keyword Statistics

- Data Storage: JSON (Local Storage)

## Project Structure
ai_study_assistant/

│
├── app.py # Main program (Streamlit application)

├── data/

│ └── history.json # Historical data

└── README.md # Project documentation
---

## ⚙️ Installation Instructions

```bash
pip install streamlit PyPDF2
If pip or python is not available, please use the full path:C:\Users\YourPath\Python39\python.exe -m pip install streamlit PyPDF2
Run in the project root directory
streamlit run app.py   or    C:\Users\YourPath\Python39\python.exe -m streamlit run app.py
Open your browser to access:http://localhost:8501
Username: admin Password: 123456
