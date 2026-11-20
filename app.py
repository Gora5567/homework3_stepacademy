
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="smart photo editor",
    page_icon="📷",
    layout="wide"
)

st.title("smart photo editor")
st.write("загрузите фото и примените к нему фильтр")

st.sidebar.header("настройка фильтра")

uploaded_file = st.sidebar.file_uploader(
    "оберіть зображення",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("оригинальное фото")
        st.image(img_array, use_container_width=True)

    filter_option = st.sidebar.selectbox(
        "выберите эффект",
        [
            "оригинал",
            "черно белый",
            "размытие",
            "инверсия",
            "віддзеркалення",
            "налаштування яскравості",
            "налаштування контрасту",
            "колірний сплеск"
        ]
    )

    processed_img = img_array.copy()

    # черно белый фильтр
    if filter_option == "черно белый":
        gray = cv2.cvtColor(
            img_array,
            cv2.COLOR_RGB2GRAY
        )
        processed_img = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2RGB
        )

    # размытие
    elif filter_option == "размытие":
        processed_img = cv2.GaussianBlur(
            img_array,
            (15, 15),
            0
        )

    # инверсия
    elif filter_option == "инверсия":
        processed_img = 255 - img_array

    # горизонтальное отражение
    elif filter_option == "віддзеркалення":
        processed_img = cv2.flip(img_array, 1)

    # настройка яркости
    elif filter_option == "налаштування яскравості":

        brightness_val = st.sidebar.slider(
            "рівень яскравості",
            -100,
            100,
            0
        )

        processed_img = cv2.convertScaleAbs(
            img_array,
            alpha=1.0,
            beta=brightness_val
        )

    # настройка контраста
    elif filter_option == "налаштування контрасту":

        contrast_val = st.sidebar.slider(
            "рівень контрасту",
            0.5,
            3.0,
            1.0,
            step=0.1
        )

        processed_img = cv2.convertScaleAbs(
            img_array,
            alpha=contrast_val,
            beta=0
        )

    # цветной сплеск
    elif filter_option == "колірний сплеск":

        selected_color = st.sidebar.selectbox(
            "оберіть колір",
            ["червоний", "зелений", "синій"]
        )

        # перевод изображения в hsv
        hsv = cv2.cvtColor(
            img_array,
            cv2.COLOR_RGB2HSV
        )

        # определение диапазонов цветов
        if selected_color == "червоний":

            low_color1 = np.array([0, 50, 50])
            high_color1 = np.array([10, 255, 255])

            low_color2 = np.array([170, 50, 50])
            high_color2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(
                hsv,
                low_color1,
                high_color1
            )

            mask2 = cv2.inRange(
                hsv,
                low_color2,
                high_color2
            )

            mask = cv2.bitwise_or(mask1, mask2)

        elif selected_color == "зелений":

            low_color = np.array([35, 50, 50])
            high_color = np.array([85, 255, 255])

            mask = cv2.inRange(
                hsv,
                low_color,
                high_color
            )

        else:

            low_color = np.array([90, 50, 50])
            high_color = np.array([130, 255, 255])

            mask = cv2.inRange(
                hsv,
                low_color,
                high_color
            )

        # создание черно белого изображения
        gray = cv2.cvtColor(
            img_array,
            cv2.COLOR_RGB2GRAY
        )

        gray_rgb = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2RGB
        )

        # объединение цветного и черно белого изображений
        processed_img = np.where(
            mask[:, :, np.newaxis] > 0,
            img_array,
            gray_rgb
        )

    with col2:
        st.subheader("обработанная фотография")
        st.image(processed_img, use_container_width=True)
