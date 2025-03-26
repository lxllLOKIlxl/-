import streamlit as st
import random

# Назва гри
st.title("Кодонавт")

# Початкові змінні
if "planet" not in st.session_state:
    st.session_state["planet"] = 1
if "score" not in st.session_state:
    st.session_state["score"] = 0

# Опис поточної планети
st.write(f"🌍 Ви на планеті #{st.session_state['planet']}. Ваша місія — вирішити задачу, щоб продовжити подорож.")
st.write(f"Ваш поточний рахунок: {st.session_state['score']}")

# Задача
task = random.choice([
    {"question": "Що таке 2 + 2?", "answer": "4"},
    {"question": "Яка планета третя від Сонця?", "answer": "Земля"},
    {"question": "Який результат: 10 // 3?", "answer": "3"}
])

st.write("Задача:", task["question"])
user_answer = st.text_input("Ваша відповідь:")

# Кнопка для перевірки
if st.button("Перевірити"):
    if user_answer.lower() == task["answer"].lower():
        st.success("Правильно! 🚀 Ви переходите на наступну планету!")
        st.session_state["planet"] += 1
        st.session_state["score"] += 10
    else:
        st.error("Неправильно 😢 Спробуйте ще раз!")

# Завершення
if st.session_state["planet"] > 5:
    st.balloons()
    st.write(f"🎉 Вітаємо! Ви дослідили всі планети! Ваш фінальний рахунок: {st.session_state['score']}")
