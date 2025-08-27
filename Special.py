import math
import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="A Special Surprise 💌", page_icon="❤️", layout="centered")

# Compliments (no raw links; just plain text & emoji)
compliments = [
    "✨ You light up every room you walk into",
    "❤️ Spending time with you is my favorite thing",
    "💻💕 You’re smarter and cuter than any code I could write",
    "🌸 Every day with you feels special",
    "🔔❤️ You're my favorite notification",
    "😊 One smile from you makes my whole day better"
]

final_message = "💌 This app was made just for you... because you’re truly special to me 💕"

# Session state
if "clicks" not in st.session_state:
    st.session_state.clicks = 0
if "used" not in st.session_state:
    st.session_state.used = set()

# Header (pure HTML; safe in Instagram/Safari)
components.html(
    """
    <meta charset="UTF-8">
    <div style="text-align:center; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;">
      <h1 style="color:#ff3366;margin:12px 0 6px;">Hi, Beautiful 💖</h1>
      <div style="font-size:72px;line-height:1;">❤️</div>
    </div>
    """,
    height=160,
    scrolling=False
)

# Button
if st.button("Click me 💕", use_container_width=True):
    st.session_state.clicks += 1

# Compliments (HTML only)
if 0 < st.session_state.clicks < 5:
    remaining = [c for c in compliments if c not in st.session_state.used]
    if not remaining:
        st.session_state.used.clear()
        remaining = compliments
    msg = random.choice(remaining)
    st.session_state.used.add(msg)

    components.html(
        f"""
        <meta charset="UTF-8">
        <div style="display:flex;justify-content:center;">
          <div style="font-size:20px;padding:10px 14px;border-radius:16px;background:#fff0f5;">
            {msg}
          </div>
        </div>
        """,
        height=90,
        scrolling=False
    )

# Final reveal (typing + floating hearts; no Streamlit balloons needed)
elif st.session_state.clicks >= 5:
    components.html(
        f"""
        <meta charset="UTF-8">
        <div id="wrap" style="text-align:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;">
          <h3 id="msg" style="color:#660033;margin:8px auto;max-width:680px;white-space:pre-wrap;"></h3>
        </div>
        <script>
          // Typing effect
          const text = `{final_message}`;
          let i = 0;
          (function type() {{
            if (i <= text.length) {{
              document.getElementById('msg').textContent = text.slice(0, i);
              i++;
              setTimeout(type, 35);
            }}
          }})();

          // Floating hearts
          for (let j = 0; j < 26; j++) {{
            const heart = document.createElement('div');
            heart.textContent = '💗';
            heart.style.position = 'fixed';
            heart.style.top = '-10px';
            heart.style.left = (Math.random() * 100) + 'vw';
            heart.style.fontSize = (Math.random() * 22 + 22) + 'px';
            heart.style.opacity = '0.85';
            heart.style.pointerEvents = 'none';
            heart.style.transform = 'translateY(0)';
            heart.style.animation = `fall ${4 + Math.random() * 3}s linear ${Math.random() * 2}s forwards`;
            document.body.appendChild(heart);
          }}
        </script>
        <style>
          @keyframes fall {{
            to {{ transform: translateY(110vh) rotate(360deg); opacity: 0; }}
          }}
        </style>
        """,
        height=300,
        scrolling=False
    )

