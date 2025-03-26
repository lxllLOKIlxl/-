import streamlit as st
import random

# Налаштування сторінки
st.set_page_config(page_title="Кодонавт: Оборона Галактики", layout="centered")
st.title("🚀 Кодонавт: Оборона Галактики")
st.markdown("Захищайте галактику, уникаючи ворогів та знищуючи їх пострілами! 🎮")

# Початкові змінні
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 3
if "player_position" not in st.session_state:
    st.session_state["player_position"] = 5  # Початкова позиція гравця
if "enemies" not in st.session_state:
    st.session_state["enemies"] = [random.randint(0, 10) for _ in range(5)]
if "bullets" not in st.session_state:
    st.session_state["bullets"] = []

# Функції гри
def move_player(direction):
    """Рух гравця"""
    if direction == "left" and st.session_state["player_position"] > 0:
        st.session_state["player_position"] -= 1
    elif direction == "right" and st.session_state["player_position"] < 10:
        st.session_state["player_position"] += 1

def shoot():
    """Вистріл гравця"""
    st.session_state["bullets"].append(st.session_state["player_position"])

def move_enemies():
    """Рух ворогів вниз по ігровому полю"""
    new_enemies = []
    for enemy in st.session_state["enemies"]:
        if enemy < 10:
            new_enemies.append(enemy + 1)
        else:
            st.session_state["lives"] -= 1  # Втрата життя, якщо ворог досяг кінця
    st.session_state["enemies"] = new_enemies

def check_hits():
    """Перевірка попадань по ворогах"""
    hits = []
    for bullet in st.session_state["bullets"]:
        if bullet in st.session_state["enemies"]:
            st.session_state["score"] += 1  # Додати очки за знищеного ворога
            hits.append(bullet)
    st.session_state["bullets"] = [b for b in st.session_state["bullets"] if b not in hits]
    st.session_state["enemies"] = [e for e in st.session_state["enemies"] if e not in hits]

def reset_game():
    """Скидання гри"""
    st.session_state["score"] = 0
    st.session_state["lives"] = 3
    st.session_state["player_position"] = 5
    st.session_state["enemies"] = [random.randint(0, 10) for _ in range(5)]
    st.session_state["bullets"] = []

# Перевірка стану гри
if st.session_state["lives"] > 0:
    # Рух ворогів
    move_enemies()

    # Перевірка попадань
    check_hits()

    # Відображення гри
    st.write("### Поле гри:")
    field = ""
    for i in range(11):
        if i == st.session_state["player_position"]:
            field += "🚀 "  # Гравець
        elif i in st.session_state["enemies"]:
            field += "💣 "  # Ворог
        elif i in st.session_state["bullets"]:
            field += "🔫 "  # Куля
        else:
            field += "⬛ "  # Пусте місце
    st.write(field)

    # Управління
    st.write("### Управління:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Вліво"):
            move_player("left")
    with col2:
        if st.button("🚀 Вистрілити"):
            shoot()
    with col3:
        if st.button("➡️ Вправо"):
            move_player("right")

    # Інформація про гру
    st.write(f"**Рахунок:** {st.session_state['score']}")
    st.write(f"**Життя:** {st.session_state['lives']}")

else:
    # Завершення гри
    st.error("💥 Гру завершено!")
    st.write(f"Ваш фінальний рахунок: {st.session_state['score']}")
    if st.button("🔄 Почати заново"):
        reset_game()
