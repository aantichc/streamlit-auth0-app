import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Sistema de Registro/Login")
    tab1, tab2 = st.tabs(["Registro", "Inicio de Sesión"])

    with tab1:
        st.header("Registrar Nueva Cuenta")
        st.write("Haz clic para registrarte con Auth0.")
        if st.button("Registrarme"):
            st.login("auth0")  # Removed client_kwargs
            st.session_state.logged_in = st.user.is_logged_in
            st.rerun()

    with tab2:
        st.header("Iniciar Sesión")
        st.write("Haz clic para iniciar sesión con Auth0.")
        if st.button("Ingresar"):
            st.login("auth0")  # Removed client_kwargs
            st.session_state.logged_in = st.user.is_logged_in
            st.rerun()

else:
    st.title("Aplicación Principal")
    st.write("Hello World! 🎉")
    st.write(f"¡Bienvenido, {st.user.name}! Has iniciado sesión correctamente.")
    st.write(f"Correo: {st.user.email}")
    if st.button("Cerrar Sesión"):
        st.logout()
        st.session_state.logged_in = False
        st.rerun()