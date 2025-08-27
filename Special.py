import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime
import base64

st.set_page_config(page_title="A Surprise for You", page_icon="❤️", layout="centered")

# Inject some CSS for nicer look
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #FFF0F5 0%, #FFF8E1 100%);
}
.header {
  text-align: center;
}
.card {
  background: rgba(255,255,255,0.8);
  padding: 18px;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.small-muted {font-size:0.9rem;color:#555}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header"><h1>✨ A Little Surprise ✨</h1></div>', unsafe_allow_html=True)

with st.expander('How to use (quick)'):
    st.write("""
    1. Enter your name and your girl's name.
    2. Add photos (optional) to create a carousel and an e-card.
    3. Customize the message and hit *Surprise!* to see confetti and preview.
    4. Download the e-card to send her.
    """)

# Inputs
col1, col2 = st.columns(2)
with col1:
    your_name = st.text_input("Your name", value="")
    her_name = st.text_input("Her name", value="")

with col2:
    special_date = st.date_input("Special date (optional countdown)", value=None)
    music_url = st.text_input("Optional: YouTube link to a song (paste full URL)")

message = st.text_area("Write a heartfelt message (this will appear on the e-card)", value=f"Dear {her_name if her_name else 'Love'},\n\nYou make my world brighter every day.")

uploaded_images = st.file_uploader("Upload photos (optional) — shows in a carousel", type=["png","jpg","jpeg"], accept_multiple_files=True)

# show images
if uploaded_images:
    imgs = []
    for u in uploaded_images:
        try:
            img = Image.open(u).convert('RGB')
            imgs.append(img)
        except Exception:
            st.warning('Could not open one of the uploaded files.')

    st.markdown("### Photo carousel")
    cols = st.columns(len(imgs))
    for i, img in enumerate(imgs):
        cols[i].image(img, use_column_width='always')
else:
    st.info('No photos uploaded — you can still create and download the e-card.')

# Countdown
if isinstance(special_date, datetime.date):
    today = datetime.date.today()
    if special_date > today:
        days_left = (special_date - today).days
        st.success(f"Countdown: {days_left} days until {special_date.strftime('%b %d, %Y')}")
    elif special_date == today:
        st.success("Today is your special day — happy day!")
    else:
        st.info("The date you selected is in the past.")

# Generate E-card function
def generate_ecard(name_to, name_from, message_text, image: Image.Image=None, size=(1200,700)):
    card = Image.new('RGB', size, (255,245,238))
    draw = ImageDraw.Draw(card)

    # try to use a nice system font; fallback to default
    try:
        font_title = ImageFont.truetype('DejaVuSans-Bold.ttf', 56)
        font_body = ImageFont.truetype('DejaVuSans.ttf', 28)
    except Exception:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Draw optional photo on the left
    padding = 40
    if image:
        img_thumb = image.copy()
        img_thumb.thumbnail((size[0]//2 - 2*padding, size[1] - 2*padding))
        card.paste(img_thumb, (padding, padding))
        text_x = size[0]//2 + padding//2
    else:
        text_x = padding

    # Title
    title = f"To {name_to if name_to else 'Someone Special'},"
    draw.text((text_x, padding), title, font=font_title, fill=(60,20,60))

    # Message (wrap manually)
    body_lines = []
    max_width = size[0] - text_x - padding
    words = message_text.split()
    line = ''
    for w in words:
        test = line + (' ' if line else '') + w
        wsize = draw.textsize(test, font=font_body)[0]
        if wsize <= max_width:
            line = test
        else:
            body_lines.append(line)
            line = w
    if line:
        body_lines.append(line)

    y = padding + 90
    for bl in body_lines:
        draw.text((text_x, y), bl, font=font_body, fill=(30,30,30))
        y += 40

    # From
    from_text = f"Love,\n{ name_from if name_from else '' }"
    draw.text((text_x, size[1] - padding - 80), from_text, font=font_body, fill=(60,20,60))

    return card

# Surprise button
st.markdown('<div class="card">', unsafe_allow_html=True)
if st.button('🎉 Surprise!'):
    # show confetti via tiny JS
    confetti_html = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <canvas id="confetti-canvas" style="position:fixed;pointer-events:none;top:0;left:0;width:100vw;height:100vh;z-index:999999;"></canvas>
    <script>
    var myCanvas = document.getElementById('confetti-canvas');
    myCanvas.width = window.innerWidth;
    myCanvas.height = window.innerHeight;
    var myConfetti = confetti.create(myCanvas, { resize: true, useWorker: true });
    myConfetti({ particleCount: 150, spread: 120 });
    </script>
    """
    st.components.v1.html(confetti_html, height=0)

    st.markdown(f"### {your_name if your_name else 'Someone'} says:")
    st.markdown(f"> {message.replace('\n','  \n> ')}")

    # Show generated e-card preview
    preview_img = None
    if uploaded_images:
        preview_img = imgs[0]

    ecard = generate_ecard(her_name, your_name, message, image=preview_img)
    buf = io.BytesIO()
    ecard.save(buf, format='PNG')
    buf.seek(0)
    st.image(ecard, caption='E-card preview (downloadable)')

    st.download_button("Download e-card (PNG)", data=buf, file_name=f"ecard_for_{her_name or 'love'}.png", mime='image/png')

    # Optional music embed
    if music_url:
        st.markdown('### Song for her')
        # naive youtube embed
        if 'youtube' in music_url:
            try:
                video_id = music_url.split('v=')[1].split('&')[0]
                iframe = f"<iframe width='100%' height='166' src='https://www.youtube.com/embed/{video_id}?autoplay=0&controls=1' title='Song' frameborder='0' allow=" + 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture' + "></iframe>"
                st.components.v1.html(iframe, height=200)
            except Exception:
                st.write('Could not parse YouTube link. Paste full URL like https://www.youtube.com/watch?v=...')
        else:
            st.write('Non-YouTube links may not embed correctly.')

st.markdown('</div>', unsafe_allow_html=True)

# "How well do you know me" mini-quiz
st.markdown('---')
st.markdown('## Mini quiz: How well do you know each other?')
q1 = st.radio('What is her favorite color (choose one)?', ['Red','Blue','Pink','Green','Other'])
q2 = st.radio('Ideal date: ', ['Dinner & movie','Beach','Home-cooked meal','Theme park','Other'])
q3 = st.radio('She prefers: ', ['Morning','Afternoon','Night'])

if st.button('Score our answers'):
    score = 0
    # these are placeholders — user can grade manually
    if q1 == 'Pink': score += 1
    if q2 == 'Home-cooked meal': score += 1
    if q3 == 'Night': score += 1
    st.success(f'You scored {score}/3 — not bad! Adjust the correct answers in the app code if you want to personalize.')

# Finishing notes and run instructions
st.markdown('---')
st.markdown('**Ready to deploy?**')
st.markdown('1. Save this file as `romantic_streamlit_app.py`.')
st.markdown('2. Install dependencies: `pip install streamlit pillow`')
st.markdown('3. Run locally: `streamlit run romantic_streamlit_app.py`')
st.markdown('4. Or deploy to Streamlit Community Cloud (app.streamlit.io) — create a new app pointing to this repo.')

st.caption('Made with ❤️ — edit the messages and art to make it truly yours.')
