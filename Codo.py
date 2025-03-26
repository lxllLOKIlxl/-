import streamlit as st
import random
from datetime import datetime, timedelta

# Функція для встановлення стилю
def set_background(theme):
    if theme == "Космічний фон":
        st.markdown(
            """
            <style>
                body {
                    background-image: url('https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d');
                    background-size: cover;
                    color: white;
                }
                .stTextInput, .stButton > button {
                    background-color: rgba(0, 0, 0, 0.6);
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                }
                .stTextInput input {
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    elif theme == "Чорний металік":
        st.markdown(
            """
            <style>
                body {
                    background-color: #1a1a1a;
                    color: white;
                }
                .stTextInput, .stButton > button {
                    background-color: #333;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                }
                .stTextInput input {
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    elif theme == "Синій металік":
        st.markdown(
            """
            <style>
                body {
                    background-color: #003366;
                    color: white;
                }
                .stTextInput, .stButton > button {
                    background-color: #00509E;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                }
                .stTextInput input {
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

# Початкова тема
if "theme" not in st.session_state:
    st.session_state["theme"] = "Космічний фон"

# Вибір теми
theme = st.selectbox("🌌 Виберіть фон:", ["Космічний фон", "Чорний металік", "Синій металік"])
if theme != st.session_state["theme"]:
    st.session_state["theme"] = theme

# Встановлення вибраного фону
set_background(st.session_state["theme"])

# Назва гри
st.title("🚀 Кодонавт: Космічна пригода")

# Початкові змінні
if "planet" not in st.session_state:
    st.session_state["planet"] = 1
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 10
if "last_life_restore" not in st.session_state:
    st.session_state["last_life_restore"] = datetime.now()
if "username" not in st.session_state:
    st.session_state["username"] = st.text_input("Введіть ваш нік:", value="Гравець")

# Відновлення життів
if st.session_state["lives"] < 10:
    time_diff = datetime.now() - st.session_state["last_life_restore"]
    if time_diff >= timedelta(minutes=10):
        restore_lives = time_diff.seconds // 600
        st.session_state["lives"] += restore_lives
        st.session_state["lives"] = min(st.session_state["lives"], 10)
        st.session_state["last_life_restore"] = datetime.now()

# Опис поточного стану
st.write(f"🌍 Планета #{st.session_state['planet']}. Ваша мета: набрати 100 очків, щоб перейти на наступний рівень!")
st.write(f"👤 Гравець: {st.session_state['username']}")
st.write(f"💯 Рахунок: {st.session_state['score']}")
st.write(f"❤️ Життя: {st.session_state['lives']} / 10")

# Задача
task = random.choice([
    {"question": "Що таке 2 + 2?", "answer": "4"},
    {"question": "Яка планета третя від Сонця?", "answer": "Земля"},
    {"question": "Який результат: 10 // 3?", "answer": "3"},
    {"question": "Яка найближча зірка до Землі?", "answer": "Сонце"}
])

st.markdown(f"### 🌌 Питання: {task['question']}")
user_answer = st.text_input("Ваша відповідь:", "")

# Кнопка для перевірки
if st.button("Перевірити"):
    if st.session_state["lives"] > 0:
        if user_answer.strip().lower() == task["answer"].lower():
            st.session_state["score"] += 10
            st.success("✅ Правильно! Ви отримали 10 очків.")
        else:
            st.session_state["lives"] -= 1
            st.error("❌ Неправильно! Ви втратили 1 життя.")
    else:
        st.warning("У вас закінчилися життя. Дочекайтесь відновлення, або перезапустіть гру!")

# Перевірка рівня
if st.session_state["score"] >= 100:
    st.session_state["planet"] += 1
    st.session_state["score"] = 0
    st.write("🎉 Ви перейшли на наступну планету!")

# Таймер для відновлення життя
if st.session_state["lives"] < 10:
    next_life_in = timedelta(minutes=10) - (datetime.now() - st.session_state["last_life_restore"])
    minutes, seconds = divmod(next_life_in.seconds, 60)
    st.write(f"⏳ Наступне життя через: {minutes} хв {seconds} с.")

# Вітання при завершенні рівня
if st.session_state["planet"] > 5:
    st.balloons()
    st.write(f"🎉 Вітаємо, {st.session_state['username']}! Ви успішно завершили космічну пригоду!")
