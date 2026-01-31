import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Konfiguracja strony (opcjonalnie, ale warto mieć)
st.set_page_config(page_title="Doradca SP56", page_icon="🏫")

st.title("System Doradcy SP56")

# Nawiązanie połączenia z Google Sheets
# Streamlit automatycznie pobierze dane z Twoich Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Odczyt danych z arkusza "Użytkownicy"
    # Upewnij się, że nazwa arkusza w Google Sheets to dokładnie: Użytkownicy
    df = conn.read(worksheet="Użytkownicy", usecols=[0, 1, 2, 3])
    
    # Wyświetlenie danych (do testów, czy działa)
    st.success("Połączono z bazą danych!")
    st.dataframe(df)

except Exception as e:
    st.error("Wystąpił problem z połączeniem.")
    st.info("Upewnij się, że klucz w Secrets jest poprawnie wklejony (z potrójnym cudzysłowem).")
    st.exception(e)
