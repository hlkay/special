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

# Keep track of clicks
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

if st.button("💌 Click me for a surprise"):
    st.session_state.clicks += 1
    if st.session_state.clicks < 5:
        st.success(random.choice(messages))
    else:
        st.markdown(
            "<h2 style='text-align:center; color:#ff1493;'>Final Message: I Worked my ass off for this just for you. ❤️</h2>",
            unsafe_allow_html=True,
        )
