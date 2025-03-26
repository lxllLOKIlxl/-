import streamlit as st
import random
from datetime import datetime, timedelta
import time

# Налаштування сторінки
st.set_page_config(page_title="Кодонавт: Космічна Пригода", page_icon="🚀")

# Функція для створення запитань за рівнями
def generate_questions():
    return {
        1: [
            {"question": "Що таке 2 + 2?", "answer": "4", "difficulty": "легко"},
            {"question": "Яка планета третя від Сонця?", "answer": "Земля", "difficulty": "легко"},
            {"question": "Який результат: 10 // 3?", "answer": "3", "difficulty": "легко"},
            {"question": "Яка найближча зірка до Землі?", "answer": "Сонце", "difficulty": "легко"},
            {"question": "Столиця України?", "answer": "Київ", "difficulty": "легко"},
        ],
        2: [
            {"question": "Скільки планет у Сонячній системі?", "answer": "8", "difficulty": "середньо"},
            {"question": "Що таке 9 * 9?", "answer": "81", "difficulty": "середньо"},
            {"question": "Яка планета найближче до Сонця?", "answer": "Меркурій", "difficulty": "середньо"},
            {"question": "Яка формула води?", "answer": "H2O", "difficulty": "середньо"},
            {"question": "Хто написав 'Кобзар'?", "answer": "Тарас Шевченко", "difficulty": "середньо"},
        ],
        3: [
            {"question": "Що таке 12 * 12?", "answer": "144", "difficulty": "складно"},
            {"question": "Який супутник обертається навколо Землі?", "answer": "Місяць", "difficulty": "складно"},
            {"question": "Яка хімічна формула вуглекислого газу?", "answer": "CO2", "difficulty": "складно"},
            {"question": "Хто відкрив пеніцилін?", "answer": "Александр Флемінг", "difficulty": "складно"},
            {"question": "Яка найвища гора у світі?", "answer": "Еверест", "difficulty": "складно"},
        ],
        4: [
            {"question": "Яка столиця Японії?", "answer": "Токіо", "difficulty": "дуже складно"},
            {"question": "Що таке 2 в ступені 8?", "answer": "256", "difficulty": "дуже складно"},
            {"question": "Яка планета відома своїми кільцями?", "answer": "Сатурн", "difficulty": "дуже складно"},
            {"question": "Хто є автором 'Гамлета'?", "answer": "Вільям Шекспір", "difficulty": "дуже складно"},
            {"question": "Скільки нот в октаві?", "answer": "8", "difficulty": "дуже складно"},
        ]
    }

# Початкова ініціалізація змінних сесії
if "username" not in st.session_state:
    st.session_state["username"] = None
if "planet" not in st.session_state:
    st.session_state["planet"] = 1
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 3
if "last_life_restore" not in st.session_state:
    st.session_state["last_life_restore"] = datetime.now()
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "question_pool" not in st.session_state:
    st.session_state["question_pool"] = []
if "level_completed" not in st.session_state:
    st.session_state["level_completed"] = False
if "game_over" not in st.session_state:
    st.session_state["game_over"] = False
if "hint_used" not in st.session_state:
    st.session_state["hint_used"] = False

# Функція для завантаження запитань для поточного рівня
def load_questions():
    st.session_state["question_pool"] = generate_questions().get(st.session_state["planet"], [])
    if st.session_state["question_pool"]:
        random.shuffle(st.session_state["question_pool"])
        st.session_state["current_question"] = st.session_state["question_pool"].pop()
        st.session_state["hint_used"] = False
    else:
        st.session_state["current_question"] = None
        st.session_state["level_completed"] = True

# Перехід до наступного рівня
def next_level():
    st.session_state["planet"] += 1
    st.session_state["score"] += st.session_state.get("level_score", 0) # Зараховуємо рахунок за попередній рівень
    st.session_state["lives"] = 3
    st.session_state["level_completed"] = False
    st.session_state["level_score"] = 0
    load_questions()

# Перевірка відповіді
def check_answer():
    if st.session_state["current_question"] and "user_answer" in st.session_state:
        if st.session_state["user_answer"].strip().lower() == st.session_state["current_question"]["answer"].lower():
            st.success(f"✅ Правильно! Ви отримали 10 очків ({st.session_state['current_question']['difficulty']}).")
            st.session_state["score"] += 10
            st.session_state["level_score"] = st.session_state.get("level_score", 0) + 10
            st.session_state["user_answer"] = ""
            st.session_state["current_question"] = None # Питання видаляється після відповіді
            st.experimental_rerun()
        else:
            st.error(f"❌ Неправильно! Спробуйте ще раз. ({st.session_state['current_question']['difficulty']})")
            st.session_state["lives"] -= 1
            st.session_state["user_answer"] = ""

