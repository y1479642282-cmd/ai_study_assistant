import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import Counter
import json
import os
import random
from datetime import datetime

# ===== 自己模块 =====
from utils.docx_reader import read_docx
from config import USE_API

# 如果你还没建 ai_client.py，可以先注释这一行
try:
    from core.ai_client import call_ai
except:
    call_ai = None

# ===== AI模型（本地）=====
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ===== 页面配置 =====
st.set_page_config(page_title="AI Study Assistant Pro", layout="wide")

# ===== 加载模型 =====
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ===== 语言 =====
language = st.sidebar.selectbox(
    "🌍 Language / 语言 / Язык",
    ["中文", "English", "Русский"]
)

def t(cn, en, ru):
    if language == "中文":
        return cn
    elif language == "English":
        return en
    else:
        return ru

# ===== AI开关 =====
use_ai_toggle = st.sidebar.checkbox(
    t("🤖 使用真实AI", "🤖 Use Real AI", "🤖 Использовать ИИ"),
    value=False
)

# ===== 登录状态 =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ===== 登录 =====
def login():
    st.title(t("🔐 登录系统", "🔐 Login System", "🔐 Вход в систему"))

    username = st.text_input(t("用户名", "Username", "Имя пользователя"))
    password = st.text_input(t("密码", "Password", "Пароль"), type="password")

    if st.button(t("登录", "Login", "Войти")):
        if username == "admin" and password == "123456":
            st.session_state.logged_in = True
            st.success(t("登录成功！", "Login successful!", "Вход выполнен успешно"))
        else:
            st.error(t("用户名", "Username", "Имя пользователя"))
t("密码", "Password", "Пароль")

# ===== 工具函数 =====
def split_sentences(text):
    return re.split(r'[.!?\n]', text)

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = ["this", "that", "with", "from", "have", "will", "your", "about"]
    words = [w for w in words if w not in stopwords]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(8)]

# ===== 本地总结 =====
def advanced_summary(text):
    sentences = split_sentences(text)
    sentences = [s.strip() for s in sentences if len(s) > 40]

    return {
        "core": sentences[:2],
        "points": sentences[2:6],
        "conclusion": sentences[6:8]
    }

# ===== 本地问答 =====
def smart_answer(text, question):
    sentences = split_sentences(text)
    sentences = [s.strip() for s in sentences if len(s) > 30]

    if not sentences:
        return t("没有有效内容", "No valid content found", "Нет доступного содержимого")

    sentence_embeddings = model.encode(sentences)
    question_embedding = model.encode([question])

    scores = cosine_similarity(question_embedding, sentence_embeddings)[0]
    best_idx = scores.argmax()

    return sentences[best_idx]

# ===== Quiz =====
def generate_quiz_local(text):
    sentences = split_sentences(text)
    sentences = [s.strip() for s in sentences if len(s) > 40]

    quiz = []

    for i in range(min(3, len(sentences))):
        correct = sentences[i]
        options = random.sample(sentences, min(4, len(sentences)))

        if correct not in options:
            options[0] = correct

        random.shuffle(options)

        quiz.append({
            "question": "Which statement is correct?",
            "options": options,
            "answer": correct
        })

    return quiz

# ===== 历史 =====
def save_history(data):
    file_path = "data/history.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(file_path):
        history = []
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except:
            history = []

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def load_history():
    file_path = "data/history.json"

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

# ===== 主系统 =====
def main_app():
    st.title("🎓 AI Study Assistant Pro")
    st.markdown(t("### 🚀 智能学习平台", "### 🚀 Smart Learning Platform", "### 🚀 Умная учебная платформа"))

    uploaded_file = st.file_uploader(
        t("📂 上传文件（PDF / Word）",
          "📂 Upload File (PDF / Word)",
          "📂 Загрузить файл (PDF / Word)"),
        type=["pdf", "docx"]
    )

    if uploaded_file:
        text = ""

        # ===== 文件识别 =====
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text().replace("\xa0", " ")

        elif uploaded_file.name.endswith(".docx"):
            with open("temp.docx", "wb") as f:
                f.write(uploaded_file.read())
            text = read_docx("temp.docx")
            os.remove("temp.docx")

        # ===== Tabs =====
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            t("📄 内容", "📄 Content", "📄 Содержимое"),
            t("🤖 总结", "🤖 Summary", "🤖 Сводка"),
            t("💬 问答", "💬 Q&A", "💬 Вопрос-ответ"),
            t("📝 练习", "📝 Quiz", "📝 Тест"),
            t("📊 历史", "📊 History", "📊 История")
        ])

        # 内容
        with tab1:
            st.subheader(t("文档预览", "Document Preview", "Предварительный просмотр документа"))
            st.write(text[:2000])

        # 总结
        with tab2:
            if st.button(t("生成总结", "Generate Summary", "Создать сводку")):
                with st.spinner("AI working..."):

                    if (USE_API or use_ai_toggle) and call_ai:
                        prompt = f"请总结以下内容：\n{text[:3000]}"
                        result = call_ai(prompt)
                        st.write(result)
                    else:
                        result = advanced_summary(text)


                        st.markdown("### " + t("核心概述", "Overview", "Обзор"))
                        for s in result["core"]:
                            st.write("- " + s)

                        st.markdown("### " + t("关键要点", "Key Points", "Основные моменты"))
                        for s in result["points"]:
                            st.write("- " + s)

                        st.markdown("### " + t("重要结论", "Conclusion", "Заключение"))
                        for s in result["conclusion"]:
                            st.write("- " + s)

                save_history({"type": "summary", "content": str(result)})

        # 问答
        with tab3:
            question = st.text_input(
                t("请输入问题", "Enter your question", "Введите вопрос")
            )

            if st.button(t("获取答案", "Get Answer", "Получить ответ")):
                with st.spinner("AI thinking..."):

                    if (USE_API or use_ai_toggle) and call_ai:
                        prompt = f"根据以下内容回答问题：\n{text[:3000]}\n\n问题：{question}"
                        answer = call_ai(prompt)
                    else:
                        answer = smart_answer(text, question)

                st.success(t("✅ 完成！", "✅ Done!", "✅ Готово!"))
                st.write(answer)

                save_history({
                    "type": "qa",
                    "question": question,
                    "answer": answer
                })

        # Quiz
        with tab4:
            if st.button(t("生成练习题", "Generate Quiz", "Создать тест")):
                quiz = generate_quiz_local(text)

                for i, q in enumerate(quiz):
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    for opt in q["options"]:
                        st.write(f"- {opt}")
                    st.markdown("---")

        # 历史
        with tab5:
            history = load_history()

            if not history:
                st.info(t("暂无记录", "No history yet", "Нет записей"))
            else:
                for item in history[::-1]:
                    st.write(item)

    else:
        st.info(t("请上传文件", "Please upload a file", "Пожалуйста, загрузите файл"))

# ===== 入口 =====
if not st.session_state.logged_in:
    login()
else:
    main_app()