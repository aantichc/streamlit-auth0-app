import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import os
import time

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# Check if user is already logged in
if st.user and st.user.is_logged_in:
    st.session_state.logged_in = True

# Set page config as the first Streamlit command when logged in
if st.session_state.logged_in:
    st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")

# Force light mode, brighten button text, make text dark, and scale text with window size
st.markdown(
    """
    <style>
    /* Force light mode */
    body {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .stApp {
        background-color: #ffffff !important;
    }
    /* Brighten button text */
    .stButton > button {
        color: #ffffff !important; /* Bright white text */
        background-color: #005EA8 !important; /* Contrasting background */
        font-weight: bold !important;
        font-size: calc(0.7rem + 0.4vw) !important; /* Tighter button text scaling */
    }
    /* Ensure button text remains bright on hover */
    .stButton > button:hover {
        color: #ffffff !important;
        background-color: #004080 !important;
    }
    /* Make main app title dark and scalable */
    h1 {
        color: #222222 !important;
        font-size: calc(1.2rem + 1.5vw) !important; /* Tighter title scaling */
        line-height: 1.2 !important;
    }
    /* Make login page header dark and scalable */
    h2, .stMarkdown h2 {
        color: #222222 !important;
        font-size: calc(1rem + 1vw) !important; /* Tighter header scaling */
    }
    /* Make login page write text dark and scalable */
    .stMarkdown p, .stText {
        color: #222222 !important;
        font-size: calc(0.8rem + 0.6vw) !important; /* Tighter write text scaling */
    }
    /* Scale survival probability text */
    .survival-text {
        font-size: calc(1.5rem + 3vw) !important; /* Tighter survival % scaling */
    }
    .survival-caption {
        font-size: calc(0.7rem + 0.8vw) !important; /* Tighter caption scaling */
    }
    /* Scale metrics text tightly */
    .metric-label {
        font-size: calc(0.6rem + 0.5vw) !important; /* Smaller metric labels */
    }
    .metric-value {
        font-size: calc(0.8rem + 0.8vw) !important; /* Smaller metric values */
    }
    /* Force columns to stay horizontal and shrink */
    .stColumns > div {
        flex-shrink: 1 !important;
        flex-grow: 0 !important;
        min-width: 0 !important;
        max-width: 25% !important; /* Cap column width for 4 columns */
        padding: 0.2rem !important; /* Reduce padding */
        margin: 0 !important; /* Remove margins */
        box-sizing: border-box !important;
    }
    /* Ensure columns container stays horizontal */
    .stColumns {
        display: flex !important;
        flex-wrap: nowrap !important; /* Prevent wrapping */
        overflow-x: auto !important; /* Allow horizontal scroll if needed */
    }
    /* Ensure container width adapts */
    .main .block-container {
        max-width: 100% !important;
        padding: 0.5rem !important; /* Tighter padding */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login page
if not st.session_state.logged_in:
    st.title("Sistema de Login")
    st.header("Iniciar Sesión o Registrarse")
    st.write("Accede o crea una cuenta con Auth0.")
    if st.button("Iniciar Sesión / Registrarse"):
        st.login("auth0")
        if st.user and st.user.is_logged_in:
            st.session_state.logged_in = True
            time.sleep(1)  # Brief delay to ensure session is set
            st.rerun()

# Main app
else:
    st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

    # Load and preprocess data
    df = pd.read_csv("AioocyteV1.csv", sep=";")
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('%', '', regex=False)
            df[col] = df[col].str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Placeholders for dynamic content
    video_placeholder = st.empty()
    supervivencia_placeholder = st.empty()
    metrics_placeholder = st.empty()
    grafico_placeholder = st.empty()
    slider_placeholder = st.empty()
    controles_placeholder = st.empty()
    logo_placeholder = st.empty()

    def mostrar_contenido():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        with video_placeholder:
            if os.path.exists(frame_path):
                image = Image.open(frame_path)
                st.image(image, caption=f"second {st.session_state.second}", use_container_width=True)
            else:
                st.warning("No se encontró imagen.")

        dato = df.iloc[st.session_state.second]
        with supervivencia_placeholder:
            st.markdown(f"""
                <div style='text-align: center; margin-top: 12px; margin-bottom: 0px;'>
                    <div class='survival-text' style='font-weight: bold; color: #005EA8; line-height: 0.85;'>
                        {dato['Survival']:.1f}%
                    </div>
                    <div class='survival-caption' style='color: #444; margin-top: 6px;'>Probability of oocyte survival after vitrification</div>
                </div>
                <hr style="margin: 1px 0;">
            """, unsafe_allow_html=True)

        with metrics_placeholder:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div class='metric-label' style='color:#888;'>Area %</div>
                        <div class='metric-value' style='font-weight:bold; color:#222'>{dato['Area%']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div class='metric-label' style='color:#888;'>Circularity</div>
                        <div class='metric-value' style='font-weight:bold; color:#222'>{dato['Circularity']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div class='metric-label' style='color:#888;'>Dehydration rate %/s</div>
                        <div class='metric-value' style='font-weight:bold; color:#222'>{dato['Vdeshidratacion']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col4:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div class='metric-label' style='color:#888;'>Deplasmolysis rate %/s</div>
                        <div class='metric-value' style='font-weight:bold; color:#222'>{dato['Vdeplasmolisi']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True
                )

        with grafico_placeholder:
            st.image("slider_background_final.png", use_container_width=True)

    def render_slider():
        with slider_placeholder:
            selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
            if selected != st.session_state.second:
                st.session_state.second = selected
                st.session_state.playing = False
                mostrar_contenido()
                mostrar_logo()

    def mostrar_logo():
        with logo_placeholder:
            st.markdown("""
            <div style='text-align: center; margin-top: 18px;'>
                <a href='https://www.fertilab.com' target='_blank'>
                    <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                         alt='Fertilab Barcelona' width='240'/>
                </a>
            </div>
            """, unsafe_allow_html=True)

    # Initial render
    mostrar_contenido()
    render_slider()
    mostrar_logo()

    # Control buttons
    with controles_placeholder:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            if st.button("⏪ Back"):
                st.session_state.second = max(0, st.session_state.second - 1)
                st.session_state.playing = False
                mostrar_contenido()
                render_slider()
                mostrar_logo()
        with col2:
            if st.button("▶️ Play 1x"):
                st.session_state.playing = True
                st.session_state.speed = 1
        with col3:
            if st.button("⏩ Forward"):
                st.session_state.second = min(359, st.session_state.second + 1)
                st.session_state.playing = False
                mostrar_contenido()
                render_slider()
                mostrar_logo()
        with col4:
            if st.button("⏸️ Pause"):
                st.session_state.playing = False
        with col5:
            if st.button("⏹️ Stop"):
                st.session_state.playing = False
                st.session_state.second = 0
                mostrar_contenido()
                render_slider()
                mostrar_logo()
        with col6:
            if st.button("⏩ Play 5x"):
                st.session_state.playing = True
                st.session_state.speed = 5

    # Playback loop
    if st.session_state.playing:
        for _ in range(500):
            if not st.session_state.playing or st.session_state.second >= 359:
                st.session_state.playing = False
                break
            time.sleep(0.5)
            st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
            mostrar_contenido()
            render_slider()
            mostrar_logo()

    # Logout button
    if st.button("Cerrar Sesión"):
        st.logout()
        st.session_state.logged_in = False
        logout_url = (
            "https://dev-47xxwxkuddgbl0fo.us.auth0.com/v2/logout?"
            "client_id=mTQf6FD1dPJm8SVz7sVaFh7LRlnQWMrI&"
            "returnTo=https://app-app0-app-hwq3xjpohg7cilzdu34ba8.streamlit.app"
        )
        components.html(
            f"""
            <script>
                window.location.href = "{logout_url}";
            </script>
            """,
            height=0
        )