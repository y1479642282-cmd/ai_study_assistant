# 🎓 AI Study Assistant Pro

## Project Goals

This project is an intelligent learning assistant system for students. It aims to improve learning efficiency by using text analysis technology to automatically understand learning materials (PDFs), including summaries, Q&A, and exercise generation.

## Team Members

- Jiajie Yan

## Key Features

### 📄 Document Parsing
Supports uploading PDF files and automatically extracts text content for subsequent analysis.
 py -m streamlit run app.py
    
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
├── data/                          # 数据存储目录
│   ├── history.json              # 历史记录
│   └── knowledge_base.json       # 知识库
│
├── utils/                         # 工具模块
│   ├── __init__.py
│   ├── file_handler.py           # 文件处理
│   └── text_processing.py        # 文本处理
│
├── app.py                         # 主程序入口
├── config.py                      # 配置信息
├── qa.py                          # 问答模块
├── quiz.py                        # 测验模块
├── summary.py                     # 总结模块
├── README.md                      # 项目说明文档
├── requirements.txt               # 依赖包列表
└── .venv/                         # 虚拟环境（不建议提交到Git）
## ⚙️ Installation Instructions

1️⃣ Knowledge-Based Question Answering (QA System): Semantic matching based on a knowledge base; uses vectorization and similarity retrieval; returns the most relevant answers.

2️⃣ Text Summarization: Automatically summarizes input text; extracts core information; suitable for note-taking/document compression.

3️⃣ Automatic Quiz Generation: Generates questions based on knowledge content; supports multiple-choice/short-answer questions; used for self-testing and review.

4️⃣ Web UI (Streamlit): Simple and intuitive interface; supports input, querying, and result display; allows for quick deployment of local web applications.
```bash
git clone https://github.com/你的用户名/ai_study_assistant.git
cd ai_study_assistant
pip install -r requirements.txt
pip install streamlit PyPDF2
If pip or python is not available, please use the full path:C:\Users\YourPath\Python39\python.exe -m pip install streamlit PyPDF2
Run in the project root directory
streamlit run app.py   or    C:\Users\YourPath\Python39\python.exe -m streamlit run app.py
Open your browser to access:http://localhost:8501
Username: admin Password: 123456
