import streamlit as st  # เรียกใช้งานไลบรารี Streamlit
import cv2  # เรียกใช้งาน OpenCV
from PIL import Image  # เรียกใช้งานไลบรารี PIL (Python Imaging Library) สำหรับการจัดการรูปภาพ
import numpy as np  # เรียกใช้งานไลบรารี NumPy สำหรับการจัดการข้อมูลอาร์เรย์

# สำหรับตั้งค่าภาพพื้นหลัง 
page_bg_img = '''<style>
.stApp {
    background-image: url('https://img.freepik.com/free-vector/hand-drawn-minimal-background_23-2149001650.jpg');
    background-size: cover;
}
<style>'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ฟังก์ชันสำหรับปรับความสว่างของรูปภาพโดยใช้ Histogram Equalization
def adjust_brightness(image, brightness):
    # แปลงรูปภาพเป็นสีเทา
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # คำนวณ scaling factor เพื่อปรับความสว่าง
    scaling_factor = (brightness + 100) / 100
    
    # ปรับความสว่างของรูปภาพ
    adjusted_image = cv2.convertScaleAbs(gray_image, alpha=scaling_factor, beta=0)
    
    # แปลงรูปภาพที่ปรับความสว่างแล้วกลับเป็นภาพสี BGR
    adjusted_bgr_image = cv2.cvtColor(adjusted_image, cv2.COLOR_GRAY2BGR)
    
    return adjusted_bgr_image

# ฟังก์ชันสำหรับสร้างภาพ Sketch จากรูปภาพต้นฉบับ
def sketch_image(image):
    # แปลงรูปภาพเป็นสีเทา
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert รูปภาพสีเทา
    inverted_gray_image = 255 - gray_image
    
    # ใช้ Gaussian Blur
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    
    # Invert รูปภาพที่ blur
    inverted_blurred_image = 255 - blurred_image
    
    # สร้างภาพ Sketch
    sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
    
    return sketch_image

# ฟังก์ชันหลักของโปรแกรม
def main():
    # สร้างเว็บแอปพลิเคชัน
    st.title("เว็บไซต์ปรับแต่งรูปภาพ")
    st.sidebar.title("Options")
    mode = st.sidebar.radio("เลือกโหมด:", ("โหมดสร้างภาพ Sketch", "โหมดการปรับความสว่างรูปภาพ"))
    
    if mode == "โหมดสร้างภาพ Sketch":
        st.sidebar.write("โหมดสร้างภาพ Sketch")
        uploaded_file = st.file_uploader("อัพโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="รูปต้นฉบับ", use_column_width=True)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # แปลงรูปภาพเป็น BGR สำหรับ OpenCV
            sketch = sketch_image(image_array)
            st.image(sketch, caption="รูป Sketch ", use_column_width=True)
    
    elif mode == "โหมดการปรับความสว่างรูปภาพ":
        st.sidebar.write("โหมดการปรับความสว่างรูปภาพ")
        uploaded_file = st.file_uploader("อัพโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="รูปต้นฉบับ", use_column_width=True)
            brightness = st.sidebar.slider("ความสว่าง", min_value=-100, max_value=100, value=0, step=1)
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # แปลงรูปภาพเป็น BGR สำหรับ OpenCV
            brightness_adjusted_image = adjust_brightness(image_array, brightness)
            st.image(brightness_adjusted_image, caption="รูปที่ปรับความสว่างแล้ว", use_column_width=True)

# เรียกใช้งานฟังก์ชันหลักเมื่อเป็นไปตามเงื่อนไข
if __name__ == "__main__":
    main()
