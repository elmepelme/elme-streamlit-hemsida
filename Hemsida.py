import streamlit as st
st.set_page_config(
    page_title = "Hemsida",
    page_icon="📘",
    layout = 'wide',
)

st.subheader("Hej, mitt namn är Elmir!")
st.title("Student i Civilingenjörsprogrammet i Teknisk Matematik")
st.write(
    'Jag är på mitt fjärde år av programmet, och planerar att specialisera mig i Bildanalys och Maskinintelligens samt Finansiell Modellering.' \
    ' På sidan om jobbar jag även deltid hos Lunds Kommun som studentmedarbetare i statistisk analys 📈')
st.write(
    'Denna hemsida är skapad för att enklare ladda upp och dela projekt. Välj ett projekt i sidofältet för att se mer!'
)
st.write(" ")
st.markdown('---')
#st.sidebar.success("Välj en sida ovan.")
#st.subheader("Kontakt:")
#st.write("Mail: elmirn@hotmail.com")
#st.write("LinkedIn: https://www.linkedin.com/in/elmir-nahodovic/")