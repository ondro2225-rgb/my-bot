import time
from PIL import Image
import google.generativeai as genai
import streamlit as st

# Sahifa sozlamalari
st.set_page_config(
    page_title="Zeed AI — Tezkor Yordamchi", page_icon="⚡", layout="centered"
)

# Secrets ichidan kalitni olish
if "GOOGLE_API_KEY" in st.secrets:
  api_key = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
  api_key = st.GEMINI_API_KEY
else:
  st.error("Iltimos, ilova sozlamalarida (Secrets) API kalitini to'g'ri kiriting.")
  st.stop()

genai.configure(api_key=api_key)


# Ishlaydigan modelni avtomatik topish funksiyasi
def get_working_model():
  try:
    # Avval eng so'nggi va tezkor modellarni sinab ko'ramiz
    for m in genai.list_models():
      if "generateContent" in m.supported_generation_methods:
        if "flash" in m.name or "pro" in m.name:
          return m.name
  except Exception:
    pass
  return "gemini-1.5-flash"  # Zaxira variant


model_name = get_working_model()
model = genai.GenerativeModel(model_name)

# Sarlavha dizayni
st.markdown(
    "<h1 style='text-align: center; color: #4F46E5;'>⚡ Zeed AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #6B7280;'>Sizning eng tezkor va"
    " aqlli yordamchingiz</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Chap tarafdagi menyu (Rasm yuklash uchun)
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
  st.write("Zeed AI yordamida tezkor javoblar va rasm tahlilini oling.")

# Chat tarixini saqlash
if "messages" not in st.session_state:
  st.session_state.messages = []

# Oldingi xabarlarni chiqarish
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    if "image" in message and message["image"]:
      st.image(message["image"], width=200)

# Pastdagi chat input oynasi
if user_query := st.chat_input("Savolingizni yozing..."):
  st.session_state.messages.append(
      {"role": "user", "content": user_query, "image": image}
  )
  with st.chat_message("user"):
    st.markdown(user_query)
    if image:
      st.image(image, width=200)

  # AI javobini tezkor shakllantirish
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
Nima qilish kerak:
