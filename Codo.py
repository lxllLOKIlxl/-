import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import io
from PIL import Image

# Ініціалізація Firebase (перевіряємо, чи вже запущено)
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
        "databaseURL": st.secrets["firebase"]["databaseURL"]
    })

# Функція для збереження фото у Firebase
def upload_photo(image_file):
    image_data = image_file.read()
    image_base64 = image_data.hex()  # Конвертуємо у HEX
    return image_base64

st.title("Sm: Галерея фото та повідомлень")

# Завантаження фото
uploaded_file = st.file_uploader("Завантажте фото", type=["jpg", "png", "jpeg"])
description = st.text_area("Опишіть фото тут")

if uploaded_file and st.button("Зберегти фото"):
    image_data = upload_photo(uploaded_file)
    ref = db.reference("photos")
    ref.push({
        "image": image_data,
        "description": description
    })
    st.success("Фото успішно збережене!")

# Відображення галереї фото
st.subheader("📸 Галерея")
photos_ref = db.reference("photos").get()
if photos_ref:
    for photo_id, photo_data in photos_ref.items():
        image_bytes = bytes.fromhex(photo_data["image"])
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, use_container_width=True)
        st.write(f"**Опис:** {photo_data['description']}")

# Форма для повідомлень
st.subheader("💬 Чат")
message = st.text_input("Напишіть повідомлення")

if st.button("Надіслати повідомлення"):
    ref = db.reference("messages")
    ref.push({
        "text": message,
        "timestamp": db.ServerValue.TIMESTAMP  # Додаємо час надсилання
    })
    st.success("Повідомлення надіслано!")

# Відображення повідомлень
st.subheader("📨 Повідомлення")
messages_ref = db.reference("messages").order_by_child("timestamp").get()
if messages_ref:
    for msg_id, msg_data in messages_ref.items():
        st.write(f"💬 {msg_data['text']}")
