import numpy as np
import streamlit as st
import io
from PIL import Image

# ----- Page configs -----
st.set_page_config(
    page_title="Image Cropper Portfolio",
    page_icon="📊",
)

# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to open, crop, display and save images using NumPy, PIL, and Matplotlib.")

# ----- Title of the page -----
st.title("🖼️ Image Cropper")
st.divider()

# ----- Getting the image from the user or using a default one -----
is_example = False
img = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

if img is None:
    is_example = True
    with Image.open("data/starry_night.png") as img:
        img_arr = np.array(img)
else:
    with Image.open(img) as img:
        img_arr = np.array(img)

# Displaying the image
st.image(img_arr, caption="Original Image" if not is_example else "Original example image", use_column_width=True)
st.write("#")

# ----- Get min and max values for cropping -----
min_height = 0
max_height = img_arr.shape[0]  # Get height
min_width = 0
max_width = img_arr.shape[1]   # Get width

# ----- Creating the sliders for user input -----
cols1 = st.columns([4, 1, 4])
crop_min_h, crop_max_h = cols1[0].slider("Crop Vertical Range", min_height, max_height, (int(max_height*0.1), int(max_height*0.9)))
crop_min_w, crop_max_w = cols1[2].slider("Crop Horizontal Range", min_width, max_width, (int(max_width*0.1), int(max_width*0.9)))

st.write("## Cropped Image")

# ----- Cropping the image -----
crop_arr = img_arr[crop_min_h:crop_max_h, crop_min_w:crop_max_w]

# ----- Displaying and allowing download of the cropped image -----
st.image(crop_arr, caption="Cropped Image", use_column_width=True)

buf = io.BytesIO()
Image.fromarray(crop_arr).save(buf, format="PNG")
cropped_img_bytes = buf.getvalue()

cols2 = st.columns([4, 1, 4])
file_name = cols2[0].text_input("Choose a File Name:", "cropped_image") + ".png"

st.download_button(f"Download the image `{file_name}`", cropped_img_bytes, file_name=file_name)
