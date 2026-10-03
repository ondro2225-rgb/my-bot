import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(page_title="Zeed AI - Sun'iy Intellekt Yordamchi", page_icon="⚡")

# Asosiy interfeys
st.title("⚡ Zeed AI")
st.write("Salom! Men **Zeed AI** — sizning shaxsiy sun'iy intellekt yordamchingizman. Marhamat, savolingizni bering va tezkor javob oling.")

# Streamlit maxfiy joyidan API kalitni olamiz
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Modelni sozlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Foydalanuvchidan savol qabul qilish
    user_prompt = st.text_input("Savolingizni yozing:")
    
    if st.button("Javob olish") and user_prompt:
        with st.spinner("Zeed AI o'ylamoqda..."):
            response = model.generate_content(user_prompt)
            st.success("Javob:")
            st.write(response.text)
            
except Exception as e:
    st.error("Iltimos, ilova sozlamalarida (Secrets) API kalitni to'g'ri kiriting.")
