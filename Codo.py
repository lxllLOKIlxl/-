import streamlit as st
import random

# Налаштування сторінки
st.set_page_config(page_title="Кодонавт: Космічна Пригода", layout="centered")
st.title("🚀 Кодонавт: Космічна Пригода")
st.markdown("Уникайте ворогів та знищуйте їх, щоб набрати очки!")

# Початкові змінні
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 3
if "enemies" not in st.session_state:
    st.session_state["enemies"] = [random.randint(0, 10) for _ in range(5)]
if "player_position" not in st.session_state:
    st.session_state["player_position"] = 5
if "bullets" not in st.session_state:
    st.session_state["bullets"] = []

# Функції гри
def move_player(direction):
    if direction == "left" and st.session_state["player_position"] > 0:
        st.session_state["player_position"] -= 1
    elif direction == "right" and st.session_state["player_position"] < 10:
        st.session_state["player_position"] += 1

def shoot():
    st.session_state["bullets"].append(st.session_state["player_position"])

def move_enemies():
    new_enemies = []
    for enemy in st.session_state["enemies"]:
        if enemy < 10:
            new_enemies.append(enemy + 1)
        else:
            st.session_state["lives"] -= 1
    st.session_state["enemies"] = new_enemies

def check_hits():
    hits = []
    for bullet in st.session_state["bullets"]:
        if bullet in st.session_state["enemies"]:
            st.session_state["score"] += 1
            hits.append(bullet)
    st.session_state["bullets"] = [b for b in st.session_state["bullets"] if b not in hits]
    st.session_state["enemies"] = [e for e in st.session_state["enemies"] if e not in hits]

def game_over():
    st.error("💥 Гру завершено! Ваш рахунок: " + str(st.session_state["score"]))
    st.button("🔄 Почати заново", on_click=reset_game)

def reset_game():
    st.session_state["score"] = 0
    st.session_state["lives"] = 3
    st.session_state["enemies"] = [random.randint(0, 10) for _ in range(5)]
    st.session_state["player_position"] = 5
    st.session_state["bullets"] = []

# Логіка гри
if st.session_state["lives"] > 0:
    # Рух ворогів
    move_enemies()

    # Перевірка попадань
    check_hits()

    # Відображення гри
    st.write("### Поле гри:")
    for i in range(11):
        if i == st.session_state["player_position"]:
            st.write("🚀", end=" ")
        elif i in st.session_state["enemies"]:
            st.write("💣", end=" ")
        elif i in st.session_state["bullets"]:
            st.write("🔫", end=" ")
        else:
            st.write("⬛", end=" ")
    st.write("\n")

    # Дії гравця
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
    game_over()
