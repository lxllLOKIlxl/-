import streamlit as st

# Заголовок сторінки
st.title("Sm: Галерея фото та описів")

# Завантаження фото
uploaded_file = st.file_uploader("Завантажте фото", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Ваше фото", use_container_width=True)

    # Додавання опису
    description = st.text_area("Опишіть фото тут")

    if description:
        st.write("### Опис:")
        st.write(description)
