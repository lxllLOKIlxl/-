import streamlit as st
import random
from datetime import datetime, timedelta

# Ініціалізація сесійних змінних
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "planet" not in st.session_state:
    st.session_state["planet"] = 1
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 10
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "last_life_restore" not in st.session_state:
    st.session_state["last_life_restore"] = datetime.now()

# Функція для створення запитань
def generate_questions():
    return [
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
    ]

# Вибір нового запитання
def get_new_question():
    if st.session_state["questions"]:
        return random.choice(st.session_state["questions"])
    return None

# Ініціалізація запитань
if not st.session_state["questions"]:
    st.session_state["questions"] = generate_questions()

# Заголовок
st.title("🚀 Кодонавт: Космічна Пригода")

# Введення імені гравця
if not st.session_state["username"]:
    st.session_state["username"] = st.text_input("👤 Введіть ваше ім'я:")
    if st.button("Підтвердити ім'я"):
        if st.session_state["username"].strip():
            st.success(f"Ім'я збережено: {st.session_state['username']}")
            st.session_state["current_question"] = get_new_question()
            st.experimental_rerun()
        else:
            st.warning("Будь ласка, введіть коректне ім'я.")
else:
    # Панель з інформацією про гравця
    st.sidebar.header("Інформація про гравця")
    st.sidebar.write(f"**Ім'я:** {st.session_state['username']}")
    st.sidebar.write(f"**❤️ Життя:** {st.session_state['lives']} / 10")
    st.sidebar.write(f"**💯 Рахунок:** {st.session_state['score']}")
    st.sidebar.write(f"**🌍 Планета:** {st.session_state['planet']}")

    # Основна гра
    if st.session_state["current_question"]:
        question = st.session_state["current_question"]
        st.write(f"**Питання:** {question['question']}")
        user_answer = st.text_input("📝 Введіть вашу відповідь:")

        if st.button("Перевірити"):
            if user_answer.strip().lower() == question["answer"].lower():
                st.success("✅ Правильно! Ви отримали 10 очків.")
                st.session_state["score"] += 10
                st.session_state["questions"].remove(question)
            else:
                st.error("❌ Неправильно! Ви втратили 1 життя.")
                st.session_state["lives"] -= 1

            if st.session_state["score"] >= 100:
                st.balloons()
                st.success("🎉 Ви перейшли на наступний рівень!")
                st.session_state["planet"] += 1
                st.session_state["score"] = 0
                st.session_state["questions"] = generate_questions()
            elif st.session_state["lives"] <= 0:
                st.warning("😢 У вас закінчилися життя. Гру завершено.")
            else:
                st.session_state["current_question"] = get_new_question()
            
            st.experimental_rerun()
    else:
        st.info("🎉 Ви завершили всі запитання цього рівня.")
