import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Function to adjust brightness using histogram equalization
def adjust_brightness(image, brightness):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the scaling factor for brightness adjustment
    scaling_factor = (brightness + 100) / 100
    
    # Apply scaling factor to adjust brightness
    adjusted_image = cv2.convertScaleAbs(gray_image, alpha=scaling_factor, beta=0)
    
    # Convert the adjusted image back to BGR color space
    adjusted_bgr_image = cv2.cvtColor(adjusted_image, cv2.COLOR_GRAY2BGR)
    
    return adjusted_bgr_image

# Function to sketch an image
def sketch_image(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert the grayscale image
    inverted_gray_image = 255 - gray_image
    
    # Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blurred_image = 255 - blurred_image
    
    # Create the sketch image
    sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
    
    return sketch_image

def main():
    st.title("เว็บไซต์ปรับแต่งรูปภาพ")
    
    st.sidebar.title("Options")
    mode = st.sidebar.radio("เลือกโหมด:", ("โหมดสร้างภาพ Sketch", "โหมดการปรับความสว่างรูปภาพ"))
    
    if mode == "โหมดสร้างภาพ Sketch":
        st.sidebar.write("โหมดสร้างภาพ Sketch")
        uploaded_file = st.file_uploader("อัพโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="รูปต้นฉบับ", use_column_width=True)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert image to BGR for OpenCV
            sketch = sketch_image(image_array)
            st.image(sketch, caption="รูป Sketch ", use_column_width=True)
    
    elif mode == "โหมดการปรับความสว่างรูปภาพ":
        st.sidebar.write("โหมดการปรับความสว่างรูปภาพ")
        uploaded_file = st.file_uploader("อัพโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="รูปต้นฉบับ", use_column_width=True)
            brightness = st.sidebar.slider("ความสว่าง", min_value=-100, max_value=100, value=0, step=1)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert image to BGR for OpenCV
            brightness_adjusted_image = adjust_brightness(image_array, brightness)
            st.image(brightness_adjusted_image, caption="รูปที่ปรับความสว่างแล้ว", use_column_width=True)

if __name__ == "__main__":
    main()
