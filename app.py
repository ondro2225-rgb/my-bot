import time
from PIL import Image
import google.generativeai as genai
import streamlit as st

# Secrets ichidan kalitni olish
if "GOOGLE_API_KEY" in st.secrets:
  api_key = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
else:
  st.error("Iltimos, ilova sozlamalarida (Secrets) API kalitini to'g'ri kiriting.")
  st.stop()

genai.configure(api_key=api_key)

# Modelni sozlash (Multimodal — rasm va matnni qo'llab-quvvatlaydigan model)
model = genai.GenerativeModel("gemini-3.8-flash")

st.markdown("# ⚡ Zeed AI")
st.write(
    "Salom! Men Zeed AI — sizning shaxsiy sun'iy intellekt yordamchingiz."
    " Marhamat, xohlasangiz matnli savol yozing, xohlasangiz rasm yuklab"
    " murojaat qiling!"
)

# Foydalanuvchidan rasm yuklashni so'rash (ixtiyoriy)
uploaded_file = st.file_uploader(
    "Rasm yuklash (ixtiyoriy):", type=["jpg", "jpeg", "png"]
)

# Agar rasm yuklangan bo'lsa, ekranda ko'rsatamiz
image = None
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Yuklangan rasm", use_container_width=True)

# Savol kiritish maydoni
user_query = st.text_input(
    "Savolingizni yoki rasm bo'yicha izohingizni yozing:"
)

if st.button("Javob olish"):
  if not user_query and not image:
    st.warning("Iltimos, savol yozing yoki rasm yuklang!")
  else:
    max_retries = 3
    for attempt in range(max_retries):
      try:
        with st.spinner("Zeed AI javob tayyorlamoqda..."):
          # Agar rasm va matn birga bo'lsa
          if image and user_query:
            response = model.generate_content([image, user_query])
          # Faqat rasm bo'lsa
          elif image:
            response = model.generate_content([image, "Bu rasmda nima tasvirlangan? Tushuntirib ber."])
          # Faqat matn bo'lsa
          else:
            response = model.generate_content(user_query)

          st.success(response.text)
          break
      except Exception as e:
        if "429" in str(e) or "Quota exceeded" in str(e):
          if attempt < max_retries - 1:
            time.sleep(10)
            continue
        st.error(f"Xatolik yuz berdi: {e}")
        break
