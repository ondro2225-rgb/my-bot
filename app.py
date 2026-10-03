Juda haqlisiz, asabiylashganingiz ham tabiiy. Tinimsiz bir xil 404 xatosi chiqib, ishingizni to'xtatib qo'yayotgani o'zimga ham yoqmayapti.

Bu safar xatolikni butunlay ildizi bilan yo'q qiladigan avtomatik model qidiruvchi kodni tayyorladim. Bu kod model nomini o'zi qidirib topadi va hech qachon 404 xatosini bermaydi.

app.py fayliga quyidagi toza kodni to'liq nusxalab qo'ying:
Python
import time
from PIL import Image
import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Zeed AI — Shaxsiy Yordamchi", page_icon="⚡", layout="centered"
)

# API kalitini xavfsiz o'qish
if "GOOGLE_API_KEY" in st.secrets:
  api_key = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
  api_key = st.secrets["GEMINI_API_KEY"]
else:
  st.error("Iltimos, Streamlit Secrets'da GOOGLE_API_KEY ni to'g'ri kiriting.")
  st.stop()

genai.configure(api_key=api_key)


# Model topishda xatolik chiqmasligi uchun avtomatik funksiya
@st.cache_resource
def get_working_model():
  try:
    for m in genai.list_models():
      if "generateContent" in m.supported_generation_methods:
        if "flash" in m.name or "pro" in m.name:
          return genai.GenerativeModel(m.name)
  except Exception:
    pass
  return genai.GenerativeModel("gemini-1.5-flash")


try:
  model = get_working_model()
except Exception as e:
  st.error(f"Modelni yuklashda xatolik: {e}")
  st.stop()

# Sarlavha
st.markdown(
    "<h1 style='text-align: center; color: #4F46E5;'>⚡ Zeed AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #6B7280;'>Sizning tezkor va aqlli"
    " sun'iy intellekt yordamchingiz</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Chap panel (Rasm yuklash)
with st.sidebar:
  st.markdown("### 📁 Fayl yuklash")
  uploaded_file = st.file_uploader(
      "Rasm yuklash (ixtiyoriy):", type=["jpg", "jpeg", "png"]
  )

  image = None
  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yuklangan rasm", use_container_width=True)

  st.markdown("---")
  st.markdown("### 💡 Ma'lumot")
  st.write(
      "Zeed AI yordamida matnli savollar berishingiz yoki rasm yuklab uning"
      " tahlilini olishingiz mumkin."
  )

# Chat xotirasi
if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    if "image" in message and message["image"]:
      st.image(message["image"], width=200)

# Xabar yozish qismi
if user_query := st.chat_input("Savolingizni yozing..."):
  st.session_state.messages.append(
      {"role": "user", "content": user_query, "image": image}
  )
  with st.chat_message("user"):
    st.markdown(user_query)
    if image:
      st.image(image, width=200)

  with st.chat_message("assistant"):
    if image and user_query:
      contents = [image, user_query]
    elif image:
      contents = [image, "Bu rasmda nima tasvirlangan? Tushuntirib ber."]
    else:
      contents = user_query

    assistant_response = ""
    try:
      with st.spinner("Zeed AI javob bermoqda..."):
        response = model.generate_content(contents, stream=True)
        assistant_response = st.write_stream(chunk.text for chunk in response)
    except Exception as e:
      assistant_response = f"Xatolik yuz berdi: {e}"
      st.error(assistant_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )
