import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import Counter
import json
import os
import random
from datetime import datetime
from summary import summarize_textgit status
from qa import answer_question
from quiz import generate_quiz

# ✅ AI模型（核心升级）
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ===== 页面配置 =====
st.set_page_config(page_title="AI Study Assistant Pro", layout="wide")

# ===== 加载模型（只加载一次）=====
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ===== 语言 =====
language = st.sidebar.selectbox("🌍 Language / 语言", ["中文", "English"])

def t(cn, en):
    return cn if language == "中文" else en

# ===== 登录状态 =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ===== 登录 =====
def login():
    st.title(t("🔐 登录系统", "🔐 Login System"))

    username = st.text_input(t("用户名", "Username"))
    password = st.text_input(t("密码", "Password"), type="password")

    if st.button(t("登录", "Login")):
        if username == "admin" and password == "123456":
            st.session_state.logged_in = True
            st.success(t("登录成功！", "Login successful!"))
        else:
            st.error(t("用户名或密码错误", "Invalid username or password"))

# ===== 工具函数 =====
def split_sentences(text):
    return re.split(r'[.!?\n]', text)

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = ["this", "that", "with", "from", "have", "will", "your", "about"]
    words = [w for w in words if w not in stopwords]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(8)]

# ===== 总结 =====
def advanced_summary(text):
    sentences = split_sentences(text)
    sentences = [s.strip() for s in sentences if len(s) > 40]

    return {
        "core": sentences[:2],
        "points": sentences[2:6],
        "conclusion": sentences[6:8]
    }

# ===== AI问答（升级版🔥）=====
def smart_answer(text, question):
    sentences = split_sentences(text)
    sentences = [s.strip() for s in sentences if len(s) > 30]

    if not sentences:
        return t("没有有效内容", "No valid content found")

    sentence_embeddings = model.encode(sentences)
    question_embedding = model.encode([question])

    scores = cosine_similarity(question_embedding, sentence_embeddings)[0]
    best_idx = scores.argmax()

    return sentences[best_idx]

# ===== Quiz =====
def generate_quiz(text):
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

    # ✅ 如果文件坏了，自动修复
    if not os.path.exists(file_path):
        history = []
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []  # 文件坏了就重置

    from datetime import datetime
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
            if isinstance(data, list):
                return data
            else:
                return []
    except:
        return []

# ===== 主系统 =====
def main_app():
    st.title("🎓 AI Study Assistant Pro")
    st.markdown(t("### 🚀 智能学习平台", "### 🚀 Smart Learning Platform"))

    uploaded_file = st.file_uploader(
        t("📂 上传PDF文件", "📂 Upload PDF"), type=["pdf"]
    )

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text().replace("\xa0", " ")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            t("📄 内容", "📄 Content"),
            t("🤖 总结", "🤖 Summary"),
            t("💬 问答", "💬 Q&A"),
            t("📝 练习", "📝 Quiz"),
            t("📊 历史", "📊 History")
        ])

        # 内容
        with tab1:
            st.subheader(t("文档预览", "Document Preview"))
            st.write(text[:2000])

        # 总结
        with tab2:
            if st.button(t("生成总结", "Generate Summary")):
                with st.spinner(t("AI正在总结...", "AI is summarizing...")):
                    result = advanced_summary(text)

                st.success("✅ Done!")

                st.markdown(t("### 核心概述", "### Overview"))
                for s in result["core"]:
                    st.write(f"- {s}")

                st.markdown(t("### 关键要点", "### Key Points"))
                for s in result["points"]:
                    st.write(f"- {s}")

                st.markdown(t("### 重要结论", "### Conclusion"))
                for s in result["conclusion"]:
                    st.write(f"- {s}")

                save_history({"type": "summary", "content": result})

        # 问答
        with tab3:
            question = st.text_input(t("请输入问题", "Enter your question"))

            if st.button(t("获取答案", "Get Answer")):
                with st.spinner("AI thinking..."):
                    answer = smart_answer(text, question)

                st.success("✅ Done!")
                st.write("📌 Answer:")
                st.write(answer)

                save_history({
                    "type": "qa",
                    "question": question,
                    "answer": answer
                })

        # Quiz
        with tab4:
            st.subheader(t("📝 智能练习", "📝 Smart Quiz"))

            if st.button(t("生成练习题", "Generate Quiz")):
                quiz = generate_quiz(text)

                for i, q in enumerate(quiz):
                    st.markdown(f"**Q{i+1}: {q['question']}**")

                    for opt in q["options"]:
                        st.write(f"- {opt}")

                    st.markdown("---")

        # 历史
        with tab5:
            history = load_history()

            if not history:
                st.info(t("暂无记录", "No history yet"))
            else:
                for item in history[::-1]:
                    st.write(item)

    else:
        st.info(t("请上传PDF文件", "Please upload a PDF file"))

# ===== 入口 =====
if not st.session_state.logged_in:
    login()
else:
    main_app()