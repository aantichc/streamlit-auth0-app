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
    st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide", initial_sidebar_state="collapsed")
    st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

    # Custom CSS for light mode and horizontal metrics layout
    st.markdown("""
        <style>
        /* Force light mode */
        body, .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }
        /* Horizontal metrics layout */
        .metrics-row {
            display: flex;
            flex-wrap: nowrap;
            justify-content: space-between;
            width: 100%;
        }
        .metrics-row > div {
            flex: 1;
            min-width: 0;
            margin: 0 10px;
        }
        </style>
    """, unsafe_allow_html=True)

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
            st.markdown('<div class="metrics-row">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

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
            f"https://dev-47xxwxkuddgbl0fo.us.auth0.com/v2/logout?"
            f"client_id=mTQf6FD1dPJm8SVz7sVaFh7LRlnQWMrI&"
            f"https://app-app0-app-hwq3xjpohg7cilzdu34ba8.streamlit.app"
        )
        components.html(
            f"""
            <script>
                window.location.href = '{logout_url}';
            </script>
            """,
            height=0
        )