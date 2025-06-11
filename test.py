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
    /* Style Streamlit buttons (e.g., Logout) */
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
    /* Ensure Streamlit button text remains bright on hover */
    .stButton > button:hover {
        color: #ffffff !important;
        background-color: #004080 !important;
    }
    /* Style custom control buttons */
    .control-button {
        color: #ffffff !important; /* Bright white text */
        background-color: #005EA8 !important; /* Match Streamlit buttons */
        font-weight: bold !important;
        font-size: calc(0.5rem + 0.25vw) !important; /* Smaller text */
        padding: 0.1rem 0.2rem !important; /* Tighter padding */
        margin: 0 !important;
        width: 100% !important; /* Full width within control-item */
        box-sizing: border-box !important;
        border: none !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        text-align: center !important;
        display: inline-block !important;
    }
    .control-button:hover {
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
        padding: 0 !important; /* Remove padding to maximize space */
        margin: 0 !important; /* Remove margins */
    }
    .control-item {
        flex: 0 0 auto !important; /* Shrink to content */
        min-width: 25px !important; /* Further reduced min-width */
        text-align: center !important;
        padding: 0.05rem !important; /* Tighter padding */
        box-sizing: border-box !important;
        transform-origin: center !important;
    }
    /* Shrink buttons on narrow screens */
    @media (max-width: 600px) {
        .control-item {
            transform: scale(0.8) !important; /* Shrink by 80% */
        }
        .control-button {
            font-size: calc(0.4rem + 0.2vw) !important;
            padding: 0.05rem 0.1rem !important;
        }
    }
    @media (max-width: 400px) {
        .control-item {
            transform: scale(0.6) !important; /* Shrink by 60% */
        }
        .control-button {
            font-size: calc(0.35rem + 0.15vw) !important;
            padding: 0.03rem 0.08rem !important;
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
    st.title("Sistema de Login")
    st.header("Iniciar Sesión o Registrarse")
    st.write("Accede o crea una cuenta con Auth0.")
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

    # Control buttons with custom HTML and JavaScript
    with controls_placeholder:
        buttons = [
            ("⏪ Back", "back"),
            ("▶️ Play 1x", "play_1x"),
            ("⏩ Forward", "forward"),
            ("⏸️ Pause", "pause"),
            ("⏹️ Stop", "stop"),
            ("⏩ Play 5x", "play_5x")
        ]
        button_html = "<div class='controls-container'>"
        for label, action in buttons:
            button_html += f"""
                <div class='control-item'>
                    <button class='control-button' onclick='setButtonClicked("{action}")'>{label}</button>
                </div>
            """
        button_html += "</div>"

        # Render buttons
        st.markdown(button_html, unsafe_allow_html=True)

        # JavaScript to update session state
        components.html(
            """
            <script>
            function setButtonClicked(action) {
                if (window.Streamlit) {
                    Streamlit.setComponentValue(action);
                } else {
                    console.error("Streamlit API not available");
                }
            }
            </script>
            """,
            height=0
        )

        # Capture button clicks
        button_action = st.query_params.get("button_action")
        if button_action:
            st.session_state.button_clicked = button_action
            st.query_params.clear()  # Clear query params to prevent repeated triggers

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