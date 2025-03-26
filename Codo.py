import streamlit as st
import random
from datetime import datetime, timedelta

# Назва гри
st.title("🚀 Кодонавт: Космічна пригода")

# Лівий стовпець для гри, правий для інформації про гравця
col1, col2 = st.columns([3, 1])

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
    st.session_state["username"] = ""

# Введення ніку гравця (правий блок)
with col2:
    if st.session_state["username"] == "":
        st.session_state["username"] = st.text_input("👤 Введіть ваш нік:", value="Гравець")

# Оновлення життів кожні 10 хвилин
if st.session_state["lives"] < 10:
    time_diff = datetime.now() - st.session_state["last_life_restore"]
    if time_diff >= timedelta(minutes=10):
        restore_lives = time_diff.seconds // 600
        st.session_state["lives"] += restore_lives
        st.session_state["lives"] = min(st.session_state["lives"], 10)
        st.session_state["last_life_restore"] = datetime.now()

# Інформація про гравця (правий блок)
with col2:
    st.markdown("### 👤 Інформація про гравця:")
    st.markdown(f"**Ім'я:** {st.session_state['username']}")
    st.markdown(f"**❤️ Життя:** {st.session_state['lives']} / 10")
    st.markdown(f"**💯 Рахунок:** {st.session_state['score']}")
    st.markdown(f"**🌍 Планета:** {st.session_state['planet']}")

# Вибір питання для рівня (лівий блок)
questions = {
    1: [
        {"question": "Що таке 2 + 2?", "answer": "4"},
        {"question": "Яка планета третя від Сонця?", "answer": "Земля"},
        {"question": "Який результат: 10 // 3?", "answer": "3"},
        {"question": "Яка найближча зірка до Землі?", "answer": "Сонце"},
        {"question": "Яке число йде після 5?", "answer": "6"},
        {"question": "Столиця України?", "answer": "Київ"},
        {"question": "Скільки днів у лютому у високосний рік?", "answer": "29"},
        {"question": "Який колір має небо?", "answer": "Синій"},
        {"question": "Скільки буде 5 * 5?", "answer": "25"},
        {"question": "Який океан найбільший?", "answer": "Тихий"}
    ],
    2: [
        {"question": "Скільки планет у Сонячній системі?", "answer": "8"},
        {"question": "Що таке 9 * 9?", "answer": "81"},
        {"question": "Яка планета найближче до Сонця?", "answer": "Меркурій"},
        # Додайте ще 17 питань
    ],
    3: [
        {"question": "Що таке 12 * 12?", "answer": "144"},
        {"question": "Який супутник обертається навколо Землі?", "answer": "Місяць"},
        # Додайте ще 28 питань
    ]
}

with col1:
    st.markdown("### 🌌 Питання:")
    level_questions = questions[st.session_state["planet"]]
    task = random.choice(level_questions)
    st.write(task["question"])
    user_answer = st.text_input("📝 Введіть вашу відповідь:", "")

# Механіка перевірки відповіді (лівий блок)
with col1:
    if st.button("Перевірити"):
        if st.session_state["lives"] > 0:
            if user_answer.strip().lower() == task["answer"].lower():
                st.session_state["score"] += 10
                st.success("✅ Правильно! Ви отримали 10 очків.")
            else:
                st.session_state["lives"] -= 1
                st.error("❌ Неправильно! Ви втратили 1 життя.")
        else:
            st.warning("У вас закінчилися життя. Дочекайтесь відновлення або перезапустіть гру!")

# Перевірка рівня (лівий блок)
with col1:
    if st.session_state["score"] >= 100:
        st.session_state["planet"] += 1
        st.session_state["score"] = 0
        if st.session_state["planet"] > 3:
            st.balloons()
            st.success(f"🎉 Вітаємо, {st.session_state['username']}! Ви завершили гру!")
        else:
            st.success(f"🎉 Ви перейшли на наступну планету! Планета #{st.session_state['planet']} чекає вас!")

# Таймер для відновлення життя (правий блок)
with col2:
    if st.session_state["lives"] < 10:
        next_life_in = timedelta(minutes=10) - (datetime.now() - st.session_state["last_life_restore"])
        minutes, seconds = divmod(next_life_in.seconds, 60)
        st.info(f"⏳ Наступне життя через: {minutes} хв {seconds} с.")
