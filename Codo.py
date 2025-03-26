import streamlit as st
import random
from datetime import datetime, timedelta

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
            {"question": "Яка формула води?", "answer": "H2O"},
            {"question": "Хто написав 'Кобзар'?", "answer": "Тарас Шевченко"},
            {"question": "Скільки сторін у трикутника?", "answer": "3"},
            {"question": "Яка столиця Франції?", "answer": "Париж"},
            {"question": "Що таке квадратний корінь з 16?", "answer": "4"},
            {"question": "Яка найбільша тварина на Землі?", "answer": "Синій кит"}
        ],
        3: [
            {"question": "Що таке 12 * 12?", "answer": "144"},
            {"question": "Який супутник обертається навколо Землі?", "answer": "Місяць"},
            {"question": "Яка хімічна формула вуглекислого газу?", "answer": "CO2"},
            {"question": "Хто відкрив пеніцилін?", "answer": "Александр Флемінг"},
            {"question": "Скільки кутів у прямокутника?", "answer": "4"},
            {"question": "Яка найвища гора у світі?", "answer": "Еверест"},
            {"question": "Що таке 15 поділити на 3?", "answer": "5"},
            {"question": "Яка країна є батьківщиною кенгуру?", "answer": "Австралія"},
            {"question": "Який газ становить більшість атмосфери Землі?", "answer": "Азот"},
            {"question": "Що таке площа квадрата зі стороною 7?", "answer": "49"}
        ],
        4: [
            {"question": "Яка столиця Японії?", "answer": "Токіо"},
            {"question": "Що таке 2 в ступені 8?", "answer": "256"},
            {"question": "Яка планета відома своїми кільцями?", "answer": "Сатурн"},
            {"question": "Хто є автором 'Гамлета'?", "answer": "Вільям Шекспір"},
            {"question": "Скільки нот в октаві?", "answer": "8"},
            {"question": "Яка найдовша річка у світі?", "answer": "Амазонка"},
            {"question": "Що таке 10 відсотків від 50?", "answer": "5"},
            {"question": "Яка офіційна мова Бразилії?", "answer": "Португальська"},
            {"question": "Який хімічний символ золота?", "answer": "Au"},
            {"question": "Що таке об'єм куба зі стороною 3?", "answer": "27"}
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
    st.session_state["lives"] = 10
if "last_life_restore" not in st.session_state:
    st.session_state["last_life_restore"] = datetime.now()
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "question_pool" not in st.session_state:
    st.session_state["question_pool"] = []
if "level_completed" not in st.session_state:
    st.session_state["level_completed"] = False

# Завантаження запитань для поточного рівня
def load_questions():
    st.session_state["question_pool"] = generate_questions().get(st.session_state["planet"], [])
    if st.session_state["question_pool"]:
        st.session_state["current_question"] = random.choice(st.session_state["question_pool"])
    else:
        st.session_state["current_question"] = None

# Перехід до наступного рівня
def next_level():
    st.session_state["planet"] += 1
    st.session_state["score"] = 0
    st.session_state["lives"] = 10
    st.session_state["level_completed"] = False
    load_questions()

# Перевірка відповіді
def check_answer():
    if st.session_state["current_question"] and "user_answer" in st.session_state:
        if st.session_state["user_answer"].strip().lower() == st.session_state["current_question"]["answer"].lower():
            st.success("✅ Правильно! Ви отримали 10 очків.")
            st.session_state["score"] += 10
            st.session_state["question_pool"].remove(st.session_state["current_question"])
            if st.session_state["question_pool"]:
                st.session_state["current_question"] = random.choice(st.session_state["question_pool"])
                st.session_state["user_answer"] = "" # Очистити поле вводу
            else:
                st.session_state["current_question"] = None
                st.session_state["level_completed"] = True
        else:
            st.error("❌ Неправильно! Ви втратили 1 життя.")
            st.session_state["lives"] -= 1
            st.session_state["current_question"] = random.choice(st.session_state["question_pool"]) if st.session_state["question_pool"] else None
            st.session_state["user_answer"] = "" # Очистити поле вводу

# Оформлення заголовка гри
st.title("🚀 Кодонавт: Космічна Пригода")
st.markdown("---")

# Введення імені гравця
if not st.session_state["username"]:
    st.session_state["username"] = st.text_input("Введіть ваше ім'я:")
    if st.session_state["username"]:
        load_questions()
        st.experimental_rerun()

# Бічна панель з інформацією про гравця
if st.session_state["username"]:
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

    if st.session_state["lives"] > 0:
        if st.session_state["current_question"]:
            st.write(f"**Запитання:** {st.session_state['current_question']['question']}")
            st.session_state["user_answer"] = st.text_input("📝 Ваша відповідь:", key="answer_input")
            if st.button("Перевірити"):
                check_answer()
                st.experimental_rerun()
        elif st.session_state["level_completed"]:
            st.balloons()
            st.success(f"🎉 Вітаємо, {st.session_state['username']}! Ви успішно пройшли планету {st.session_state['planet']}!")
            if st.session_state["planet"] < len(generate_questions()):
                if st.button(f"🚀 Вирушити на планету {st.session_state['planet'] + 1}"):
                    next_level()
                    st.experimental_rerun()
            else:
                st.info("🎉 Ви дослідили всі планети! Ваша космічна подорож завершена!")
        else:
            if st.session_state["planet"] <= len(generate_questions()):
                st.info("🤔 Запитання на цій планеті закінчились. Спробуйте ще раз або перейдіть далі.")
                if st.button(f"➡️ Перейти на планету {st.session_state['planet'] + 1}"):
                    next_level()
                    st.experimental_rerun()
            elif st.session_state["planet"] > len(generate_questions()):
                st.info("🎉 Ви завершили всі рівні!")
            else:
                st.info("⏳ Завантажуємо запитання...")
                load_questions()
                st.experimental_rerun()

    else:
        st.warning(f"😢 У {st.session_state['username']} закінчилися життя. Гру завершено.")
        if st.button("🔄 Спробувати знову"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
