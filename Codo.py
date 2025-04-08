import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
from PIL import Image
import io

# Ініціалізація Firebase
cred = credentials.Certificate("firebase_key.json")  # Використай локальний JSON-файл
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dyfcalcchat-default-rtdb.firebaseio.com/'
})

def upload_photo(image_file):
    image_data = image_file.read()
    image_base64 = image_data.hex()  # Конвертація фото у HEX для збереження
    return image_base64

st.title("Sm: Галерея фото")

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
        st.success("Фото збережено!")

st.subheader("📸 Галерея")

ref = db.reference("photos").get()
if ref:
    for photo_id, photo_data in ref.items():
        image_bytes = bytes.fromhex(photo_data["image"])
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, use_container_width=True)
        st.write(f"**Опис:** {photo_data['description']}")
