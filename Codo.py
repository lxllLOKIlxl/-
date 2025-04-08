import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import io
from PIL import Image
import time

# --- Додаємо чорний фон із плавним переходом ---
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(90deg, black, #1a1a1a);
            color: white;
        }
        .stApp {
            background: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Оформлення заголовка ---
st.markdown('<h1 style="color:red; text-align:center;">Sm</h1>', unsafe_allow_html=True)

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
    image_base64 = image_data.hex()
    return image_base64

# --- Бокове випливаюче меню для логіну ---
with st.sidebar:
    st.subheader("🔒 Адмін-логін")
    admin_login = st.text_input("Логін:")
    admin_password = st.text_input("Пароль:", type="password")
    is_admin = admin_login == "Loki" and admin_password == "19871987"

# --- Центр: Завантаження фото та опису ---
st.subheader("📸 Завантаження фото")
uploaded_file = st.file_uploader("Завантажте фото", type=["jpg", "png", "jpeg"])
description = st.text_area("Опишіть фото тут")

if is_admin:  # Фото може завантажувати лише адмін
    if uploaded_file and st.button("Зберегти фото"):
        image_data = upload_photo(uploaded_file)
        ref = db.reference("photos")
        ref.push({
            "image": image_data,
            "description": description
        })
        st.success("Фото успішно збережене!")
else:
    st.warning("⚠️ Фото можуть додавати тільки адміністратори.")

# --- Центр: Галерея фото ---
st.subheader("📷 Галерея")
photos_ref = db.reference("photos").get()
if photos_ref:
    for photo_id, photo_data in photos_ref.items():
        image_bytes = bytes.fromhex(photo_data["image"])
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, use_container_width=True)
        st.write(f"**Опис:** {photo_data['description']}")

# --- Бокова панель: Чат ---
st.sidebar.subheader("💬 Чат")
message = st.sidebar.text_input("Напишіть повідомлення")
if st.sidebar.button("Надіслати повідомлення"):
    ref = db.reference("messages")
    ref.push({
        "text": message,
        "timestamp": {".sv": "timestamp"}  # Автоматичний час у Firebase
    })
    st.sidebar.success("Повідомлення надіслано!")

# --- Видалення повідомлень після 24 годин ---
messages_ref = db.reference("messages").get()
if messages_ref:
    current_time = int(time.time() * 1000)  # Поточний час у мілісекундах
    for msg_id, msg_data in messages_ref.items():
        if "timestamp" in msg_data and current_time - msg_data["timestamp"] > 86400:  # 24 години = 86400 мс
            db.reference(f"messages/{msg_id}").delete()

# --- Відображення повідомлень у боковій панелі ---
st.sidebar.subheader("📨 Повідомлення")
messages_ref = db.reference("messages").order_by_child("timestamp").get()
if messages_ref:
    for msg_id, msg_data in messages_ref.items():
        message_text = msg_data.get("text", "Немає тексту")
        timestamp = msg_data.get("timestamp", "Час недоступний")
        st.sidebar.write(f"💬 {message_text} (🕒 {timestamp})")
else:
    st.sidebar.write("❌ Немає повідомлень")
    
    # --- Бокова панель: Контактна інформація ---
with st.sidebar:
    st.markdown('<h2 style="text-align:center; color:red;">Sm Підтримка</h2>', unsafe_allow_html=True)
    st.subheader("📞 Контакти")
    st.write("📱 Адміністратор: +380 99 362 55 37")
    st.write("📱 Техпідтримка: +380 96 522 26 37")

# --- Додаємо Sm ver 1.0 внизу випливаючого вікна ---
with st.sidebar:
    st.markdown('<p style="text-align:center; color:gray; font-size:14px;">Sm ver 1.0</p>', unsafe_allow_html=True)
