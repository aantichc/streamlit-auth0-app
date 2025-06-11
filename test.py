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
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = None

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
    /* Style buttons */
    .stButton > button {
        color: #ffffff !important; /* Bright white text */
        background-color: #005EA8 !important; /* Contrasting background */
        font-weight: bold !important;
        font-size: calc(0.6rem + 0.3vw) !important; /* Tighter button text scaling */
        padding: 0.2rem 0.4rem !important; /* Compact padding */
        margin: 0 !important; /* Remove margins */
        width: auto !important; /* Default to content width */
        box-sizing: border-box !important;
        border-radius: 4px !important;
        white-space: nowrap !important; /* Prevent text wrapping */
    }
    /* Control buttons within flexbox */
    .control-item .stButton > button {
        width: 100% !important; /* Full width within control-item */
        font-size: calc(0.5rem + 0.25vw) !important; /* Even smaller for narrow screens */
        padding: 0.1rem 0.2rem !important; /* Tighter padding */
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
        font-size: calc(0.6rem + 0.6vw) !important; /* Tighter write text scaling */
    }
    /* Scale survival probability text */
    .survival-text {
        font-size: calc(1.4rem + 2vw) !important; /* Tighter survival % scaling */
    }
    .survival-caption {
        font-size: calc(0.6rem + 0.5vw) !important; /* Tighter caption scaling */
    }
    /* Scale metrics text */
    .metric-label {
        font-size: calc(0.5rem + 0.4vw) !important; /* Smaller metric labels */
        white-space: nowrap !important; /* Prevent label wrapping */
        overflow: hidden !important;
        text-overflow: visible !important; /* Allow full text to show */
    }
    .metric-value {
        font-size: calc(0.7rem + 0.6vw) !important; /* Smaller metric values */
        min-height: 1.5rem !important; /* Consistent height for alignment */
    }
    /* Custom flexbox for metrics to stay horizontal */
    .metrics-container {
        display: flex !important;
        flex-wrap: nowrap !important; /* Prevent wrapping */
        overflow-x: auto !important; /* Horizontal scrollbar */
        width: 100% !important;
        gap: 0.1rem !important; /* Minimal spacing between metrics */
    }
    .metric-item {
        flex: 1 !important; /* Equal width distribution */
        min-width: 90px !important; /* Tighter fit */
        text-align: center !important;
        padding: 0.1rem !important; /* Minimal padding */
        box-sizing: border-box !important;
    }
    /* Custom flexbox for control buttons to stay horizontal */
    .controls-container {
        display: flex !important;
        flex-wrap: nowrap !important; /* Prevent wrapping */
        overflow-x: auto !important; /* Horizontal scrollbar */
        width: 100% !important;
        gap: 0.05rem !important; /* Tighter spacing between buttons */
    }
    .control-item {
        flex: 0 0 auto !important; /* Shrink to content */
        min-width: 30px !important; /* Reduced min-width for shrinking */
        text-align: center !important;
        padding: 0.05rem !important; /* Tighter padding */
        box-sizing: border-box !important;
        transform-origin: center !important;
    }
    /* Shrink buttons on narrow screens */
    @media (max-width: 600px) {
        .control-item {
            transform: scale(0.8) !important; /* Shrink buttons by 80% */
        }
        .control-item .stButton > button {
            font-size: calc(0.4rem + 0.2vw) !important; /* Smaller text */
            padding: 0.05rem 0.1rem !important; /* Tighter padding */
        }
    }
    @media (max-width: 400px) {
        .control-item {
            transform: scale(0.6) !important; /* Shrink further by 60% */
        }
        .control-item .stButton > button {
            font-size: calc(0.35rem + 0.15vw) !important; /* Even smaller text */
        }
    }
    /* Ensure container width adapts */
    .main .block-container {
        max-width: 100% !important;
        padding: 0.5rem !important; /* Tighter padding */
    }
    /* Scrollbar styling for metrics and controls */
    .metrics-container::-webkit-scrollbar, .controls-container::-webkit-scrollbar {
        height: 6px !important; /* Thinner scrollbar */
    }
    .metrics-container::-webkit-scrollbar-thumb, .controls-container::-webkit-scrollbar-thumb {
        background: #005EA8 !important; /* Match app theme */
        border-radius: 3px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login page
if not st.session_state.logged_in:
    st.title("Vitrification Viability via Osmotic Response Calculator")
    if st.button("Log in / Sign up"):
        st.login("auth0")
        if st.user and st.user.is_logged_in:
            st.session_state.logged_in = True
            time.sleep(0.5)
            st.rerun()

# Main app
else:
    st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

    # Load and preprocess data
    df = pd.read_csv("AioocyteV1.csv", sep=";")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace("%", "").str.replace(",", ".", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Placeholders for dynamic content
    video_placeholder = st.empty()
    survival_placeholder = st.empty()
    metrics_placeholder = st.empty()
    grafico_placeholder = st.empty()
    slider_placeholder = st.empty()
    controls_placeholder = st.empty()
    logo_placeholder = st.empty()

    def mostrar_contenido():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        with video_placeholder:
            if os.path.exists(frame_path):
                image = Image.open(frame_path)
                st.image(image, caption=f"Frame {st.session_state.second}", use_container_width=True)
            else:
                st.caption("Image not found.")

        dato = df.iloc[int(st.session_state.second)]
        with survival_placeholder:
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <div class='survival-text' style='font-weight: bold; color: #005EA8'>
                        {dato['Survival']:.1f}%
                    </div>
                    <div class='survival-caption' style='color: #555'>Probability of oocyte survival after vitrification</div>
                </div>
                <hr style='margin: 0.5rem 0;'>
                """,
                unsafe_allow_html=True
            )

        with metrics_placeholder:
            st.markdown(
                f"""
                <div class='metrics-container'>
                    <div class='metric-item'>
                        <div class='metric-label' style='color:#888;'>Area %</div>
                        <div class='metric-value' style='font-weight: bold; color:#222'>{dato['Area%']:.3f}</div>
                    </div>
                    <div class='metric-item'>
                        <div class='metric-label' style='color:#888;'>Circularity</div>
                        <div class='metric-value' style='font-weight: bold; color:#222'>{dato['Circularity']:.3f}</div>
                    </div>
                    <div class='metric-item'>
                        <div class='metric-label' style='color:#888;'>Dehydration rate %/s</div>
                        <div class='metric-value' style='font-weight: bold; color:#222'>{dato['Vdeshidratacion']:.2f}%</div>
                    </div>
                    <div class='metric-item'>
                        <div class='metric-label' style='color:#888;'>Deplasmolysis rate %/s</div>
                        <div class='metric-value' style='font-weight: bold; color:#222'>{dato['Vdeplasmolisi']:.2f}%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with grafico_placeholder:
            st.image("slider_background_final.png", use_container_width=True)

    def render_slider():
        with slider_placeholder:
            selected = st.slider("🕒", 0, 359, value=int(st.session_state.second), label_visibility="collapsed")
            if selected != st.session_state.second:
                st.session_state.second = selected
                st.session_state.playing = False
                mostrar_contenido()
                mostrar_logo()

    def mostrar_logo():
        with logo_placeholder:
            st.markdown(
                """
                <div style='text-align: center; margin-top: 1rem;'>
                    <a href='https://www.fertilab.com' target='_blank'>
                        <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                             alt='Fertilab Barcelona' width='200'/>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Initial render
    mostrar_contenido()
    render_slider()
    mostrar_logo()

    # Control buttons with form for interactivity
    with controls_placeholder:
        with st.form(key="control_form"):
            st.markdown("<div class='controls-container'>", unsafe_allow_html=True)
            buttons = [
                ("⏪ Back", "back"),
                ("▶️ Play 1x", "play_1x"),
                ("⏩ Forward", "forward"),
                ("⏸️ Pause", "pause"),
                ("⏹️ Stop", "stop"),
                ("⏩ Play 5x", "play_5x")
            ]
            for label, action in buttons:
                st.markdown("<div class='control-item'>", unsafe_allow_html=True)
                if st.form_submit_button(label):
                    st.session_state.button_clicked = action
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Process button actions
    if st.session_state.button_clicked == "back":
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
        mostrar_contenido()
        render_slider()
        mostrar_logo()
        st.session_state.button_clicked = None
    elif st.session_state.button_clicked == "play_1x":
        st.session_state.playing = True
        st.session_state.speed = 1
        st.session_state.button_clicked = None
    elif st.session_state.button_clicked == "forward":
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
        mostrar_contenido()
        render_slider()
        mostrar_logo()
        st.session_state.button_clicked = None
    elif st.session_state.button_clicked == "pause":
        st.session_state.playing = False
        st.session_state.button_clicked = None
    elif st.session_state.button_clicked == "stop":
        st.session_state.playing = False
        st.session_state.second = 0
        mostrar_contenido()
        render_slider()
        mostrar_logo()
        st.session_state.button_clicked = None
    elif st.session_state.button_clicked == "play_5x":
        st.session_state.playing = True
        st.session_state.speed = 5
        st.session_state.button_clicked = None

    # Playback loop
    if st.session_state.playing:
        for _ in range(500):
            if not st.session_state.playing or st.session_state.second >= 359:
                st.session_state.playing = False
                break
            time.sleep(0.3)
            st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
            mostrar_contenido()
            render_slider()
            mostrar_logo()

    # Logout button
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    if st.button("Log out"):
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
    st.markdown("</div>", unsafe_allow_html=True)