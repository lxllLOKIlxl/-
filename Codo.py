import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import threading
import time

# Функція для завантаження перекладів
def load_translations(lang):
    try:
        with open(f"translations/{lang}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Помилка завантаження: файл '{lang}.json' не знайдено.")
        return {}
    except Exception as e:
        st.error(f"Сталася помилка: {e}")
        return {}

# Ініціалізація Firebase через Streamlit Secrets (перевіряємо, чи вже ініціалізовано)
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets["firebase"]["databaseURL"]
    })

# Функція для завантаження фото у Firebase
def upload_photo(image_file):
    image_data = image_file.read()
    image_base64 = image_data.hex()  # Конвертація у HEX
    return image_base64

st.title("Sm: Галерея фото на Firebase")

# Завантаження фото
uploaded_file = st.file_uploader("Завантажте фото", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image_data = upload_photo(uploaded_file)
    description = st.text_area("Опишіть фото тут")

    if st.button("Зберегти"):
        ref = db.reference("photos")
        ref.push({
            "image": image_data,
            "description": description
        })
        st.success("Фото успішно збережене!")

# Відображення всіх фото з Firebase
st.subheader("📸 Галерея")

photos_ref = db.reference("photos").get()
if photos_ref:
    for photo_id, photo_data in photos_ref.items():
        image_bytes = bytes.fromhex(photo_data["image"])
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, use_container_width=True)
        st.write(f"**Опис:** {photo_data['description']}")
