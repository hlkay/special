import streamlit as st
import random

st.set_page_config(page_title="For You ❤️", page_icon="✨", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#e75480;'>A Little Surprise 💕</h1>",
    unsafe_allow_html=True,
)

messages = [
    "You make my heart smile every single day 💖",
    "Life feels magical with you in it ✨",
    "I’m so lucky to have you 💕",
    "You’re my favorite notification 💌",
    "Every moment with you is my favorite 🥰",
    "You’re the best thing that ever happened to me ❤️",
]

if st.button("💌 Click me for a surprise"):
    st.success(random.choice(messages))
