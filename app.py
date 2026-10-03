import time
from PIL import Image
import google.generativeai as genai
import streamlit as st

# Sahifa sozlamalari
st.set_page_config(
    page_title="Zeed AI — Shaxsiy Yordamchi", page_icon="⚡", layout="centered"
)

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

# Chap tarafdagi menyu (Sidebar) - rasm yuklash uchun
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

# Chat tarixini saqlash uchun xotira
if "messages" not in st.session_state:
  st.session_state.messages = []

# Oldingi xabarlarni ekranga chiqarish (Chat tarixi saqlanib turishi uchun)
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    if "image" in message and message["image"]:
      st.image(message["image"], width=200)

# Pastdagi yozish oynasi (Xuddi ChatGPT kabi)
if user_query := st.chat_input("Savolingizni yozing..."):
  # Foydalanuvchi xabarini tarixga qo'shish va chiqarish
  st.session_state.messages.append(
      {"role": "user", "content": user_query, "image": image}
  )
  with st.chat_message("user"):
    st.markdown(user_query)
    if image:
      st.image(image, width=200)

  # AI javobini tayyorlash
  with st.chat_message("assistant"):
    # Kontentni shakllantirish
    if image and user_query:
      contents = [image, user_query]
    elif image:
      contents = [image, "Bu rasmda nima tasvirlangan? Tushuntirib ber."]
    else:
      contents = user_query

    max_retries = 3
    assistant_response = ""

    for attempt in range(max_retries):
      try:
        with st.spinner("Zeed AI o'ylamoqda..."):
          response = model.generate_content(contents, stream=True)
          # Streaming orqali yozib chiqarish
          assistant_response = st.write_stream(chunk.text for chunk in response)
          break
      except Exception as e:
        error_str = str(e)
        if "429" in error_str or "Quota exceeded" in error_str:
          if attempt < max_retries - 1:
            time.sleep(15)
            continue
        assistant_response = f"Xatolik yuz berdi: {e}"
        st.error(assistant_response)
        break

    # AI javobini tarixga qo'shish
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )
