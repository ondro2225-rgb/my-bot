import os
import google.generativeai as genai
import streamlit as st

# Sahifa sozlamalari
st.set_page_config(
    page_title="Zeed AI — Professional Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Maxsus CSS dizayn
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput textarea {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar sozlamalari
with st.sidebar:
  st.title("Zeed AI Panel")
  st.markdown("---")

  model_choice = st.selectbox(
      "Modelni tanlang:", ["gemini-pro", "gemini-1.5-flash"]
  )

  temperature = st.slider(
      "Kreativlik darajasi:",
      min_value=0.0,
      max_value=1.0,
      value=0.7,
      step=0.1,
  )

  st.markdown("---")
  st.info(
      "💡 **Zeed AI** — Google Gemini quvvati asosida ishlaydigan aqlli yordamchi."
  )

# Asosiy ekran
st.title("🤖 Zeed AI Workspace")
st.markdown(
    "Xohlagan savolingizni bering, matn yozing yoki kod tuzing. Sizga tez"
    " va aniq javob beraman!"
)

# API kalitni tekshirish
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
  st.error(
      "⚠ **Diqqat!** `GOOGLE_API_KEY` topilmadi. Iltimos, Render.com"
      " sozlamalarida Environment Variables qismiga kalitni qo'shing."
  )
else:
  genai.configure(api_key=api_key)

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Savolingizni shu yerga yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    try:
      model = genai.GenerativeModel(model_choice)

      with st.chat_message("assistant"):
        with st.spinner("Zeed AI o'ylamoqda..."):
          response = model.generate_content(prompt)
          bot_reply = response.text

          st.markdown(bot_reply)
          st.session_state.messages.append(
              {"role": "model", "content": bot_reply}
          )

    except Exception as e:
      st.error(f"❌ Xatolik yuz berdi: {e}")
