import google.generativeai as genai
import streamlit as st

# Secrets ichidan kalitni qidirish (ikkala variantni ham qo'llab-quvvatlaydi)
if "GOOGLE_API_KEY" in st.secrets:
  api_key = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
else:
  st.error("Iltimos, ilova sozlamalarida (Secrets) API kalitini to'g'ri kiriting.")
  st.stop()

genai.configure(api_key=api_key)

# Modelni sozlash
model = genai.GenerativeModel("gemini-1.5-flash")

# Zeed AI interfeysi
st.markdown("# ⚡ Zeed AI")
st.write(
    "Salom! Men Zeed AI — sizning shaxsiy sun'iy intellekt yordamchingiz."
    " Marhamat, savolingizni bering va tezkor javob oling."
)

user_query = st.text_input("Savolingizni yozing:")

if st.button("Javob olish"):
  if user_query:
    try:
      response = model.generate_content(user_query)
      st.success(response.text)
    except Exception as e:
      st.error(f"Xatolik yuz berdi: {e}")
  else:
      st.warning("Iltimos, savol kiriting!")
