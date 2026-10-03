import os
import google.generativeai as genai
import streamlit as st

# Sahifa sozlamalari (keng ekran va sarlavha)
st.set_page_config(
    page_title="Zeed AI — Professional Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Maxsus CSS dizayn va zamonaviy uslub berish
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
    .css-164nlkn {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar (Yon panel) dizayni va sozlamalari
with st.sidebar:
  st.image(
      "https://img.icons8.com/clouds/200/artificial-intelligence.png", width=120
  )
  st.title("Zeed AI Panel")
  st.markdown("---")

  # Modelni tanlash
  model_choice = st.selectbox(
      "Modelni tanlang:",
      ["gemini-1.5-pro", "gemini-1.5-flash"],
      help="Flash - tezkor, Pro - chuqur tahlil uchun",
  )

  # Kreativlik darajasi (Temperature)
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
      "⚠️️ **Diqqat!** `GOOGLE_API_KEY` topilmadi. Iltimos, Render.com"
      " sozlamalarida Environment Variables qismiga kalitni qo'shing."
  )
else:
  genai.configure(api_key=api_key)

  # Chat tarixini xotirada saqlash uchun
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Oldingi xabarlarni ekranga chiqarish
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Foydalanuvchidan habar olish
  if prompt := st.chat_input("Savolingizni shu yerga yozing..."):
    # Foydalanuvchi xabarini tarixga qo'shish
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # Gemini modelini chaqirish
    try:
      generation_config = {"temperature": temperature}
      model = genai.GenerativeModel(
          model_name=model_choice, generation_config=generation_config
      )

      with st.chat_message("assistant"):
        with st.spinner("Zeed AI o'ylamoqda..."):
          # Suhbat tarixini formatlab uzatish
          chat_history = [
              {"role": m["role"], "parts": [m["content"]]}
              for m in st.session_state.messages
          ]
          chat = model.start_chat(history=[])
          response = chat.send_message(prompt)
          bot_reply = response.text

          st.markdown(bot_reply)

          # Bot javobini tarixga qo'shish
          st.session_state.messages.append(
              {"role": "model", "content": bot_reply}
          )

    except Exception as e:
      st.error(f"❌ Xatolik yuz berdi: {e}")
