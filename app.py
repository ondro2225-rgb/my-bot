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

# Modelni sozlash
model = genai.GenerativeModel("gemini-3.8-flash")

st.markdown("# ⚡ Zeed AI")
st.write(
    "Salom! Men Zeed AI — sizning shaxsiy sun'iy intellekt yordamchingiz."
    " Marhamat, tezkor javob oling!"
)

# Rasm yuklash (ixtiyoriy)
uploaded_file = st.file_uploader(
    "Rasm yuklash (ixtiyoriy):", type=["jpg", "jpeg", "png"]
)

image = None
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Yuklangan rasm", use_container_width=True)

user_query = st.text_input(
    "Savolingizni yoki rasm bo'yicha izohingizni yozing:"
)

if st.button("Javob olish"):
  if not user_query and not image:
    st.warning("Iltimos, savol yozing yoki rasm yuklang!")
  else:
    try:
      # Kontentni shakllantirish
      if image and user_query:
        contents = [image, user_query]
      elif image:
        contents = [image, "Bu rasmda nima tasvirlangan? Tushuntirib ber."]
      else:
        contents = user_query

      # Streaming (Tezkor oqimli) javob olish funksiyasi
      response = model.generate_content(contents, stream=True)

      # Javobni ekranga darhol, so'zma-so'z chiqarish
      st.write_stream(chunk.text for chunk in response)

    except Exception as e:
      st.error(f"Xatolik yuz berdi: {e}")
