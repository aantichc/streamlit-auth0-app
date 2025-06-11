import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import os
import time

# Force light mode and brighten button text with custom CSS
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
        background-color: #005EA8 !important; /* Optional: Set a contrasting background */
        font-weight: bold !important;
    }
    /* Ensure button text remains bright on hover */
    .stButton > button:hover {
        color: #ffffff !important;
        background-color: #004080 !important; /* Slightly darker shade on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Main app (from app.py)
else:
    st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")
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
                    <div style='font-size: 96px; font-weight: bold; color: #005EA8; line-height: 0.85;'>
                        {dato['Survival']:.1f}%
                    </div>
                    <div style='font-size: 22px; color: #444; margin-top: 6px;'>Probability of oocyte survival after vitrification</div>
                </div>
                <hr style="margin: 1px 0;">
            """, unsafe_allow_html=True)

        with metrics_placeholder:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div style='font-size:16px; color:#888;'>Area %</div>
                        <div style='font-size:28px; font-weight:bold; color:#222'>{dato['Area%']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div style='font-size:16px; color:#888;'>Circularity</div>
                        <div style='font-size:28px; font-weight:bold; color:#222'>{dato['Circularity']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div style='font-size:16px; color:#888;'>Dehydration rate %/s</div>
                    <div style='font-size:28px; font-weight:bold; color:#222'>{dato['Vdeshidratacion']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            with col4:
                st.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <div style='font-size:16px; color:#888;'>Deplasmolysis rate %/s</div>
                        <div style='font-size:28px; font-weight:bold; color:#222'>{dato['Vdeplasmolisi']:.2f}%</div>
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
            <div style='text-align: center; margin-top: 18