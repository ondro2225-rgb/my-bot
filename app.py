import streamlit as st
import google.generativeai as genai

# Sahifa sarlavhasi
st.set_page_config(page_title="Smart AI Yordamchi", page_icon="🤖")

st.title("🤖 Smart AI Yordamchi")
st.write("Salom! Men sizning shaxsiy sun'iy intellekt yordamchingizman. Marhamat, savolingizni bering.")

# Foydalanuvchi o'zining API kalitini kiritishi uchun maxsus joy
api_key = st.text_input("Google AI Studio API kalitingizni kiriting:", type="password")

if api_key:
    try:
        # API kalitni sozlaymiz
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Foydalanuvchidan savol qabul qilish
        user_prompt = st.text_input("Savolingizni yozing:")
        
        if st.button("Javob olish") and user_prompt:
            with st.spinner("Sun'iy intellekt o'ylamoqda..."):
                response = model.generate_content(user_prompt)
                st.success("Javob:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
else:
    st.info("Iltimos, saytdan foydalanish uchun o'zingizning Google AI Studio API kalitingizni kiriting.")
