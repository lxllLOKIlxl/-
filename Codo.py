import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import io
from PIL import Image

# Ініціалізація Firebase через Streamlit Secrets
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase_key"]["type"],
        "project_id": st.secrets["firebase_key"]["project_id"],
        "private_key_id": st.secrets["firebase_key"]["private_key_id"],
        "private_key": st.secrets["firebase_key"]["private_key"],
        "client_email": st.secrets["firebase_key"]["client_email"],
        "client_id": st.secrets["firebase_key"]["client_id"],
        "databaseURL": st.secrets["firebase_key"]["databaseURL"]
    })
    firebase_admin.initialize_app(cred, {
        "databaseURL": st.secrets["firebase_key"]["databaseURL"]
    })

# Функція для збереження фото в Firebase
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
