import streamlit as st
import random
from datetime import datetime, timedelta

# Початкова ініціалізація змінних сесії
if "username" not in st.session_state:
    st.session_state["username"] = None
if "planet" not in st.session_state:
    st.session_state["planet"] = 1
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 10
if "last_life_restore" not in st.session_state:
    st.session_state["last_life_restore"] = datetime.now()
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "question_pool" not in st.session_state:
    st.session_state["question_pool"] = []

# Функція для створення запитань за рівнями
def generate_questions():
    return {
        1: [
            {"question": "Що таке 2 + 2?", "answer": "4"},
            {"question": "Яка планета третя від Сонця?", "answer": "Земля"},
            {"question": "Який результат: 10 // 3?", "answer": "3"},
            {"question": "Яка найближча зірка до Землі?", "answer": "Сонце"},
            {"question": "Столиця України?", "answer": "Київ"},
            {"question": "Скільки днів у лютому у високосний рік?", "answer": "29"},
            {"question": "Який колір має небо?", "answer": "Синій"},
            {"question": "Скільки буде 5 * 5?", "answer": "25"},
            {"question": "Який океан найбільший?", "answer": "Тихий"},
            {"question": "Яке число йде після 5?", "answer": "6"}
        ],
        2: [
            {"question": "Скільки планет у Сонячній системі?", "answer": "8"},
            {"question": "Що таке 9 * 9?", "answer": "81"},
            {"question": "Яка планета найближче до Сонця?", "answer": "Меркурій"},
            {"question": "Який рік має 366 днів?", "answer": "Високосний"},
            # Додайте ще питання
        ],
        3: [
            {"question": "Що таке 12 * 12?", "answer": "144"},
            {"question": "Який супутник обертається навколо Землі?", "answer": "Місяць"},
            # Додайте ще питання
        ]
    }

# Завантаження запитань для поточного рівня
if not st.session_state["question_pool"]:
    st.session_state["question_pool"] = generate_questions()[st.session_state["planet"]]

# Вибір нового запитання
def get_new_question():
    if st.session_state["question_pool"]:
        return random.choice(st.session_state["question_pool"])
    return None

# Перехід до наступного рівня
def next_level():
    st.session_state["planet"] += 1
    st.session_state["score"] = 0
    st.session_state["lives"] = 10
    st.session_state["question_pool"] = generate_questions().get(st.session_state["planet"], [])
    st.session_state["current_question"] = get_new_question()

# Оформлення заголовка гри
st.title("🚀 Кодонавт: Космічна Пригода")
st.markdown("---")

# Введення імені гравця
if st.session_state["username"] is None:
    st.session_state["username"] = st.text_input("Введіть ваше ім'я:")
    if st.session_state["username"]:
        st.session_state["current_question"] = get_new_question()
        st.experimental_rerun()

# Панель з інформацією про гравця
with st.sidebar:
    st.header("Інформація про гравця")
    st.write(f"**Ім'я:** {st.session_state['username']}")
    st.write(f"**❤️ Життя:** {st.session_state['lives']} / 10")
    st.write(f"**💯 Рахунок:** {st.session_state['score']}")
    st.write(f"**🌍 Планета:** {st.session_state['planet']}")

    # Таймер для відновлення життя
    if st.session_state["lives"] < 10:
        time_diff = datetime.now() - st.session_state["last_life_restore"]
        if time_diff >= timedelta(minutes=10):
            restore_lives = time_diff.seconds // 600
            st.session_state["lives"] += restore_lives
            st.session_state["lives"] = min(st.session_state["lives"], 10)
            st.session_state["last_life_restore"] = datetime.now()

        next_life_in = timedelta(minutes=10) - (datetime.now() - st.session_state["last_life_restore"])
        minutes, seconds = divmod(next_life_in.seconds, 60)
        st.info(f"⏳ Наступне життя через: {minutes} хв {seconds} с.")

# Основний блок гри
st.header("🌌 Ваша місія")
if st.session_state["current_question"]:
    st.write(f"**Запитання:** {st.session_state['current_question']['question']}")
    user_answer = st.text_input("📝 Ваша відповідь:")

    if st.button("Перевірити"):
        if user_answer.strip().lower() == st.session_state["current_question"]["answer"].lower():
            st.success("✅ Правильно! Ви отримали 10 очків.")
            st.session_state["score"] += 10
            st.session_state["question_pool"].remove(st.session_state["current_question"])
        else:
            st.error("❌ Неправильно! Ви втратили 1 життя.")
            st.session_state["lives"] -= 1

        if st.session_state["score"] >= 100:
            st.balloons()
            st.success("🎉 Ви перейшли на наступний рівень!")
            next_level()
        elif st.session_state["lives"] <= 0:
            st.warning("😢 У вас закінчилися життя. Гру завершено.")
        else:
            st.session_state["current_question"] = get_new_question()
            st.experimental_rerun()
else:
    st.info("🎉 Ви завершили всі запитання цього рівня. Натисніть, щоб перейти далі.")
