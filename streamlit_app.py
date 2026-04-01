import streamlit as st
import matplotlib.pyplot as plt
from groq import Groq

# 1. Groq AI sozlamalari
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Smart Wallet", page_icon="💰")
st.title("💰 Moliyaviy Reja va Aqlli AI")

# --- MA'LUMOTLARNI KIRITISH ---
col1, col2 = st.columns(2)
with col1:
    income = st.number_input("Oylik daromad (so'm):", min_value=0, value=5000000)
    rent = st.number_input("Uy ijarasi:", min_value=0, value=0)
    food = st.number_input("Oziq-ovqat:", min_value=0, value=0)
with col2:
    transport = st.number_input("Transport:", min_value=0, value=0)
    internet = st.number_input("Internet:", min_value=0, value=0)
    entertainment = st.number_input("Ko'ngilochar:", min_value=0, value=0)

total_expenses = rent + food + transport + internet + entertainment
balance = income - total_expenses

st.divider()
st.metric("💰 Umumiy qoldiq", f"{balance:,} so'm")

# --- DIAGRAMMA ---
labels = ['Ijara', 'Oziq-ovqat', 'Transport', 'Internet', 'Ko\'ngilochar']
values = [rent, food, transport, internet, entertainment]
final_labels = [labels[i] for i in range(len(values)) if values[i] > 0]
final_values = [v for v in values if v > 0]

if sum(final_values) > 0:
    st.subheader("📊 Xarajatlar taqsimoti")
    fig, ax = plt.subplots()
    ax.pie(final_values, labels=final_labels, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
else:
    st.info("Diagramma chiqishi uchun xarajatlarni kiriting.")

# --- 🤖 AI CHATBOT (Aqlli Model) ---
st.divider()
st.subheader("🤖 Aqlli Moliyaviy Maslahatchi")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat tarixini ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Foydalanuvchi savoli
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # AIga sizning hisob-kitoblaringizni tushuntiramiz
        context = (f"Foydalanuvchi daromadi: {income}. Xarajatlari: "
                   f"Ijara {rent}, Ovqat {food}, Transport {transport}, Internet {internet}, "
                   f"Ko'ngilochar {entertainment}. Qoldiq: {balance} so'm.")
        
        try:
            # Eng aqlli model (70b) dan foydalanamiz
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "Siz professional moliyaviy maslahatchisiz. O'zbek tilida, mantiqiy va takrorlarsiz javob bering."
                    },
                    {
                        "role": "user", 
                        "content": f"{context} Savol: {prompt}"
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )
            
            # Javobni to'g'ri olish tartibi
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")




