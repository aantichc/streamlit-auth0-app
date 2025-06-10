
import streamlit as st
import streamlit.components.v1 as components
import time

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Check if user is already logged in
if st.user and st.user.is_logged_in:
    st.session_state.logged_in = True

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

else:
    st.title("Aplicación Principal")
    st.write("Hola Sergi Novo! Has iniciado sesión, aquí colocaríamos tu app 🎉")
    st.write(f"¡Bienvenido, {st.user.name}! Has iniciado sesión correctamente."")
    st.write(f"Correo: {st.user.email}")
    if st.button("Cerrar Sesión"):
        st.logout()
        st.session_state.logged_in = False
        # Redirect to Auth0 logout URL
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