# Показати підказку
def show_hint():
    if st.session_state["current_question"] and not st.session_state["hint_used"]:
        answer = st.session_state["current_question"]["answer"]
        if len(answer) > 3:
            hint = "*" * (len(answer) - 2) + answer[-2:]
            st.info(f"💡 Підказка: Відповідь закінчується на '{answer[-2:]}'.")
            st.session_state["hint_used"] = True
        else:
            st.info("🤔 Підказка для цієї відповіді недоступна.")

# Оформлення гри
st.title("🚀 Кодонавт: Космічна Пригода")
st.markdown("---")

# Введення імені гравця
if not st.session_state["username"]:
    st.session_state["username"] = st.text_input("Введіть ваше ім'я, юний коднавте:")
    if st.session_state["username"]:
        st.info(f"Привіт, {st.session_state['username']}! Готові до космічної подорожі?")
        load_questions()
        st.experimental_rerun()

# Основний блок гри
if st.session_state["username"]:
    with st.sidebar:
        st.header(f"Інформація для {st.session_state['username']}")
        st.write(f"**❤️ Життя:** {st.session_state['lives']}")
        st.write(f"**💯 Загальний рахунок:** {st.session_state['score']}")
        st.write(f"**🌍 Планета:** {st.session_state['planet']}")
        st.write(f"**⭐ Рахунок на планеті:** {st.session_state.get('level_score', 0)}")

        if st.session_state["lives"] > 0 and not st.session_state["game_over"]:
            if st.button("Здатись"):
                st.session_state["lives"] = 0
                st.experimental_rerun()

    st.header(f"🪐 Планета {st.session_state['planet']}")

    if st.session_state["lives"] > 0 and not st.session_state["game_over"]:
        if st.session_state["current_question"]:
            st.subheader("❓ Запитання:")
            st.markdown(f"> {st.session_state['current_question']['question']}")
            st.session_state["user_answer"] = st.text_input("Ваша відповідь:", key="answer_input")

            cols = st.columns(2)
            with cols[0]:
                if st.button("Перевірити"):
                    check_answer()
                    if st.session_state["current_question"] is None and st.session_state["lives"] > 0:
                        if not st.session_state["question_pool"]:
                            st.session_state["level_completed"] = True
                            st.experimental_rerun()
                        else:
                            st.session_state["current_question"] = st.session_state["question_pool"].pop()
                            st.session_state["hint_used"] = False
                            st.experimental_rerun()
            with cols[1]:
                if st.button("Підказка"):
                    show_hint()

        elif st.session_state["level_completed"]:
            st.balloons()
            st.success(f"🎉 Вітаємо, {st.session_state['username']}! Ви пройшли планету {st.session_state['planet']}!")
            if st.session_state["planet"] < len(generate_questions()):
                if st.button(f"🚀 Вирушити на планету {st.session_state['planet'] + 1}"):
                    next_level()
                    st.experimental_rerun()
            else:
                st.info("✨ Ви дослідили всі планети! Ваша космічна подорож завершена!")
                st.session_state["game_over"] = True
                st.experimental_rerun()
        else:
            if st.session_state["lives"] > 0 and not st.session_state["game_over"]:
                if not st.session_state["question_pool"]:
                    st.info("🤔 Запитання на цій планеті закінчились. Перейдіть на наступну.")
                    if st.session_state["planet"] < len(generate_questions()):
                        if st.button(f"➡️ Перейти на планету {st.session_state['planet'] + 1}"):
                            next_level()
                            st.experimental_rerun()
                    else:
                        st.info("✨ Ви дослідили всі планети! Ваша космічна подорож завершена!")
                        st.session_state["game_over"] = True
                        st.experimental_rerun()
                else:
                    load_questions()
                    st.experimental_rerun()

    elif st.session_state["lives"] <= 0:
        st.error(f"💀 Гра закінчена, {st.session_state['username']}! Ви використали всі життя.")
        st.subheader(f"Ваш фінальний рахунок: {st.session_state['score']}")
        if st.button("🔄 Спробувати знову"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()

    elif st.session_state["game_over"]:
        st.info("✨ Дякуємо за гру, коднавте!")
        if st.button("🔄 Почати нову гру"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()

else:
    st.info("Будь ласка, введіть ваше ім'я, щоб розпочати.")
