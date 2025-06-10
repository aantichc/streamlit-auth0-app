
import streamlit as st

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Check if user is already logged in
if st.user and st.user.is_logged_in:
    st.session_state.logged_in = True

if not st.session_state.logged_in:
    st.title("Sistema de Registro/Login")
    st.header("Iniciar Sesión o Registrarse")
    st.write("Haz clic para acceder o crear una cuenta con Auth0.")
    if st.button("Iniciar Sesión / Registrarse"):
        st.login("auth0")
        if st.user and st.user.is_logged_in:
            st.session_state.logged_in = True
            st.rerun()

else:
    st.title("Aplicación Principal")
    st.write("Hola Sergi Novo! Has iniciado sesión, aquí colocaríamos tu app 🎉")
    st.write(f"¡Bienvenido, {st.user.name}! Has iniciado sesión correctamente.")
    st.write(f"Correo: {st.user.email}")
    if st.button("Cerrar Sesión"):
        st.logout()
        st.session_state.logged_in = False
        st.rerun()