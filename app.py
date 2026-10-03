import time
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
    " Marhamat, savolingizni bering va tezkor javob oling."
)

user_query = st.text_input("Savolingizni yozing:")

if st.button("Javob olish"):
  if user_query:
    # Limitga uchrasa, avtomatik kutib, qayta urinish funksiyasi
    max_retries = 3
    success = False

    for attempt in range(max_retries):
      try:
        with st.spinner("Zeed AI javob tayyorlamoqda..."):
          response = model.generate_content(user_query)
          st.success(response.text)
          success = True
          break
      except Exception as e:
        if "429" in str(e) or "Quota exceeded" in str(e):
          if attempt < max_retries - 1:
            time.sleep(10)  # 10 soniya kutib, qayta urinib ko'radi
            continue
        st.error(f"Xatolik yuz berdi: {e}")
        success = True
        break
  else:
    st.warning("Iltimos, savol kiriting!")
